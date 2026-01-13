import os
import json
import time
import requests
from dotenv import load_dotenv
import pandas as pd
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Load environment variables
load_dotenv()

# Default to Staging if not specified
API_URL = os.getenv("API_URL", "https://epist-api-staging-920152096400.us-central1.run.app/api/v1")
API_KEY = os.getenv("STAGING_API_KEY") or os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY or STAGING_API_KEY must be set in .env")

HEADERS = {"x-api-key": API_KEY}
AUDIO_PATH = "labs/data/sample_podcast.mp3"
DATASET_PATH = "labs/data/golden_dataset.json"
RESULTS_DIR = "labs/results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def check_health():
    try:
        resp = requests.get(f"{API_URL.replace('/api/v1', '')}/health")
        return resp.status_code == 200
    except:
        return False

def upload_audio():
    print(f"Uploading {AUDIO_PATH}...")
    with open(AUDIO_PATH, "rb") as f:
        files = {"file": ("sample_podcast.mp3", f, "audio/mpeg")}
        resp = requests.post(f"{API_URL}/audio/upload", headers=HEADERS, files=files)
    
    if resp.status_code != 201:
        raise Exception(f"Upload failed: {resp.text}")
    
    audio_id = resp.json()["id"]
    print(f"Uploaded Audio ID: {audio_id}")
    return audio_id

def wait_for_processing(audio_id):
    print("Waiting for processing...")
    while True:
        resp = requests.get(f"{API_URL}/audio/{audio_id}", headers=HEADERS)
        status = resp.json()["status"]
        print(f"Status: {status}")
        if status == "completed":
            break
        if status == "failed":
            raise Exception("Processing failed")
        time.sleep(2)
    print("Processing complete.")

def run_queries(dataset):
    results = []
    print("Running queries...")
    for item in dataset:
        question = item["user_input"]
        ground_truth = item["reference"]
        
        print(f"Q: {question}")
        
        # Call Chat Endpoint
        payload = {
            "messages": [{"role": "user", "content": question}],
            "stream": False
        }
        resp = requests.post(f"{API_URL}/chat/completions", headers=HEADERS, json=payload)
        
        if resp.status_code != 200:
            print(f"Error: {resp.text}")
            continue
            
        data = resp.json()
        answer = data["choices"][0]["message"]["content"]
        citations = data["citations"] or []
        contexts = [c["text"] for c in citations]
        
        results.append({
            "question": question,
            "answer": answer,
            "contexts": contexts,
            "ground_truth": ground_truth
        })
        
    return results

def main():
    if not check_health():
        print("API is not running. Please start the backend.")
        return

    # 1. Upload & Index
    try:
        audio_id = upload_audio()
        wait_for_processing(audio_id)
    except Exception as e:
        print(f"Setup failed: {e}")
        # If upload fails (e.g. already exists), we might want to skip or handle it.
        # For now, let's assume we need to upload.
        return

    # 2. Load Dataset
    with open(DATASET_PATH) as f:
        golden_data = json.load(f)
    
    # 3. Run Benchmark
    query_results = run_queries(golden_data)
    
    # 4. Evaluate with RAGAS
    print("Evaluating with RAGAS...")
    df = pd.DataFrame(query_results)
    rag_dataset = Dataset.from_pandas(df)
    
    # Use GPT-4o for evaluation
    evaluator_llm = ChatOpenAI(model="gpt-4o")
    
    scores = evaluate(
        rag_dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
        ],
        llm=evaluator_llm,
    )
    
    print("Results:")
    print(scores)
    
    # 5. Save Results
    results_path = f"{RESULTS_DIR}/baseline_results.json"
    # Convert EvaluationResult to dict (it behaves like a dict of metrics)
    results_dict = dict(scores)
    with open(results_path, "w") as f:
        json.dump(results_dict, f, indent=2)
    
    # Save detailed dataframe
    df.to_csv(f"{RESULTS_DIR}/baseline_details.csv")
    print(f"Saved results to {results_path}")

if __name__ == "__main__":
    main()
