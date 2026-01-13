import phoenix as px
from openinference.instrumentation.openai import OpenAIInstrumentor
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Launch Phoenix
session = px.launch_app()
if session is None:
    raise RuntimeError("Failed to launch Phoenix app")
print(f"Phoenix UI: {session.url}")

# Instrument
OpenAIInstrumentor().instrument()

# Client
client = OpenAI()

print("Sending test trace...")
try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say hello to Phoenix!"}],
    )
    print(f"Response: {response.choices[0].message.content}")
    print("Trace sent. Check UI.")
except Exception as e:
    print(f"Error: {e}")

# Keep alive
import time
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping...")
