import os
import json
import time
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

# Load env
load_dotenv()

API_KEY = os.getenv("FIREWORKS_API_KEY")
AUDIO_PATH = "labs/data/conversation.wav"
RESULTS_DIR = "labs/results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def transcribe_with_diarization(audio_path):
    print(f"Uploading {audio_path} to Fireworks...")
    
    url = "https://api.fireworks.ai/inference/v1/audio/transcriptions"
    
    with open(audio_path, "rb") as f:
        files = {
            "file": ("conversation.wav", f, "audio/wav"),
        }
        data = {
            "model": "whisper-v3",
            "response_format": "verbose_json",
            "timestamp_granularities[]": ["segment", "word"],
            "diarization": "true",
            "diarization_config": json.dumps({
                "min_speakers": 2,
                "max_speakers": 2
            })
        }
        headers = {
            "Authorization": f"Bearer {API_KEY}"
        }
        
        resp = requests.post(url, headers=headers, files=files, data=data)
        
    if resp.status_code != 200:
        raise Exception(f"Transcription failed: {resp.text}")
        
    return resp.json()

def process_transcript(data):
    segments = data.get("segments", [])
    documents = []
    
    print(f"Found {len(segments)} segments.")
    
    for seg in segments:
        text = seg.get("text", "").strip()
        start = seg.get("start")
        end = seg.get("end")
        speaker = seg.get("speaker", "unknown") # Fireworks returns 'speaker' field
        
        if not text:
            continue
            
        # Create Document with Speaker Metadata
        doc = Document(
            page_content=text,
            metadata={
                "start": start,
                "end": end,
                "speaker": speaker,
                "source": "conversation.wav"
            }
        )
        documents.append(doc)
        
    return documents

def run_rag(documents, query):
    print("Indexing documents...")
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=OpenAIEmbeddings(),
        collection_name="speaker_test"
    )
    
    # Test Retrieval
    print(f"Querying: {query}")
    retriever = vectorstore.as_retriever()
    docs = retriever.invoke(query)
    
    for d in docs:
        print(f"Retrieved: [{d.metadata['speaker']}] {d.page_content}")
        
    # Cleanup
    vectorstore.delete_collection()
    return docs

def main():
    if not API_KEY:
        print("FIREWORKS_API_KEY not set.")
        return

    # 1. Transcribe
    try:
        result = transcribe_with_diarization(AUDIO_PATH)
        # Save raw result
        with open(f"{RESULTS_DIR}/diarization_raw.json", "w") as f:
            json.dump(result, f, indent=2)
    except Exception as e:
        print(f"Error: {e}")
        return

    # 2. Process
    documents = process_transcript(result)
    
    # 3. Verify Speakers
    speakers = set(d.metadata['speaker'] for d in documents)
    print(f"Identified Speakers: {speakers}")
    
    # 4. Run Test RAG
    # Since we don't have a QA dataset for this synthetic file, we just verify retrieval works
    run_rag(documents, "What did the male speaker say?")
    
    print("Experiment Complete.")

if __name__ == "__main__":
    main()
