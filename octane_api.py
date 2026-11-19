import requests
import urllib3

from auth import get_session
from parser import parse_features
from fields import FIELDS
from config import (
    FEATURE_API,
    HEADERS,
    LIMIT,
    OFFSET
)


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_features():

    print("=" * 60)
    print("Getting Feature Data From Octane API")
    print("=" * 60)

    params = {
        "fields": FIELDS,
        "limit": LIMIT,
        "offset": OFFSET    
    }

    try: 

        session = get_session()
    
        response = session.get(
            FEATURE_API,
            headers=HEADERS,
            params=params,
            verify=False,
            timeout=60
        )

        print(
            "Status Code:",
            response.status_code
        )

        response.raise_for_status()

        data = response.json()

        for item in data.get("data",[]):
            if item.get("product_areas") is not None:
                print(item["product_areas"])
                break

        print(
            "Total Features:",
            data.get("total_count")
        )

        print("=" * 60)

        return data
    
    except requests.exceptions.Timeout:

        print(
            "ERROR: Octane API Timeout"
        )

        return None

    except requests.exceptions.RequestException as e:

        print(
            "API Request Error"
        )

        print(e)

        return None

if __name__ == "__main__":

    result = get_features()

    if result:

        print(
            result.keys()
        )
