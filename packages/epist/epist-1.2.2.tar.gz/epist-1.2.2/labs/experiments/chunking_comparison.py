import os
import json
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from datasets import Dataset

# Load env
load_dotenv()

TRANSCRIPT_PATH = "labs/data/transcript.txt"
DATASET_PATH = "labs/data/golden_dataset.json"
RESULTS_DIR = "labs/results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def run_pipeline(name, splitter, documents, queries):
    print(f"--- Running Pipeline: {name} ---")
    
    # 1. Split
    chunks = splitter.split_documents(documents)
    print(f"Generated {len(chunks)} chunks.")
    
    # 2. Index (Ephemeral Chroma)
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=OpenAIEmbeddings(),
        collection_name=f"test_{name}"
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    
    # 3. Generate Answers
    llm = ChatOpenAI(model="gpt-3.5-turbo") # Use 3.5 for generation to match baseline app
    
    results = []
    for item in queries:
        question = item["user_input"]
        ground_truth = item["reference"]
        
        # Retrieve
        docs = retriever.invoke(question)
        contexts = [d.page_content for d in docs]
        
        # Generate
        context_text = "\n\n".join(contexts)
        prompt = f"""You are an AI assistant. Answer the question based ONLY on the context.
Context:
{context_text}

Question: {question}
"""
        response = llm.invoke(prompt)
        answer = response.content
        
        results.append({
            "question": question,
            "answer": answer,
            "contexts": contexts,
            "ground_truth": ground_truth
        })
        
    # 4. Evaluate
    df = pd.DataFrame(results)
    rag_dataset = Dataset.from_pandas(df)
    
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
    
    print(f"{name} Scores: {scores}")
    
    # Cleanup
    vectorstore.delete_collection()
    
    # Convert to dict via pandas
    # EvaluationResult -> DataFrame -> Mean -> Dict
    scores_df = scores.to_pandas()
    # Select only numeric columns (metrics)
    aggregate_scores = scores_df.select_dtypes(include=['number']).mean().to_dict()
    
    return aggregate_scores

def main():
    # Load Data
    loader = TextLoader(TRANSCRIPT_PATH)
    documents = loader.load()
    
    with open(DATASET_PATH) as f:
        queries = json.load(f)
        
    results = {}
    
    # Pipeline 1: Baseline (Recursive)
    baseline_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    results["baseline"] = run_pipeline("Baseline", baseline_splitter, documents, queries)
    
    # Pipeline 2: Semantic
    semantic_splitter = SemanticChunker(
        OpenAIEmbeddings(),
        breakpoint_threshold_type="percentile" # Default
    )
    results["semantic"] = run_pipeline("Semantic", semantic_splitter, documents, queries)
    
    # Save Comparison
    with open(f"{RESULTS_DIR}/chunking_comparison.json", "w") as f:
        json.dump(results, f, indent=2)
        
    print("Experiment Complete. Results saved.")

if __name__ == "__main__":
    main()
