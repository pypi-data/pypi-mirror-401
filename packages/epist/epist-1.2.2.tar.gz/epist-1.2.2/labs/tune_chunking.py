from langchain_community.document_loaders import TextLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

TRANSCRIPT_PATH = "labs/data/transcript_audio_style.txt"

def test_threshold(text, percentile):
    print(f"\n--- Testing Threshold: {percentile} (percentile) ---")
    embeddings = OpenAIEmbeddings()
    splitter = SemanticChunker(
        embeddings,
        breakpoint_threshold_type="percentile",
        breakpoint_threshold_amount=percentile
    )
    docs = splitter.create_documents([text])
    
    print(f"Created {len(docs)} chunks.")
    for i, doc in enumerate(docs):
        print(f"Chunk {i+1} (len={len(doc.page_content)}): {doc.page_content[:50]}... ...{doc.page_content[-50:]}")
        # Check for topic keywords to see separation
        topics = []
        if "privacy" in doc.page_content.lower() or "refrigerator" in doc.page_content.lower(): topics.append("Privacy")
        if "solar" in doc.page_content.lower(): topics.append("Solar")
        if "batteries" in doc.page_content.lower(): topics.append("Batteries")
        if "space" in doc.page_content.lower() or "orbit" in doc.page_content.lower(): topics.append("Space")
        print(f"  -> Topics found: {topics}")

def main():
    loader = TextLoader(TRANSCRIPT_PATH)
    docs = loader.load()
    text = "\n".join([d.page_content for d in docs])
    
    # Test range
    for p in [95, 90, 80, 70, 60, 50]:
        test_threshold(text, float(p))

if __name__ == "__main__":
    main()
