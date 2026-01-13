import os
import json
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.document_loaders import TextLoader
from sentence_transformers import CrossEncoder
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

# Reranker Class
class RerankRetriever:
    def __init__(self, base_retriever, model_name="cross-encoder/ms-marco-MiniLM-L-6-v2", top_k=5):
        self.base_retriever = base_retriever
        self.model = CrossEncoder(model_name)
        self.top_k = top_k

    def invoke(self, query):
        # 1. Retrieve candidates (get more than needed)
        docs = self.base_retriever.invoke(query)
        
        if not docs:
            return []
            
        # 2. Score pairs
        pairs = [[query, d.page_content] for d in docs]
        scores = self.model.predict(pairs)
        
        # 3. Sort and filter
        scored_docs = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
        return [d for d, s in scored_docs[:self.top_k]]

def run_pipeline(name, retriever_func, queries):
    print(f"\n--- Running Pipeline: {name} ---")
    
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    
    results = []
    for item in queries:
        question = item["user_input"]
        ground_truth = item["reference"]
        
        # Retrieve
        try:
            # Handle both standard retrievers and our custom RerankRetriever
            if hasattr(retriever_func, 'invoke'):
                docs = retriever_func.invoke(question)
            else:
                docs = retriever_func(question)
                
            contexts = [d.page_content for d in docs]
            
            # Generate
            context_text = "\n\n".join(contexts)
            prompt = f"Answer based on context:\n{context_text}\n\nQuestion: {question}"
            response = llm.invoke(prompt)
            answer = response.content
            
            results.append({
                "question": question,
                "answer": answer,
                "contexts": contexts,
                "ground_truth": ground_truth
            })
        except Exception as e:
            print(f"Error processing query '{question}': {e}")

    # Evaluate
    df = pd.DataFrame(results)
    rag_dataset = Dataset.from_pandas(df)
    
    print(f"Evaluating {name} with RAGAS...")
    scores = evaluate(
        rag_dataset,
        metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
        llm=ChatOpenAI(model="gpt-4o")
    )
    
    # Extract scores
    final_scores = scores.to_pandas().select_dtypes(include=['number']).mean().to_dict()
    print(f"{name} Scores: {final_scores}")
    return final_scores

def main():
    # Load Data
    loader = TextLoader(TRANSCRIPT_PATH)
    documents = loader.load()
    
    with open(DATASET_PATH) as f:
        golden_data = json.load(f)
        
    # Chunking (Semantic - The Winner)
    print("Chunking Documents...")
    splitter = SemanticChunker(OpenAIEmbeddings())
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} semantic chunks.")
    
    # 1. Vector Retriever (Baseline)
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=OpenAIEmbeddings(),
        collection_name="exp_advanced_retrieval"
    )
    vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    
    # 2. BM25 Retriever
    bm25_retriever = BM25Retriever.from_documents(chunks)
    bm25_retriever.k = 5
    
    # 3. Ensemble Retriever (Hybrid)
    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, vector_retriever],
        weights=[0.5, 0.5]
    )
    
    # 4. Reranking Retriever (Hybrid + Rerank)
    # We retrieve top 20 candidates from Ensemble, then rerank to top 5
    ensemble_candidates = EnsembleRetriever(
        retrievers=[bm25_retriever, vector_retriever],
        weights=[0.5, 0.5]
    )
    # Hack: Set k on underlying retrievers to get more candidates
    # Note: Ensemble doesn't accept 'k' in constructor easily for underlying, 
    # so we rely on the retrievers' own k settings.
    # Let's boost the candidate pool for reranking
    vector_retriever_large = vectorstore.as_retriever(search_kwargs={"k": 10})
    bm25_retriever_large = BM25Retriever.from_documents(chunks)
    bm25_retriever_large.k = 10
    
    ensemble_large = EnsembleRetriever(
        retrievers=[bm25_retriever_large, vector_retriever_large],
        weights=[0.5, 0.5]
    )
    
    rerank_retriever = RerankRetriever(ensemble_large, top_k=5)
    
    # Run Experiments
    results = {}
    
    results["Vector (Baseline)"] = run_pipeline("Vector", vector_retriever, golden_data)
    results["Hybrid (Ensemble)"] = run_pipeline("Hybrid", ensemble_retriever, golden_data)
    results["Hybrid + Rerank"] = run_pipeline("Hybrid + Rerank", rerank_retriever, golden_data)
    
    # Save Results
    with open(f"{RESULTS_DIR}/advanced_retrieval_results.json", "w") as f:
        json.dump(results, f, indent=2)
        
    vectorstore.delete_collection()
    print("Experiment Complete.")

if __name__ == "__main__":
    main()
