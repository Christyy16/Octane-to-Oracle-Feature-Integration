from dotenv import load_dotenv
from fields import FIELDS

import os

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

SHARED_SPACE_ID = os.getenv("SHARED_SPACE_ID")
WORKSPACE_ID = os.getenv("WORKSPACE_ID")

ORACLE_USER = os.getenv("ORACLE_USER")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")
ORACLE_HOST = os.getenv("ORACLE_HOST")
ORACLE_PORT = int(os.getenv("ORACLE_PORT"))
ORACLE_SERVICE = os.getenv("ORACLE_SERVICE")

HEADERS = {
    "Accept": "application/json",
    "XSRF-HEADER": os.getenv("XSRF-HEADER"),
    "HPECLIENTTYPE": os.getenv("HPECLIENTTYPE")    
}


FEATURE_API = (
    f"{BASE_URL}/api/shared_spaces/"
    f"{SHARED_SPACE_ID}/workspaces/"
    f"{WORKSPACE_ID}/features"
)

SWAGGER_URL = f"{BASE_URL}/ui/xxxx-xxxx/swagger.jsp"

LIMIT = 100
OFFSET = 0

TABLE_NAME="OCTANE_FEATURES"