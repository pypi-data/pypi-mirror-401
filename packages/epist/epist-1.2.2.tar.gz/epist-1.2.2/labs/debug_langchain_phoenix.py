import os
from dotenv import load_dotenv
import phoenix as px
from openinference.instrumentation.openai import OpenAIInstrumentor
from openinference.instrumentation.langchain import LangChainInstrumentor
from langchain_openai import ChatOpenAI

load_dotenv()

# Do not launch app, connect to existing
# os.environ["PHOENIX_PROJECT_NAME"] = "debug_langchain" 
# session = px.launch_app()

# Set project name for the tracer
os.environ["PHOENIX_PROJECT_NAME"] = "grand_benchmark"

# Instrument
OpenAIInstrumentor().instrument()
LangChainInstrumentor().instrument()

print("Sending LangChain trace...")
try:
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    response = llm.invoke("Hello from LangChain!")
    print(f"Response: {response.content}")
    print("Trace sent. Check 'debug_langchain' project.")
except Exception as e:
    print(f"Error: {e}")

# Keep alive
import time
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping...")
