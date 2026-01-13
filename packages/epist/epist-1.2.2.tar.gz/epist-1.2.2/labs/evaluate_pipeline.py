import os
import json
import pandas as pd
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_openai import ChatOpenAI
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from datasets import Dataset

from src.core.rag.pipeline import get_pipeline_for_tier

# Load env variables
load_dotenv()

TRANSCRIPT_PATH = "labs/data/transcript_audio_style.txt"
DATASET_PATH = "labs/data/dataset_audio_style.json"
RESULTS_DIR = "labs/results"
os.makedirs(RESULTS_DIR, exist_ok=True)


def run_evaluation(tier_name: str, pipeline, golden_data: list[dict]):
    print(f"\n--- Evaluating Tier: {tier_name} ---")
    
    # 1. Ingest Data (Chunks & Indexes)
    print("Ingesting transcript...")
    loader = TextLoader(TRANSCRIPT_PATH)
    raw_docs = loader.load()
    text_content = "\n".join([d.page_content for d in raw_docs])
    
    num_chunks = pipeline.ingest(text_content, collection_name=f"eval_{tier_name.lower()}")
    print(f"Ingested {num_chunks} chunks.")

    # 2. Run Queries & Generate Answers
    print("Running queries...")
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    
    results = []
    
    for item in golden_data:
        question = item["user_input"]  # or "question" depending on json format
        ground_truth = item["reference"] # or "ground_truth"
        
        try:
            # Retrieve
            retrieved_docs = pipeline.query(question, top_k=2)
            contexts = [d.page_content for d in retrieved_docs]
            
            # Generate Answer
            context_block = "\n\n".join(contexts)
            prompt = f"Answer the question based ONLY on the following context:\n\n{context_block}\n\nQuestion: {question}"
            
            response = llm.invoke(prompt)
            answer = response.content
            
            results.append({
                "question": question,
                "answer": answer,
                "contexts": contexts,
                "ground_truth": ground_truth
            })
            
        except Exception as e:
            print(f"Error on query '{question}': {e}")

    # 3. Evaluate with Ragas
    if not results:
        print("No results to evaluate.")
        return {}

    df = pd.DataFrame(results)
    rag_dataset = Dataset.from_pandas(df)
    
    print(f"Running Ragas metrics for {tier_name}...")
    scores = evaluate(
        rag_dataset,
        metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
        llm=ChatOpenAI(model="gpt-4o")
    )
    
    final_scores = scores.to_pandas().select_dtypes(include=['number']).mean().to_dict()
    print(f"Scores for {tier_name}: {final_scores}")
    
    # Check if vectorstore needs cleanup if possible (not exposed in pipeline currently)
    # But since it's in-memory Chroma or local, it's fine for this script run
    
    return final_scores, results

def main():
    # Load Dataset
    with open(DATASET_PATH) as f:
        # Check structure
        data = json.load(f)
        # Handle if it's a list or dict
        if isinstance(data, dict) and "questions" in data:
            golden_data = data["questions"]
        elif isinstance(data, list):
            golden_data = data
        else:
            # Fallback for simple structure likely in current file
            golden_data = data
            
    # Run Comparisons
    results_summary = {}
    
    # 1. Free Tier
    pipeline_free = get_pipeline_for_tier("free")
    results_summary["Free"], pipeline_free_details = run_evaluation("Free", pipeline_free, golden_data)
    
    # 2. Pro Tier
    pipeline_pro = get_pipeline_for_tier("pro")
    results_summary["Pro"], pipeline_pro_details = run_evaluation("Pro", pipeline_pro, golden_data)
    
    # Save Summary
    with open(f"{RESULTS_DIR}/pipeline_comparison.json", "w") as f:
        json.dump(results_summary, f, indent=2)

    # Save details
    with open(f"{RESULTS_DIR}/details_free.json", "w") as f:
        json.dump(pipeline_free_details, f, indent=2)
    with open(f"{RESULTS_DIR}/details_pro.json", "w") as f:
        json.dump(pipeline_pro_details, f, indent=2)
        
    print("\n--- Final Comparison ---")
    print(json.dumps(results_summary, indent=2))

if __name__ == "__main__":
    main()
