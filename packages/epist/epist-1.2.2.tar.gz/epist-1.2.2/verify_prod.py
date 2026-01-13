import json

import httpx

PROD_URL = "https://epist-api-prod-920152096400.us-central1.run.app"
API_KEY = "Uc9Fy5tVHI7mD86rskWMvykNk0oMfH00"


def test_health():
    print(f"Testing health: {PROD_URL}/health")
    try:
        response = httpx.get(f"{PROD_URL}/health")
        print(f"Status: {response.status_code}, Response: {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")


def test_diagnostic():
    print(f"Testing diagnostic: {PROD_URL}/api/v1/diagnostic/network")
    headers = {"X-API-Key": API_KEY}
    try:
        response = httpx.get(f"{PROD_URL}/api/v1/diagnostic/network", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error detail: {response.text}")
    except Exception as e:
        print(f"Diagnostic failed: {e}")


def test_stats():
    print(f"Testing stats: {PROD_URL}/api/v1/stats")
    headers = {"X-API-Key": API_KEY}
    try:
        response = httpx.get(f"{PROD_URL}/api/v1/stats", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error detail: {response.text}")
    except Exception as e:
        print(f"Stats check failed: {e}")


if __name__ == "__main__":
    test_health()
    test_diagnostic()
    test_stats()
