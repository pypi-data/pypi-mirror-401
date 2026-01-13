import json

import httpx

STAGING_URL = "https://epist-api-staging-920152096400.us-central1.run.app"
API_KEY = "yaSwFNMVCrYup1m65XZvAJd5vgEqD0yl"


def test_health():
    print(f"Testing health: {STAGING_URL}/health")
    try:
        response = httpx.get(f"{STAGING_URL}/health")
        print(f"Status: {response.status_code}, Response: {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")


def test_diagnostic():
    print(f"Testing diagnostic: {STAGING_URL}/api/v1/diagnostic/network")
    headers = {"X-API-Key": API_KEY}
    try:
        response = httpx.get(f"{STAGING_URL}/api/v1/diagnostic/network", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error detail: {response.text}")
    except Exception as e:
        print(f"Diagnostic failed: {e}")


def test_upload_repro():
    """Simulate the Python SDK upload that caused 422 errors."""
    print(f"Testing upload repro: {STAGING_URL}/api/v1/audio/upload")
    files = {"file": ("test.mp3", b"fake audio content", "audio/mpeg")}
    data = {"preset": "general", "chunking_config": json.dumps({"chunk_size": 1000})}
    headers = {"X-API-Key": API_KEY}
    try:
        response = httpx.post(f"{STAGING_URL}/api/v1/audio/upload", files=files, data=data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code in [201, 200]:
            print("Success!")
        else:
            print(f"Failed with {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Upload repro failed: {e}")


def test_connectivity():
    print(f"Testing connectivity: {STAGING_URL}/health/connectivity")
    try:
        response = httpx.get(f"{STAGING_URL}/health/connectivity")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error detail: {response.text}")
    except Exception as e:
        print(f"Connectivity check failed: {e}")


if __name__ == "__main__":
    # Note: These will likely fail until deployment is finished
    test_health()
    test_diagnostic()
    test_connectivity()
    test_upload_repro()
