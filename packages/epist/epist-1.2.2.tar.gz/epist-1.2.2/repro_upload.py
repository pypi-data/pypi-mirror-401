import threading
import time

import httpx
import uvicorn
from fastapi import BackgroundTasks, Depends, FastAPI, File, Form, Request, UploadFile

app = FastAPI()


async def get_session():
    return "session"


async def get_current_user():
    return "user"


@app.post("/upload")
async def upload_audio(
    request: Request,
    file: UploadFile = File(description="Audio file to upload"),
    preset: str = Form("general"),
    chunking_config: str | None = Form(None),
    session: str = Depends(get_session),
    current_user: str = Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return {"status": "ok", "filename": file.filename, "preset": preset}


def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8001)


if __name__ == "__main__":
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    time.sleep(2)

    url = "http://127.0.0.1:8001/upload"

    print("--- Test 1: Files only ---")
    files = {"file": ("test.mp3", b"content", "audio/mpeg")}
    try:
        r = httpx.post(url, files=files)
        print(f"Status: {r.status_code}")
        print(f"Body: {r.text}")
    except Exception as e:
        print(f"Error: {e}")

    print("\n--- Test 2: Standard SDK pattern ---")
    headers = {"X-API-Key": "test"}
    # SDK does files=files, headers=headers
    try:
        r = httpx.post(url, files=files, headers=headers)
        print(f"Status: {r.status_code}")
        print(f"Body: {r.text}")
    except Exception as e:
        print(f"Error: {e}")

    print("\n--- Test 3: Including data ---")
    data = {"preset": "podcast"}
    try:
        r = httpx.post(url, files=files, data=data)
        print(f"Status: {r.status_code}")
        print(f"Body: {r.text}")
    except Exception as e:
        print(f"Error: {e}")
