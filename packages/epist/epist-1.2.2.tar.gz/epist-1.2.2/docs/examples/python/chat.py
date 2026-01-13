import json
import os

import requests

# Configuration
API_KEY = os.getenv("EPIST_API_KEY", "sk_live_replace_me")
BASE_URL = "https://api.epist.ai/v1"
HEADERS = {"X-API-Key": API_KEY, "Content-Type": "application/json"}


def chat_rag(question):
    """
    Sends a chat request. The backend automatically retrieves relevant
    context from your audio knowledge base (RAG).
    """
    print(f"User: {question}")

    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=HEADERS,
        json={
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            "model": "gpt-4-turbo",
            "stream": True,  # Enable streaming
        },
        stream=True,
    )

    print("Assistant: ", end="", flush=True)

    # Handle Streaming Response
    for line in response.iter_lines():
        if line:
            line_text = line.decode("utf-8")
            if line_text.startswith("data: "):
                data_str = line_text.replace("data: ", "")
                if data_str == "[DONE]":
                    break
                try:
                    data = json.loads(data_str)
                    token = data["choices"][0]["delta"].get("content", "")
                    print(token, end="", flush=True)

                    # Citations might be sent in a specific delta or footer
                    if "citations" in data:
                        print(f"\n\n[Citations: {data['citations']}]")

                except json.JSONDecodeError:
                    pass
    print("\n")


if __name__ == "__main__":
    chat_rag("What were the key action items from the last meeting?")
