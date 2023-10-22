import os
import tracemalloc

from typing import Any, Dict

from cognite.client import ClientConfig, CogniteClient
from cognite.client.credentials import OAuthClientCredentials
from dotenv import load_dotenv
from handler import handle


load_dotenv()

CDF_CLIENT_NAME = "manual_run"


# def get_local_client(env):
def get_local_client():
    """
    Functionality: Retrieves a CDF client
    Parameters:
    ---
    ---
    Return:
    client (cognite.CogniteClient): instantiated client used to access data from and write data to CDF
    """
    CLIENT_ID = os.environ.get("CLIENT_ID_IIND")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET_IIND")
    COGNITE_PROJECT = os.environ.get("COGNITE_PROJECT")
    CDF_CLUSTER = os.environ.get("CDF_CLUSTER")
    TENANT_ID = os.environ.get("TENANT_ID_IIND")
    TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    SCOPES = [f"https://{CDF_CLUSTER}.cognitedata.com/.default"]
    BASE_URL = f"https://{CDF_CLUSTER}.cognitedata.com"
    creds = OAuthClientCredentials(token_url=TOKEN_URL, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scopes=SCOPES)

    cnf = ClientConfig(
        client_name=CDF_CLIENT_NAME, project=COGNITE_PROJECT, base_url=BASE_URL, credentials=creds, debug=False
    )
    client = CogniteClient(cnf)
    res = client.assets.list(limit=1)
    if len(res) == 1:
        print("CONNECTION SUCCESSFUL")
        print(f"Cognite SDK Version {client.version}")
    return client


# IF WORKING WITH MULTIPLE ENVIRONMENTS, CAN PASS ENV AS PARAMETER TO GET LOCAL CLIENT FUNCTION
# env = "iind"
# client = get_local_client(env=env)
client = get_local_client()
secrets = {}
data: Dict[str, Any] = {'queue_name':'mrt'}

# start monitoring
tracemalloc.start()

if client is not None:
    try:
        handle(data, client, secrets)
        print(
            "MEMORY USAGE:\nPEAK SIZE OF MEMORY BLOCKS TRACED BY tracemalloc:\n",
            round(tracemalloc.get_traced_memory()[1] / 1e9, 2),
            "GB",
        )
        # stopping the library
        tracemalloc.stop()

    except Exception as error:
        print(error)