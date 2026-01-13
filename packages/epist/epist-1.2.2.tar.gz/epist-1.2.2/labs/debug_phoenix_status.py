import phoenix as px
import requests
import json

PHOENIX_URL = "http://localhost:6006"

print(f"Checking Phoenix at {PHOENIX_URL}...")

# method 1: GraphQL
query = """
{
  projects {
    name
  }
}
"""
try:
    response = requests.post(f"{PHOENIX_URL}/graphql", json={"query": query})
    print("GraphQL Response:", response.text)
except Exception as e:
    print("GraphQL failed:", e)

# Method 2: Python Client (if running in same process, but we are external)
# We can't easily attach to the *other* process's memory.
# But we can try to use the client to query the remote URL if supported.

print("\nTrying to send a probe trace to 'grand_benchmark'...")
from openinference.instrumentation.openai import OpenAIInstrumentor
from openai import OpenAI
import os

os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = "http://localhost:6006/v1/traces"
os.environ["PHOENIX_PROJECT_NAME"] = "grand_benchmark"

client = OpenAI()
OpenAIInstrumentor().instrument()

try:
    client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Probe trace"}],
    )
    print("Probe trace sent.")
except Exception as e:
    print(f"Probe failed: {e}")
