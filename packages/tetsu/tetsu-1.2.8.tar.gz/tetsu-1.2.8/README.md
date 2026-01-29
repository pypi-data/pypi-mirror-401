<div align="center">
  <img src="https://i.imgur.com/bwBBG4X.jpg"><br>
</div>

# tetsu: a Python helper toolkit 
**tetsu** (*tetsudai* - Japanese for 'helper') is a Python toolkit designed to streamline data science and
engineering projects. It consolidates common helper scripts into a single, easy-to-use package, reducing project setup
time and removing development blockers.
---
### Getting Started

**Installation**

Install tetsu directly from your terminal using pip:

```bash
pip install tetsu
```

**Core Concepts**

The helpers in `tetsu` fall into two categories:

1. **Function-Based (Class-less)**: Simple, direct functions for services like code scans, Cloudant, Mime, logging, and TM1.

2. **Class-Based:** Helpers that require instantiation for services like Box, Cloud Object Storage (COS), and DB2.

**Credential Management**: The `cloudant_helper` is central to `tetsu`. You typically call it once at the beginning of
your project. By default, it securely stores your credentials document as an environment variable, which other tetsu
helpers can then access automatically.
---
### Usage Examples

### Function-Based helpers

`scans`

Run security and dependency scans on your project.

**Option 1: From the Terminal (Recommended)**

```bash
# Run a scan on the entire project
python -m tetsu.scans

# Scan a specific subdirectory
python -m tetsu.scans ./path/to/your/app

# Exclude a custom-named virtual environment
python -m tetsu.scans --venv-name .venv

# Change the output log file name
python -m tetsu.scans --log-file security_report.log

```

**Option 2: From a Python Script**

Create a script (e.g., `run_checks.py`) in your project's root directory. This is useful for integrating scans into a
CI/CD pipeline.

```python
import sys
from tetsu import run_scans

# Run scans on the current directory, excluding a '.venv' folder and saving the output to 'scan_results.log'.
success = run_scans(
    target_directory='.',
    venv_name='.venv',
    log_file='scan_results.log'
)
if not success:
    sys.exit(1)
```

---
`cloudant_helper`

Fetch a credentials document from Cloudant. This document is cached for use by other helpers.

```python
import tetsu as ts

doc = ts.cloudant_helper.get_document(document_id='dsc-finds2')
```

> Note: It is expected that the Cloudant API key is stored as an environment variable called CLOUDANT_IAM_API_KEY
---
`mime_helper`

Send emails programmatically.

```python
import tetsu as ts

ts.mime_helper.send_message(
    sender_email='john.doe@ibm.com',
    receiver_email='jane.doe@ibm.com',
    subject='MIME Example',
    message_body='This is how you send an email using tetsu'
)
```

---
`log_helper`

Set up consistent logging across all your project scripts.

1. In your main script (e.g., `main.py`), set up logging once:

```python
import logging
import tetsu as ts

ts.setup_logging()

log = logging.getLogger(__name__)
```

2. At the start of all your other scripts

```python
import logging

log = logging.getLogger(__name__)
```

> Note: This helper requires a logging.yaml file located in your /project_folder/config directory.
---
`tm1_helper`

Interact with TM1 cubes to pull and push data.

```python
import tetsu as ts

# Pull data using an MDX query
example_mdx = open("config/incur_expense.txt", 'r').read()

df = ts.tm1_helper.tm1_pull(
    mdx_query=example_mdx,
    environment='prod',
    cube='ibmpsend'
)

# Push data to a TM1 cube
ts.tm1_helper.tm1_push(
    df=df,
    environment='uat',
    cube='ibmplanning'
)
```

### Class-based helpers

`db2_helper`

Connect to and query a DB2 database.

```python 
import tetsu as ts

# In this example, Db2Helper will use the previously pulled FINDS2 credentials and the deployment environment used here is staging
db2_conn = ts.DB2Helper(environment='staging',
                        driver='ODBC')  # default is ODBC 

df = db2_conn.db2_pull("SELECT * from EPM.DIM_GEOGRAPHY LIMIT 10")
```

**Overriding the default arguments**

If you need to use a different credentials document or specify a more complex credential structure, you can pass them
directly during initialization.

```python 
import tetsu as ts

# 1. Fetch a different Cloudant doc without saving it to the environment
custom_doc = ts.cloudant_helper.get_document(
    document_id='csgm-finds1',
    save_env=False  # Prevents overwriting the default doc in the environment
)

# 2. Define the path to each credential within the document
custom_creds = {
    "username": ['staging', 'db2', 'username'],
    "password": ['staging', 'db2', 'password'],
    "hostname": ['staging', 'db2', 'hostname'],
    "port": ['staging', 'db2', 'port'],
    "database": ['staging', 'db2', 'database'],
    "trustpass": ['staging', 'db2', 'trustpass']  # Example of an extra parameter
}

# 3. Initialize the helper with the custom doc and credential map
db2_conn = ts.DB2Helper(
    cloudant_doc=custom_doc,
    environment='staging',
    creds=custom_creds
)

df = db2_conn.db2_pull("SELECT * from EPM.DIM_GEOGRAPHY LIMIT 10")
```

---
`cos_helper`

Manage files in IBM Cloud Object Storage (COS).

```python
import tetsu as ts

cos_conn = ts.COSHelper(
    environment='dsc-internal'
   # You can use custom creds here to override any of the connection params
   # e.g. creds={"auth_endpoints": ['prod-dallas', 'cos', 'auth_endpoints']}
)

cos_conn.upload_file(files_list=['data/test.csv', 'data/test2.csv'])
```
--- 

`box_helper`

Connect to Box to manage files and folders.

```python
import pandas as pd

import tetsu as ts

# Option 1: Initialize using the default Cloudant document
box_conn = ts.BoxHelper()

# Option 2: Initialize using a local JWTAuth JSON file
box_conn2 = ts.BoxHelper(auth_filepath='local/path/to/JWTAuth/Json/file')

# Example: Upload a Pandas DataFrame to a specific Box folder as a CSV 
df = pd.DataFrame([[1, 2, 3], [4, 5, 6]])
box_conn.upload_df(
    data=df,
    path='path/to/local-dir/where/df/should/be/saved',
    folder_id='your_box_folder_id',
    file_type='csv'
)

```

## Contributing to tetsu

Contributions are welcome! We encourage bug reports, fixes, documentation improvements, and new features.

**Development Process**

1. **Create an Issue**: Before starting work, please create a GitHub issue to track the development.

2. **Create a Branch**: Name your branch using the convention issue_name-initialsdev.

    * Example: upgrade_cloudant_helper-hkdev

3. **Develop & Test**: Write your code and add any necessary tests.

4. **Submit a Pull Request**: Create a Pull Request (PR) from your branch into main. Please assign both Rahul and Hassan
   as reviewers.