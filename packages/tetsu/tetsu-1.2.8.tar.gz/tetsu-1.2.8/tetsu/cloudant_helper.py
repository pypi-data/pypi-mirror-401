"""
Facilitate communication with Cloudant
"""

import logging
import os
from base64 import b64decode, b64encode
from sys import platform
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core.api_exception import ApiException

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

logger = logging.getLogger(__name__)

CLOUDANT_URL = os.getenv("CLOUDANT_ACCOUNT", "https://848f0f0a-7ff0-4280-9a93-994725506313-bluemix.cloudant.com")
CLOUDANT_DATABASE = os.getenv("CLOUDANT_DATABASE", "epm-finance-dst")
CLOUDANT_API_KEY = os.getenv("CLOUDANT_IAM_API_KEY")


def get_document(
        document_id: str,
        save_env: bool = True,
) -> dict:
    """
    Connects to cloudant and gets requested document.

    :param document_id: name of document in your cloudant database environment variables
    :param save_env: If the cloudant document should be saved as an environment variable
    :return: cloudant document as json-like nested dictionary
    """

    try:
        authenticator = IAMAuthenticator(CLOUDANT_API_KEY)
        client = CloudantV1(authenticator=authenticator)
        client.set_service_url(CLOUDANT_URL)

        doc = client.get_document(
            db=CLOUDANT_DATABASE,
            doc_id=document_id
        ).get_result()

        if save_env:
            os.environ["cloudant_doc"] = str(doc)

        logger.info(f"Successfully downloaded Cloudant document: {document_id}")
        return doc

    except ApiException as e:
        logger.exception(f"Error downloading document '{document_id}'. Status code: {e.code}. Error: {e.message}")
        raise


def get_credentials(doc: dict, creds: dict) -> dict:
    """
    Get credentials from cloudant, if password, decrypt if necessary.
        example:
            doc = get_document(document_id="DOC_NAME",
                               cloudant_api_key=os.getenv('CLOUDANT_API_KEY'))

            params = {"bot_auth_token": ['slack-bots', "staging", "pricing-bot", 'bot_auth_token'],
                      "slack_app_token": ['slack-bots', "staging", "pricing-bot", 'slack_app_token']}

            slack_creds = get_credentials(doc=doc,
                                          creds=params)

        :param doc: The document object returned from the get_document function
        :param creds: A credentials dictionary with the name of the secret as the key and the path as the value in a list

        :return: creds_dict: A dictionary with the retrieved secret values
    """
    try:
        creds_dict = {}
        for key in creds:
            creds_dict[key] = get_field_value(doc, creds[key])
    except Exception as e:
        logger.exception(f"Could not retrieve credentials due to {e}")
        raise e
    else:
        logger.info("Credentials have been retrieved")
    return creds_dict


def get_field_value(dct: dict, keys: list):
    """
    Get password from cloudant, decrypt if necessary.
    example:
    some_dict = {
        "jdbc":{
            "staging":{
                "username":"epmtaxon",
                "password":{
                    "varname":"CLOUDANT_DECRYPTION_KEY",
                    "value":"some_password"}}}}
    > get_field_value(some_dict, 'jdbc', 'staging', 'username')
    'finds1'
    :param dct: dictionary containing the field value you want to find
    :param keys: the keys needed to traverse down the nested dict
    :return: value you wanted to find
    """
    field = safe_get(dct, keys)

    if isinstance(field, dict):
        # New style: { "encrypted_value": "..." }
        if "encrypted_value" in field:
            return decrypt_value(field["encrypted_value"])
        # Old style: { "encrypted": true, "value": "..." }
        elif field.get("encrypted") and "value" in field:
            return decrypt_value(field["value"])
    else:
        return field


def safe_get(dct: dict, keys: list):
    """
    Allows you to easily and safely get nested dictionary values
    EXAMPLE
    some_dict = {
    "jdbc":{
       "staging":{
          "username":"epmtaxon",
          "password":{
             "varname":"CLOUDANT_DECRYPTION_KEY",
             "value":"some_password"}}}}
    > safe_get(some_dict, 'jdbc', 'staging', 'username')
    'epmtaxon'
    > safe_get(some_dict, 'jdbc', 'staging', 'password')
    {'varname': 'CLOUDANT_DECRYPTION_KEY',
     'value': 'some_password'}
    :param dct: dictionary like data structure
    :param keys: comma separated fields
    :return:  value
    """
    for key in keys:
        try:
            dct = dct[key]
        except (KeyError, TypeError):
            return None
    return dct


def decrypt_value(encrypted_val: str) -> str:
    """
    Decrypts a password using cloudant decryption key.
    :param encrypted_val: encrypted string
    :return: decrypted string
    """
    if platform == "win32" or platform == "darwin":
        rsa_key = open(os.path.join(r"config", r"id_rsa")).read()
    else:
        rsa_key = os.getenv("DST_CLOUDANT_DECRYPTION_KEY").replace(r"\n", "\n")
    try:
        private_key = serialization.load_pem_private_key(
            rsa_key.encode('utf-8'),
            password=None,
        )
        decoded_ciphertext = b64decode(encrypted_val)

        decrypted_message = private_key.decrypt(
            decoded_ciphertext,
            padding.PKCS1v15()
        )
        return decrypted_message.decode('utf-8')

    except Exception as e:
        logger.exception(f"Failed to decrypt value. Error: {e}")
        raise


def encrypt_value(value_to_encrypt: str) -> str:
    """
    Encrypts a string using an RSA public key from a file.

    :param value_to_encrypt: The plaintext string to encrypt.
    :return: A Base64 encoded encrypted string.
    """
    public_rsa_key = os.path.join(r'config', r'id_rsa.pub')

    try:
        # 2. Read the public key file
        with open(public_rsa_key, 'rb') as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read()
            )

        ciphertext = public_key.encrypt(
            value_to_encrypt.encode('utf-8'),
            padding.PKCS1v15()
        )

        return b64encode(ciphertext).decode('utf-8')

    except FileNotFoundError:
        print(f"Error: Public key file not found at {public_rsa_key}")
        raise
    except Exception as e:
        print(f"An error occurred during encryption: {e}")
        raise
