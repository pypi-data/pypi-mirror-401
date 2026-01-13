import os
import sys

# Add src to path
sys.path.append(os.getcwd())

from src.core.rag import get_pipeline_for_tier
from dotenv import load_dotenv

load_dotenv()

def test_pipeline():
    print("🧪 Testing RAG Pipeline Construction...")
    
    # Init Pro Tier
    try:
        pipeline = get_pipeline_for_tier("pro")
        print("✅ Pro Pipeline Initialized")
    except Exception as e:
        print(f"❌ Failed to init Pro pipeline: {e}")
        return

    # Ingest
    text = """
    The Apollo 11 mission was the first manned mission to land on the Moon. 
    Neil Armstrong and Buzz Aldrin walked on the lunar surface. 
    Michael Collins orbited in the command module.
    """
    print("📄 Ingesting text...")
    try:
        count = pipeline.ingest(text, collection_name="test_pipeline_coll")
        print(f"✅ Ingested {count} chunks.")
    except Exception as e:
        print(f"❌ Ingestion failed: {e}")
        return

    # Query
    q = "Who stayed in orbit?"
    print(f"🔍 Querying: '{q}'")
    try:
        results = pipeline.query(q, top_k=1)
        if results:
            print(f"✅ Result: {results[0].page_content}")
        else:
            print("⚠️ No results found.")
    except Exception as e:
        print(f"❌ Query failed: {e}")

if __name__ == "__main__":
    test_pipeline()
