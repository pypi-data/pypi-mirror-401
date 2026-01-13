import os

# Set Project Name
os.environ["PHOENIX_PROJECT_NAME"] = "grand_benchmark"

# Instrument BEFORE other imports
from openinference.instrumentation.openai import OpenAIInstrumentor
from openinference.instrumentation.langchain import LangChainInstrumentor
import phoenix as px

# Explicit OpenTelemetry Setup
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from phoenix.otel import register

# Launch Phoenix
session = px.launch_app()
if session is None:
    raise RuntimeError("Failed to launch Phoenix app")
print(f"🚀 Phoenix UI: {session.url}")

# Register Tracer Provider with Phoenix
tracer_provider = register(
    project_name="grand_benchmark",
    endpoint="http://localhost:6006/v1/traces"
)

# Instrument with specific provider
OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)
LangChainInstrumentor().instrument(tracer_provider=tracer_provider)

import json
import time
import requests
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import openai
from langchain_community.vectorstores import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_classic.chains.hyde.base import HypotheticalDocumentEmbedder
from langchain_classic.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from sentence_transformers import CrossEncoder
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from ragas.testset.synthesizers.generate import TestsetGenerator
from datasets import Dataset

SOURCES_PATH = "labs/data/sources.json"
DATA_DIR = "labs/data/grand_benchmark"
RESULTS_DIR = "labs/results/grand_benchmark"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# Load env
load_dotenv()

FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not FIREWORKS_API_KEY:
    print("❌ Error: FIREWORKS_API_KEY not found in environment.")
    # Fallback or exit?
    # For now, let's try to continue but it will crash later if used.
    
if not OPENAI_API_KEY:
    print("❌ Error: OPENAI_API_KEY not found in environment.")

fw_client = openai.OpenAI(
    base_url="https://api.fireworks.ai/inference/v1",
    api_key=FIREWORKS_API_KEY or "dummy_key_to_prevent_init_error", # Prevent immediate crash if missing, but will fail on use
)

# --- Classes ---

class RerankRetriever:
    def __init__(self, base_retriever, model_name="cross-encoder/ms-marco-MiniLM-L-6-v2", top_k=5):
        self.base_retriever = base_retriever
        self.model = CrossEncoder(model_name)
        self.top_k = top_k

    def invoke(self, query):
        docs = self.base_retriever.invoke(query)
        if not docs: return []
        pairs = [[query, d.page_content] for d in docs]
        scores = self.model.predict(pairs)
        scored_docs = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
        return [d for d, s in scored_docs[:self.top_k]]

# --- Helpers ---

def download_audio(url, filepath):
    if os.path.exists(filepath): return True
    try:
        print(f"  - Downloading {url}...")
        response = requests.get(url, stream=True, verify=False, allow_redirects=True)
        if 'text/html' in response.headers.get('Content-Type', ''):
            print("    - Error: HTML returned.")
            return False
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"    - Download failed: {e}")
        return False

def transcribe_audio(filepath):
    txt_path = filepath.replace(".mp3", ".txt").replace(".wav", ".txt").replace(".webm", ".txt")
    if os.path.exists(txt_path):
        with open(txt_path, 'r') as f: return f.read()
    print("  - Transcribing...")
    try:
        with open(filepath, "rb") as audio_file:
            transcription = fw_client.audio.transcriptions.create(
                model="whisper-v3", file=audio_file, response_format="text"
            )
        text = transcription
        if len(text) < 500: text = (text + "\n") * 5
        with open(txt_path, "w") as f: f.write(text)
        return text
    except Exception as e:
        print(f"    - Transcription failed: {e}")
        return None

def generate_qa(text, source_id):
    qa_path = f"{DATA_DIR}/{source_id}_qa.json"
    if os.path.exists(qa_path):
        with open(qa_path, 'r') as f: return json.load(f)
    print("  - Generating QA...")
    generator_llm = ChatOpenAI(model="gpt-4o")
    embeddings = OpenAIEmbeddings()
    generator = TestsetGenerator.from_langchain(generator_llm, embeddings)
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.create_documents([text], metadatas=[{"filename": source_id}])
    
    try:
        testset = generator.generate_with_langchain_docs(chunks, testset_size=3, raise_exceptions=False)
        df = testset.to_pandas()
        dataset = []
        for _, row in df.iterrows():
            q_col = "question" if "question" in df.columns else "user_input"
            gt_col = "ground_truth" if "ground_truth" in df.columns else "reference"
            dataset.append({"user_input": row[q_col], "reference": row[gt_col]})
        with open(qa_path, "w") as f: json.dump(dataset, f, indent=2)
        return dataset
    except Exception as e:
        print(f"    - QA Gen failed: {e}")
        return []

# --- Pipelines ---

def run_pipeline(name, retriever, qa_dataset, llm):
    results = []
    for item in qa_dataset:
        question = item["user_input"]
        ground_truth = item["reference"]
        try:
            # HyDE needs special handling if it's just a vectorstore, but here we pass a retriever
            docs = retriever.invoke(question)
            contexts = [d.page_content for d in docs]
            context_text = "\n\n".join(contexts)
            prompt = f"Answer based on context:\n{context_text}\n\nQuestion: {question}"
            response = llm.invoke(prompt)
            results.append({
                "question": question, "answer": response.content,
                "contexts": contexts, "ground_truth": ground_truth
            })
        except Exception as e:
            print(f"    - Error in {name}: {e}")
            
    if not results: return None
    
    df = pd.DataFrame(results)
    rag_dataset = Dataset.from_pandas(df)
    scores = evaluate(rag_dataset, metrics=[faithfulness, answer_relevancy], llm=ChatOpenAI(model="gpt-4o"))
    return scores.to_pandas().select_dtypes(include=['number']).mean().to_dict()

# --- Main ---

def main():
    with open(SOURCES_PATH, 'r') as f: sources = json.load(f)
    overall_results = {}
    
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    embeddings = OpenAIEmbeddings()
    
    # DEBUG: Only run first source
    # sources = sources[:1]
    
    for i, source in enumerate(sources):
        print(f"\n[{i+1}/{len(sources)}] Processing: {source['description']}")
        source_id = source['id']
        ext = source['url'].split('.')[-1]
        audio_path = f"{DATA_DIR}/{source_id}.{ext}"
        
        if not download_audio(source['url'], audio_path): continue
        text = transcribe_audio(audio_path)
        if not text: continue
        qa_dataset = generate_qa(text, source_id)
        if not qa_dataset: continue
        
        results = {}
        
        # 1. Baseline (Recursive + Vector)
        print("  - Running Baseline...")
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = splitter.create_documents([text])
        vs = Chroma.from_documents(docs, embeddings, collection_name=f"base_{source_id}")
        results["Baseline"] = run_pipeline("Baseline", vs.as_retriever(search_kwargs={"k": 5}), qa_dataset, llm)
        vs.delete_collection()
        
        # 2. Semantic (Semantic + Vector)
        print("  - Running Semantic...")
        splitter = SemanticChunker(embeddings)
        docs = splitter.create_documents([text])
        if not docs: docs = splitter.create_documents([text]) # Fallback
        vs = Chroma.from_documents(docs, embeddings, collection_name=f"sem_{source_id}")
        results["Semantic"] = run_pipeline("Semantic", vs.as_retriever(search_kwargs={"k": 5}), qa_dataset, llm)
        
        # 3. Hybrid + Rerank (Semantic + Hybrid + Rerank)
        print("  - Running Hybrid+Rerank...")
        bm25 = BM25Retriever.from_documents(docs)
        bm25.k = 5
        ensemble = EnsembleRetriever(retrievers=[bm25, vs.as_retriever(search_kwargs={"k": 5})], weights=[0.5, 0.5])
        reranker = RerankRetriever(ensemble, top_k=5)
        results["HybridRerank"] = run_pipeline("HybridRerank", reranker, qa_dataset, llm)
        
        # 4. HyDE (Semantic + HyDE)
        print("  - Running HyDE...")
        # Manual HyDE logic inside a custom retriever wrapper to fit the interface
        class HyDERetriever:
            def __init__(self, vs, base_embeddings, llm):
                self.vs = vs
                self.base_embeddings = base_embeddings
                self.llm_chain = LLMChain(llm=llm, prompt=PromptTemplate(input_variables=["question"], template="Answer: {question}"))
            def invoke(self, query):
                hypothetical = self.llm_chain.invoke({"question": query})["text"]
                vec = self.base_embeddings.embed_query(hypothetical)
                return self.vs.similarity_search_by_vector(vec, k=5)
                
        hyde = HyDERetriever(vs, embeddings, llm)
        results["HyDE"] = run_pipeline("HyDE", hyde, qa_dataset, llm)
        
        vs.delete_collection()
        
        overall_results[source_id] = {"category": source['category'], "results": results}
        with open(f"{RESULTS_DIR}/grand_results_partial.json", "w") as f: json.dump(overall_results, f, indent=2)
        
    print("\n--- Grand Benchmark Complete ---")
    with open(f"{RESULTS_DIR}/grand_results_final.json", "w") as f: json.dump(overall_results, f, indent=2)
    
    # Debug Traces
    try:
        spans = px.Client().get_spans_dataframe()
        print(f"\n📊 Total Spans Collected: {len(spans)}")
        if len(spans) > 0:
            print("✅ Traces found in memory!")
            spans.to_csv(f"{RESULTS_DIR}/traces_debug.csv")
            print(f"   Saved to {RESULTS_DIR}/traces_debug.csv")
        else:
            print("❌ No traces found in memory.")
    except Exception as e:
        print(f"Error checking traces: {e}")

    print(f"\n🚀 Phoenix UI is still running at: {session.url}")
    print("Press Ctrl+C to stop the server.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping server...")

if __name__ == "__main__":
    main()
