import os
import json
import time
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
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

# Configuration
AUDIO_TRANSCRIPT_PATH = "labs/data/transcript.txt" # JFK Speech
GOLDEN_DATASET_PATH = "labs/data/golden_dataset.json"
RESULTS_DIR = "labs/results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# 1. Propositional Chunker
class PropositionalChunker:
    def __init__(self, model_name="gpt-4o"):
        self.llm = ChatOpenAI(model=model_name, temperature=0)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """
            You are an expert content analyzer. Your task is to decompose the following text into "atomic propositions".
            A proposition is a self-contained, meaningful statement that captures a single fact or idea.
            
            Rules:
            1. Each proposition must be a complete sentence.
            2. Resolve pronouns (he, it, they) to their specific nouns (e.g., "He said" -> "President Kennedy said").
            3. Keep the original meaning intact.
            4. Return a JSON list of strings.
            """),
            ("user", "{text}")
        ])
        
    def split_text(self, text):
        # Naive first pass: split by paragraphs to avoid context window issues
        paragraphs = [p for p in text.split("\n\n") if p.strip()]
        all_propositions = []
        
        print(f"Processing {len(paragraphs)} paragraphs...")
        
        for i, para in enumerate(paragraphs):
            try:
                chain = self.prompt | self.llm | JsonOutputParser()
                propositions = chain.invoke({"text": para})
                if isinstance(propositions, list):
                    all_propositions.extend(propositions)
                print(f"  Paragraph {i+1}: Extracted {len(propositions)} propositions.")
            except Exception as e:
                print(f"  Error processing paragraph {i+1}: {e}")
                # Fallback: just use the paragraph itself
                all_propositions.append(para)
                
        return all_propositions

# 2. Pipeline
def run_experiment():
    # Load Transcript
    if not os.path.exists(AUDIO_TRANSCRIPT_PATH):
        print("Transcript not found. Please run baseline first.")
        return

    with open(AUDIO_TRANSCRIPT_PATH, "r") as f:
        full_text = f.read()

    # Load Golden Dataset
    with open(GOLDEN_DATASET_PATH, "r") as f:
        golden_data = json.load(f)
        
    questions = [item["user_input"] for item in golden_data]
    ground_truths = [item["reference"] for item in golden_data]

    # --- Run Pipeline: LLM Propositional ---
    print("\n--- Running Pipeline: LLM Propositional ---")
    
    chunker = PropositionalChunker()
    start_time = time.time()
    chunks = chunker.split_text(full_text)
    duration = time.time() - start_time
    
    print(f"Generated {len(chunks)} propositional chunks in {duration:.2f}s.")
    
    # Create Documents
    documents = [Document(page_content=c, metadata={"source": "jfk.wav", "chunk_index": i}) for i, c in enumerate(chunks)]
    
    # Index
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=OpenAIEmbeddings(),
        collection_name="llm_chunking_experiment"
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5}) # Retrieve more small chunks
    
    # Generate & Evaluate
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    
    answers = []
    contexts = []
    
    for query in questions:
        # Retrieve
        retrieved_docs = retriever.invoke(query)
        context_text = "\n".join([d.page_content for d in retrieved_docs])
        contexts.append([d.page_content for d in retrieved_docs])
        
        # Generate
        response = llm.invoke(f"Answer based on context:\n{context_text}\n\nQuestion: {query}")
        answers.append(response.content)
        
    # RAGAS Evaluation
    data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    }
    dataset = Dataset.from_dict(data)
    
    print("Evaluating with RAGAS...")
    scores = evaluate(
        dataset=dataset,
        metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
        llm=ChatOpenAI(model="gpt-4o")
    )
    
    # Robust Score Extraction
    # Convert to pandas, select numeric columns, calculate mean, convert to dict
    final_scores = scores.to_pandas().select_dtypes(include=['number']).mean().to_dict()
    
    print(f"LLM Chunking Scores: {final_scores}")
    
    # Save Results
    results = {
        "strategy": "LLM Propositional",
        "chunks_count": len(chunks),
        "processing_time": duration,
        "scores": final_scores
    }
    
    with open(f"{RESULTS_DIR}/llm_chunking_results.json", "w") as f:
        json.dump(results, f, indent=2)
        
    # Cleanup
    vectorstore.delete_collection()
    print("Experiment Complete.")

if __name__ == "__main__":
    run_experiment()
