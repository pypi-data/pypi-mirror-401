import os
import time

import requests

# Configuration
API_KEY = os.getenv("EPIST_API_KEY", "sk_live_replace_me")
BASE_URL = "https://api.epist.ai/v1"
HEADERS = {"X-API-Key": API_KEY}


def upload_audio(file_path):
    """Uploads a local audio file for transcription and indexing."""
    print(f"Uploading {file_path}...")
    with open(file_path, "rb") as f:
        response = requests.post(f"{BASE_URL}/audio/upload", headers=HEADERS, files={"file": f})
    return response.json()


def search_knowledge_base(query):
    """Searches the processed audio transcripts."""
    print(f"\nSearching for: '{query}'")
    response = requests.post(
        f"{BASE_URL}/search",
        headers=HEADERS,
        json={
            "query": query,
            "limit": 3,
            "rrf_k": 60,  # Optional: Tune rank fusion
        },
    )
    results = response.json()

    for i, res in enumerate(results, 1):
        print(f"{i}. [{res.get('score', 0):.2f}] {res.get('text', '')[:100]}...")
        # Access metadata like timestamps
        # print(f"   Time: {res.get('start_time')} - {res.get('end_time')}")


def main():
    # 1. Upload a File
    # Create a dummy file for demonstration if it doesn't exist
    demo_file = "demo_meeting.mp3"
    if not os.path.exists(demo_file):
        print("Please provide a real audio file path.")
        return

    # Upload
    upload_res = upload_audio(demo_file)
    print("Upload Response:", upload_res)

    # Note: In a real scenario, you might poll a task ID if the file is large.
    # The current API returns processed metadata synchronously for small files
    # or a task ID for large ones. Assuming sync for this example or wait.
    time.sleep(2)

    # 2. Search
    search_knowledge_base("roadmap Q3")


if __name__ == "__main__":
    main()
