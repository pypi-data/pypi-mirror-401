import os
import sys
import time

import epist
from dotenv import load_dotenv

load_dotenv()

# Goal: Show off the "killer feature"—Citations and Time.

client = epist.Client(api_key=os.getenv("EPIST_API_KEY"))

# Imagine this is a 60-minute Lex Fridman episode.
# Please place 'podcast.mp3' in the data directory.
file_path = os.path.join(os.path.dirname(__file__), "..", "data", "podcast.mp3")

if not os.path.exists(file_path):
    print("❌ Please place a 'podcast.mp3' in the 'data/' folder to run this recipe.")
    print("   (Any long-form audio will work)")
    sys.exit(1)

print(f"🚀 Uploading {file_path}...")
file = client.upload(file_path)

print("🧠 Indexing (creating temporal graph)...")
index = client.index.create([file.id])

while index.status != "ready":
    print("   ...analyzing prosody and content")
    time.sleep(2)
    index = client.index.get(index.id)

# The "Needle in a Haystack" query
# Standard RAG often fails here because it retrieves the wrong chunk.
# Epist uses the temporal graph to find the exact context.
query = "What book did the guest recommend?"
print(f"\n❓ Asking: '{query}'")

response = index.query(query)

print("------------------------------------------------")
if response.citations:
    # We use integer division // 60 for minutes
    minute = int(response.citations[0]["start"] // 60)
    print(f"🎙️ Found in episode at approx {minute} minutes")
else:
    print("🎙️ Answer found (no exact citation)")

print(f"📝 Answer: {response.text}")
print("------------------------------------------------")

# Generate a clickable link (Simulated)
if response.citations:
    start_sec = int(response.citations[0]["start"])
    print(f"🔗 Listen here: https://podcast-player.com/episode?t={start_sec}")
