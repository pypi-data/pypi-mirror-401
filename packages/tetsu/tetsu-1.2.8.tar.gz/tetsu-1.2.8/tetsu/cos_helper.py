# COS Helper --- Interact with COS via Python
import ast
import functools
import io
import logging
import os
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import IO, List, Dict, Union, Optional

import ibm_boto3
import pandas as pd
from ibm_boto3.s3.transfer import TransferConfig
from ibm_botocore.client import Config

from tetsu import cloudant_helper

logger = logging.getLogger(__name__)


def deprecated(new_name):
    """
    Decorator to mark functions as deprecated.
    It will emit a FutureWarning when the old function is called.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"'{func.__name__}' is deprecated and will be removed in a future version. "
                f"Please use '{new_name}' instead.",
                category=FutureWarning,
                stacklevel=2  # Points to the line in the USER'S script, not this line
            )
            return func(*args, **kwargs)

        return wrapper

    return decorator


class COSHelper:
    def __init__(
            self,
            environment: str,
            cloudant_doc=None,
            creds=None
    ):
        """
        Instantiation of the COSHelper class

        :param environment: The environment (prod/metrics or staging)
        :param cloudant_doc: The cloudant document object that will be used to retrieve credentials
                             If None, user env will be searched for a document
        """
        if creds is None:
            if cloudant_doc is None:
                try:
                    self.cloudant_doc = ast.literal_eval(os.getenv("cloudant_document"))
                except Exception as e:
                    raise RuntimeError("cloudant_document environment variable not set", e)
            else:
                self.cloudant_doc = cloudant_doc

            self.creds = {
                "cos_api_key": [environment, "cos", "apikey"],
                "cos_resource_crn": [environment, "cos", "resource_instance_id"],
                "cos_endpoint": [environment, "cos", "endpoints"],
                "cos_auth_endpoint": [environment, "cos", "auth_endpoint"],
            }
            self.creds = cloudant_helper.get_credentials(
                doc=self.cloudant_doc, creds=self.creds
            )
        else:
            self.creds = creds

        self.cos_object = ibm_boto3.client(
            service_name="s3",
            ibm_api_key_id=self.creds["cos_api_key"],
            ibm_service_instance_id=self.creds["cos_resource_crn"],
            ibm_auth_endpoint=self.creds["cos_auth_endpoint"],
            config=Config(signature_version="oauth"),
            endpoint_url=self.creds["cos_endpoint"],
        )

        # This allows for multi-part uploads for files greater than 5MB
        self.config = TransferConfig(
            multipart_threshold=1024 * 1024 * 25,
            max_concurrency=10,
            multipart_chunksize=1024 * 1024 * 25,
            use_threads=True,
        )

    def upload_files(self,
                     files_list: List[str],
                     cos_bucket: str,
                     file_key_list: List[str] = None) -> None:
        """
        Takes a list of local file paths and uploads them to the specified COS bucket.
        """
        if file_key_list is None:
            file_key_list = files_list
        for i, filename in enumerate(files_list):
            try:
                self.cos_object.upload_file(
                    Filename=filename, Bucket=cos_bucket, Key=file_key_list[i], Config=self.config
                )
                logger.info(f"File {filename} uploaded to {cos_bucket} successfully")
            except Exception as e:
                logger.exception(f"Could not upload file {filename} to {cos_bucket} due to {e}")

    def download_files(self,
                       cos_bucket: str,
                       files_list: List[str],
                       file_key_list: List[str] = None) -> None:
        """
        Takes a list of keys and downloads them from a COS bucket to the local filesystem.
        """
        if file_key_list is None:
            file_key_list = files_list
        for i, filename in enumerate(files_list):
            try:
                self.cos_object.download_file(
                    Filename=filename, Bucket=cos_bucket, Key=file_key_list[i]
                )
                logger.info(f"File {file_key_list[i]} downloaded from {cos_bucket} successfully")
            except Exception as e:
                logger.exception(f"Could not download file {file_key_list[i]} from {cos_bucket} due to {e}")

    def download_buffer(self, cos_bucket: str, key: str) -> Optional[io.BytesIO]:
        """
        Downloads a SINGLE file from the COS bucket returning it as an in-memory byte buffer.
        """
        buffer = io.BytesIO()
        try:
            self.cos_object.download_fileobj(cos_bucket, key, buffer)
            buffer.seek(0)
            return buffer
        except Exception as e:
            logger.exception(f"Failed to download buffer for {key}: {e}")
            return None

    def upload_buffer(self, cos_bucket: str, key: str, data: Union[IO, str]) -> None:
        """
        Uploads an in-memory, file-like object or string directly to the COS bucket.
        """
        if isinstance(data, str):
            data = io.BytesIO(initial_bytes=data.encode("utf-8"))

        # Ensure we are at the start of the stream
        if hasattr(data, 'seek'):
            data.seek(0)

        try:
            self.cos_object.upload_fileobj(data, cos_bucket, key)
            logger.info(f"Buffer uploaded to {cos_bucket} as {key} successfully")
        except Exception as e:
            logger.exception(f"Could not upload buffer to {cos_bucket} due to {e}")

    def download_buffers(self, cos_bucket: str, keys: List[str], max_workers: int = 10) -> Dict[str, io.BytesIO]:
        """
        Downloads MULTIPLE files concurrently into memory.
        Returns: Dict { 'key': BytesIO }
        """
        results = {}
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # We use self.download_buffer (the new method) to avoid triggering warnings
            future_to_key = {
                executor.submit(self.download_buffer, cos_bucket, key): key
                for key in keys
            }
            for future in as_completed(future_to_key):
                key = future_to_key[future]
                try:
                    data = future.result()
                    if data:
                        results[key] = data
                        logger.info(f"File '{key}' downloaded to memory successfully")
                except Exception as e:
                    logger.exception(f"Batch download failed for {key}: {e}")
        return results

    # ==========================================
    # DATA & UTILS (New Standard)
    # ==========================================

    def upload_dataframe(self,
                         df: pd.DataFrame,
                         file_name: str,
                         cos_bucket: str,
                         file_key: str = None,
                         file_type: str = None) -> None:
        """
        Takes a dataframe and uploads it to the specified COS bucket as CSV, Parquet, or Pickle.
        """
        filename = ""
        if file_type == "csv":
            filename = file_name + ".csv"
            df.to_csv(filename, sep=",", index=False)
        elif file_type == "parquet":
            filename = file_name + ".csv"  # NOTE: Kept original logic, but usually should be .parquet
            df.to_parquet(filename)
        elif file_type == "pickle":
            filename = file_name + ".pkl"
            df.to_pickle(filename)
        else:
            raise RuntimeError("Please pick from csv, parquet, or pickle")

        if file_key is None:
            file_key = filename

        try:
            self.cos_object.upload_file(
                Filename=filename,
                Bucket=cos_bucket,
                Key=file_key,
                Config=self.config,
            )
            logger.info(f"{filename} uploaded to {cos_bucket} successfully")
        except Exception as e:
            logger.exception(f"Could not upload {filename} to {cos_bucket} due to {e}")

    def list_keys(self, cos_bucket: str, prefix: str, token: str = None) -> List[str]:
        """
        Retrieves a list of all object keys under the given prefix in the COS bucket.
        """
        kws = {} if token is None else {"ContinuationToken": token}
        resp = self.cos_object.list_objects_v2(Bucket=cos_bucket, Prefix=prefix, **kws)

        contents = resp.get("Contents", [])
        keys = [c["Key"] for c in contents]

        next_token = resp.get("NextContinuationToken")
        if next_token is not None:
            keys += self.list_keys(cos_bucket, prefix, next_token)

        return keys

    # ==========================================
    # DEPRECATED WRAPPERS (Backward Compatibility)
    # ==========================================

    @deprecated(new_name="upload_files_from_disk")
    def upload_file(self, files_list: list, cos_bucket: str, file_key_list: list = None) -> None:
        return self.upload_files(files_list, cos_bucket, file_key_list)

    @deprecated(new_name="download_files_to_disk")
    def download_file(self, cos_bucket: str, files_list: list, file_key_list: list = None) -> None:
        return self.download_files(cos_bucket, files_list, file_key_list)

    @deprecated(new_name="upload_dataframe")
    def upload_df(self, df: pd.DataFrame, file_name: str, cos_bucket: str, file_key: str = None,
                  file_type: str = None) -> None:
        return self.upload_dataframe(df, file_name, cos_bucket, file_key, file_type)

    @deprecated(new_name="list_keys")
    def list_objects_by_prefix(self, cos_bucket: str, prefix: str, token: str = None) -> list[str]:
        return self.list_keys(cos_bucket, prefix, token)

    @deprecated(new_name="download_buffer")
    def download_fileobj(self, cos_bucket: str, key: str) -> io.BytesIO:
        return self.download_buffer(cos_bucket, key)

    @deprecated(new_name="upload_buffer")
    def upload_fileobj(self, cos_bucket: str, key: str, data: Union[IO, str]) -> None:
        return self.upload_buffer(cos_bucket, key, data)