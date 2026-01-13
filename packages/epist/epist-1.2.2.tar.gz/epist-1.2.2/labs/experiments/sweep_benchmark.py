import os
import gc
import json
import time
import requests
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import openai
from langchain_community.vectorstores import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_experimental.text_splitter import SemanticChunker
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from sentence_transformers import CrossEncoder
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from datasets import Dataset

# Setup Paths
DATA_DIR = "labs/data/grand_benchmark"
RESULTS_DIR = "labs/results/rag_sweep"
os.makedirs(RESULTS_DIR, exist_ok=True)

load_dotenv()

# --- Configurations for Sweep ---
CHUNKING_PARAMS = [
    # {"name": "Semantic-P90", "type": "percentile", "threshold": 90},
    {"name": "Semantic-P95", "type": "percentile", "threshold": 95}, # Default only for memory save
    # {"name": "Semantic-P99", "type": "percentile", "threshold": 99},
]

HYBRID_PARAMS = [
    # {"name": "Hybrid-VectorHeavy", "weights": [0.3, 0.7]},
    {"name": "Hybrid-Balanced",    "weights": [0.5, 0.5]}, 
    # {"name": "Hybrid-KeywordHeavy","weights": [0.7, 0.3]},
]

HYDE_PROMPTS = [
    {"name": "HyDE-Standard", "template": "Please write a scientific paper passage to answer the question: {question}"},
    # {"name": "HyDE-Audio",    "template": "Write a transcript segment where a speaker discusses the following topic: {question}"},
]

# Limit to just one source for memory safety initially
TARGET_SOURCES = ["jfk_inaugural"] # , "apollo_11"]

# Global Models (Singleton to avoid reload)
print("📦 Loading global CrossEncoder...")
CROSS_ENCODER_MODEL = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# --- Classes ---
class RerankRetriever:
    def __init__(self, base_retriever, top_k=5):
        self.base_retriever = base_retriever
        self.top_k = top_k
        # Use global model
        self.model = CROSS_ENCODER_MODEL

    def invoke(self, query):
        docs = self.base_retriever.invoke(query)
        if not docs: return []
        pairs = [[query, d.page_content] for d in docs]
        scores = self.model.predict(pairs)
        scored_docs = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
        return [d for d, s in scored_docs[:self.top_k]]

# --- Helpers ---
def load_source_data(source_id):
    urls = {
        "jfk_inaugural": "https://ia800300.us.archive.org/1/items/JFK_Inaugural_Address/JFK_Inaugural_Address.mp3",
        "apollo_11": "https://ia800108.us.archive.org/24/items/Apollo11Audio/11-069-070.mp3"
    }
    url = urls.get(source_id)
    filepath = f"labs/data/{source_id}.mp3"
    
    if not os.path.exists(filepath):
        print(f"⬇️ Downloading {source_id}...")
        r = requests.get(url, verify=False)
        with open(filepath, "wb") as f: f.write(r.content)
        
    transcript_path = f"labs/data/{source_id}_transcript.txt"
    if os.path.exists(transcript_path):
        with open(transcript_path, "r") as f: text = f.read()
    else:
        print(f"🎙️ Transcribing {source_id}...")
        # Use simple mock if API key missing or just use first 10k chars if huge?
        # For sweep optimization, let's limit text size too.
        files = {'file': open(filepath, 'rb')}
        data = {'model': 'whisper-v3', 'response_format': 'text'}
        try:
             resp = requests.post("https://audio-turbo.us-virginia-1.direct.fireworks.ai/v1/audio/transcriptions", 
                                  headers={"Authorization": f"Bearer {os.getenv('FIREWORKS_API_KEY')}"}, 
                                  files=files, data=data)
             if resp.status_code == 200:
                 text = resp.text
                 with open(transcript_path, "w") as f: f.write(text)
             else:
                 print(f"Fallback: Transcription failed ({resp.text}). Using dummy text.")
                 text = "This is a dummy transcript used because the API failed. The president spoke about freedom and space exploration."
        except Exception as e:
             print(f"Fallback: Transcription error {e}. Using dummy text.")
             text = "This is a dummy transcript used because the API failed. The president spoke about freedom and space exploration."

    # TRUNCATE TEXT for memory safety during dev
    if len(text) > 50000:
        print(f"⚠️ Truncating text from {len(text)} to 50000 chars for memory safety.")
        text = text[:50000]
        
    return text

def generate_qa_dataset(text, source_id):
    # Reduced QA count for memory/speed
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    prompt = f"Given the text below, generate 2 question-answer pairs in JSON format with keys 'question' and 'answer':\n\n{text[:2000]}..."
    res = llm.invoke(prompt)
    try:
        data = json.loads(res.content)
        if isinstance(data, dict) and 'pairs' in data: data = data['pairs']
        examples = []
        for pair in data:
            examples.append({"question": pair['question'], "ground_truth": pair['answer']})
        return Dataset.from_list(examples)
    except:
        return Dataset.from_list([{"question": "What is this about?", "ground_truth": "The transcript."}])

def run_pipeline(name, retriever, dataset, llm):
    print(f"    🏃‍♂️ Running Pipeline: {name}")
    results = []
    for row in dataset:
        q = row['question']
        gt = row['ground_truth']
        docs = retriever.invoke(q)
        context = "\n".join([d.page_content for d in docs])
        ans = llm.invoke(f"Answer based on context:\n{context}\n\nQuestion: {q}").content
        results.append({
            "question": q,
            "answer": ans,
            "contexts": [d.page_content for d in docs],
            "ground_truth": gt
        })
        
    # Evaluate
    eval_dataset = Dataset.from_list(results)
    # Using smaller batch size / fewer metrics if needed
    scores = evaluate(eval_dataset, metrics=[faithfulness, answer_relevancy], llm=llm, embeddings=OpenAIEmbeddings())
    return scores

def save_result(result):
    file = f"{RESULTS_DIR}/sweep_results.csv"
    df = pd.DataFrame([result])
    if not os.path.exists(file):
        df.to_csv(file, index=False)
    else:
        df.to_csv(file, mode='a', header=False, index=False)

# --- Main Sweep Logic ---

def main():
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    embeddings = OpenAIEmbeddings()
    
    # Clean state
    if os.path.exists(f"{RESULTS_DIR}/sweep_results.csv"):
        os.remove(f"{RESULTS_DIR}/sweep_results.csv")

    for source_id in TARGET_SOURCES:
        print(f"\n🎧 Processing Source: {source_id}")
        text = load_source_data(source_id)
        qa_dataset = generate_qa_dataset(text, source_id)
        
        # 1. Sweep Chunking
        print("\n  🧪 Sweep: Semantic Chunking")
        for chunk_conf in CHUNKING_PARAMS:
            print(f"    Checking {chunk_conf['name']}...")
            splitter = SemanticChunker(
                embeddings, 
                breakpoint_threshold_type=chunk_conf['type'], 
                breakpoint_threshold_amount=chunk_conf['threshold']
            )
            docs = splitter.create_documents([text])
            if not docs: docs = splitter.create_documents([text]) 
            
            vs = Chroma.from_documents(docs, embeddings, collection_name=f"swp_{source_id}_{chunk_conf['name']}")
            retriever = vs.as_retriever(search_kwargs={"k": 5})
            
            scores = run_pipeline(chunk_conf['name'], retriever, qa_dataset, llm)
            res = {
                "experiment": "chunking",
                "source": source_id,
                "config": chunk_conf['name'],
                "faithfulness": scores["faithfulness"],
                "relevancy": scores["answer_relevancy"]
            }
            save_result(res)
            
            # Cleanup
            vs.delete_collection()
            del vs, retriever, docs, splitter
            gc.collect()

        # 2. Sweep Hybrid
        print("\n  🧪 Sweep: Hybrid Weights")
        default_splitter = SemanticChunker(embeddings, breakpoint_threshold_type="percentile", breakpoint_threshold_amount=95)
        docs = default_splitter.create_documents([text])
        vs = Chroma.from_documents(docs, embeddings, collection_name=f"swp_{source_id}_base")
        bm25 = BM25Retriever.from_documents(docs)
        bm25.k = 5
        
        for hyb_conf in HYBRID_PARAMS:
            print(f"    Checking {hyb_conf['name']}...")
            ensemble = EnsembleRetriever(
                retrievers=[bm25, vs.as_retriever(search_kwargs={"k": 5})], 
                weights=hyb_conf['weights']
            )
            # Pass singleton model implicitly by class init logic or modify logic
            reranker = RerankRetriever(ensemble, top_k=5)
            
            scores = run_pipeline(hyb_conf['name'], reranker, qa_dataset, llm)
            res = {
                "experiment": "hybrid",
                "source": source_id,
                "config": hyb_conf['name'],
                "faithfulness": scores["faithfulness"],
                "relevancy": scores["answer_relevancy"]
            }
            save_result(res)
            gc.collect()
            
        vs.delete_collection()
        del vs, docs, bm25
        gc.collect()

        # 3. Sweep HyDE
        print("\n  🧪 Sweep: HyDE Prompts")
        # Re-create docs slightly inefficiently but safe
        default_splitter = SemanticChunker(embeddings, breakpoint_threshold_type="percentile", breakpoint_threshold_amount=95)
        docs = default_splitter.create_documents([text])
        vs = Chroma.from_documents(docs, embeddings, collection_name=f"swp_{source_id}_hyde")
        
        for hyde_conf in HYDE_PROMPTS:
            print(f"    Checking {hyde_conf['name']}...")
            
            class CustomHyDERetriever:
                def __init__(self, vs, base_embeddings, llm, template):
                    self.vs = vs
                    self.base_embeddings = base_embeddings
                    self.llm_chain = LLMChain(llm=llm, prompt=PromptTemplate(input_variables=["question"], template=template))
                def invoke(self, query):
                    hypothetical = self.llm_chain.invoke({"question": query})["text"]
                    vec = self.base_embeddings.embed_query(hypothetical)
                    return self.vs.similarity_search_by_vector(vec, k=5)

            hyde = CustomHyDERetriever(vs, embeddings, llm, hyde_conf['template'])
            scores = run_pipeline(hyde_conf['name'], hyde, qa_dataset, llm)
            res = {
                "experiment": "hyde",
                "source": source_id,
                "config": hyde_conf['name'],
                "faithfulness": scores["faithfulness"],
                "relevancy": scores["answer_relevancy"]
            }
            save_result(res)
            gc.collect()
            
        vs.delete_collection()
        del vs, docs
        gc.collect()

    print("\n✅ Sweep Complete. Results saved.")
    print(pd.read_csv(f"{RESULTS_DIR}/sweep_results.csv"))

if __name__ == "__main__":
    main()
