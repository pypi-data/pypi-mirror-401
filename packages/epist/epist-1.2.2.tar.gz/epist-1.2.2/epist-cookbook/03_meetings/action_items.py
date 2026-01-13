import os
import sys
import time

import epist
from dotenv import load_dotenv

load_dotenv()

# Goal: detailed extraction of tasks and assignees from a meeting.


def format_timestamp(seconds):
    """Converts seconds (float) to [MM:SS] format string."""
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"[{m:02d}:{s:02d}]"


client = epist.Client(api_key=os.getenv("EPIST_API_KEY"))

file_path = os.path.join(os.path.dirname(__file__), "..", "data", "meeting.mp3")
if not os.path.exists(file_path):
    print("❌ Please place a 'meeting.mp3' in the 'data/' folder.")
    sys.exit(1)

print("🚀 Uploading meeting recording...")
file = client.upload(file_path)

print("🧠 Indexing meeting content...")
index = client.index.create([file.id])

while index.status != "ready":
    print("   ...processing speakers and action items")
    time.sleep(2)
    index = client.index.get(index.id)

# A complex query asking for structure
query = "List all action items and who is responsible for them."
print(f"\n❓ Querying: '{query}'")

response = index.query(query)

print("\n--- 📋 Action Items Summary ---")
print(response.text)

print("\n--- 🕒 Evidence & Context ---")
# Show exactly where in the meeting these were discussed
for cit in response.citations:
    ts_str = format_timestamp(cit.get("start", 0))
    print(f"{ts_str} - Topic mentioned (Confidence: {cit.get('confidence')})")
