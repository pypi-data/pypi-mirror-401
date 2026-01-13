import os
import time
import phoenix as px
from openinference.instrumentation.openai import OpenAIInstrumentor
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from dotenv import load_dotenv

# Load env
load_dotenv()

def main():
    # 1. Launch Phoenix
    session = px.launch_app()
    print(f"\n🚀 Phoenix UI is running at: {session.url}\n")
    
    # 2. Instrument OpenAI
    OpenAIInstrumentor().instrument()
    
    print("Generating sample traces (JFK Speech)...")
    
    # 3. Run a quick RAG pipeline to generate traces
    text = """
    And so, my fellow Americans: ask not what your country can do for you--ask what you can do for your country.
    My fellow citizens of the world: ask not what America will do for you, but what together we can do for the freedom of man.
    """
    
    docs = [Document(page_content=text)]
    vectorstore = Chroma.from_documents(docs, OpenAIEmbeddings(), collection_name="phoenix_demo")
    retriever = vectorstore.as_retriever()
    llm = ChatOpenAI(model="gpt-4o")
    
    # Query 1
    query = "What should Americans ask?"
    print(f"  - Query: {query}")
    context = retriever.invoke(query)
    response = llm.invoke(f"Context: {context}\n\nQuestion: {query}")
    print(f"  - Answer: {response.content}")
    
    # Query 2
    query = "What about citizens of the world?"
    print(f"  - Query: {query}")
    context = retriever.invoke(query)
    response = llm.invoke(f"Context: {context}\n\nQuestion: {query}")
    print(f"  - Answer: {response.content}")
    
    print("\n✅ Traces generated!")
    print(f"👉 Go to {session.url} to view them.")
    print("Press Ctrl+C to stop the server.")
    
    # Keep server alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping server...")

if __name__ == "__main__":
    main()
