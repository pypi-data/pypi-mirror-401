import os
import json
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_classic.chains.hyde.base import HypotheticalDocumentEmbedder
from langchain_classic.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_experimental.text_splitter import SemanticChunker
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

def run_experiment():
    # Load Data
    loader = TextLoader(TRANSCRIPT_PATH)
    documents = loader.load()
    
    with open(DATASET_PATH) as f:
        golden_data = json.load(f)
        
    # Chunking (Semantic)
    splitter = SemanticChunker(OpenAIEmbeddings())
    chunks = splitter.split_documents(documents)
    
    # Index (Standard Embeddings)
    base_embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=base_embeddings,
        collection_name="exp_hyde"
    )
    
    # HyDE Embedder
    print("\n--- Initializing HyDE ---")
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    
    # Custom HyDE Prompt
    prompt_template = """Please answer the user's question about the JFK Inaugural Address.
    Question: {question}
    Answer:"""
    prompt = PromptTemplate(input_variables=["question"], template=prompt_template)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    
    hyde_embeddings = HypotheticalDocumentEmbedder(
        llm_chain=llm_chain,
        base_embeddings=base_embeddings
    )
    
    # HyDE Retriever
    # Note: We don't need a special retriever class, we just use the hyde_embeddings to query the vectorstore
    # BUT standard vectorstore.as_retriever() uses the embedding model stored in the vectorstore.
    # So we need to manually embed the query with HyDE and then search.
    
    print("Running Pipeline: HyDE...")
    results = []
    
    for item in golden_data:
        question = item["user_input"]
        ground_truth = item["reference"]
        
        # Manual HyDE Implementation
        # 1. Generate Hypothetical Document
        hypothetical_doc = llm_chain.invoke({"question": question})["text"]
        
        # 2. Embed Hypothetical Document
        query_vector = base_embeddings.embed_query(hypothetical_doc)
        
        # 2. Search Vectorstore with HyDE vector
        docs = vectorstore.similarity_search_by_vector(query_vector, k=5)
        
        contexts = [d.page_content for d in docs]
        
        # 3. Generate Answer
        context_text = "\n\n".join(contexts)
        gen_prompt = f"Answer based on context:\n{context_text}\n\nQuestion: {question}"
        response = llm.invoke(gen_prompt)
        answer = response.content
        
        results.append({
            "question": question,
            "answer": answer,
            "contexts": contexts,
            "ground_truth": ground_truth
        })

    # Evaluate
    df = pd.DataFrame(results)
    rag_dataset = Dataset.from_pandas(df)
    
    print("Evaluating HyDE with RAGAS...")
    scores = evaluate(
        rag_dataset,
        metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
        llm=ChatOpenAI(model="gpt-4o")
    )
    
    final_scores = scores.to_pandas().select_dtypes(include=['number']).mean().to_dict()
    print(f"HyDE Scores: {final_scores}")
    
    # Save Results
    with open(f"{RESULTS_DIR}/hyde_results.json", "w") as f:
        json.dump(final_scores, f, indent=2)
        
    vectorstore.delete_collection()
    print("Experiment Complete.")

if __name__ == "__main__":
    run_experiment()
