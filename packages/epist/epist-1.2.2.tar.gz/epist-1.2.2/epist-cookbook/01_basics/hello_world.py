import os
import sys
import time

import epist
from dotenv import load_dotenv

load_dotenv()

# Goal: Prove it works in structured, easy-to-read code.

# 1. Initialize the client
client = epist.Client(api_key=os.getenv("EPIST_API_KEY"))

# Ensure we have a file to test with
file_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample.mp3")
if not os.path.exists(file_path):
    print(f"❌ File not found: {file_path}")
    print("   -> Please place a 'sample.mp3' file in the 'data/' folder to run this demo.")
    sys.exit(1)

print("🚀 Uploading audio...")
file = client.upload(file_path)

# 2. Create an Index (The "Brain")
print("🧠 Indexing audio into Temporal Graph...")
index = client.index.create([file.id])

# Wait for status to be ready (polling helper)
while index.status != "ready":
    print("   ...processing (this may take a moment)")
    time.sleep(2)
    index = client.index.get(index.id)

# 3. Query the Audio
question = "What is the main topic of this recording?"
print(f"\n❓ Asking: '{question}'")

answer = index.query(question)

print(f"\n✨ Answer: {answer.text}")

if answer.citations:
    cit = answer.citations[0]
    print(f"   ⏱️  Citation: {cit['start']}s - {cit['end']}s (Confidence: {cit['confidence']})")
else:
    print("   No citations found.")
