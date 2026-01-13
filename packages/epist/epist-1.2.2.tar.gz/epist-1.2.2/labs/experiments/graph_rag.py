import os
import json
import pandas as pd
import networkx as nx
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
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

class SimpleGraphRAG:
    def __init__(self, documents):
        self.llm = ChatOpenAI(temperature=0, model="gpt-4o")
        self.transformer = LLMGraphTransformer(llm=self.llm)
        self.graph = nx.Graph()
        self.documents = documents
        self.build_graph()

    def build_graph(self):
        print("Extracting Graph Entities & Relationships (this may take a while)...")
        graph_documents = self.transformer.convert_to_graph_documents(self.documents)
        
        print(f"Extracted {len(graph_documents)} graph documents.")
        
        for doc in graph_documents:
            for node in doc.nodes:
                self.graph.add_node(node.id, type=node.type)
            for edge in doc.relationships:
                self.graph.add_edge(edge.source.id, edge.target.id, relation=edge.type)
                
        print(f"Graph Built: {self.graph.number_of_nodes()} nodes, {self.graph.number_of_edges()} edges.")

    def retrieve(self, query):
        # 1. Extract entities from query
        # Simple heuristic: ask LLM to extract entities from query
        prompt = f"Extract the main entities (people, places, concepts) from this query as a comma-separated list: {query}"
        response = self.llm.invoke(prompt)
        entities = [e.strip() for e in response.content.split(",")]
        
        print(f"Query Entities: {entities}")
        
        # 2. Find neighbors in graph
        relevant_context = []
        for entity in entities:
            # Fuzzy match or exact match
            # For simplicity, we check if entity is in graph
            matches = [n for n in self.graph.nodes if entity.lower() in n.lower()]
            
            for match in matches:
                neighbors = list(self.graph.neighbors(match))
                for neighbor in neighbors:
                    relation = self.graph.get_edge_data(match, neighbor)['relation']
                    # Construct a sentence
                    fact = f"{match} {relation} {neighbor}"
                    relevant_context.append(fact)
                    
        # If no graph matches, fallback to empty (or vector in a real hybrid system)
        return list(set(relevant_context))

def run_experiment():
    # Load Data
    loader = TextLoader(TRANSCRIPT_PATH)
    documents = loader.load()
    
    # Limit text for graph extraction cost/time (JFK speech is short enough)
    
    with open(DATASET_PATH) as f:
        golden_data = json.load(f)
        
    # Build GraphRAG
    rag = SimpleGraphRAG(documents)
    
    # Run Pipeline
    print("\n--- Running Pipeline: GraphRAG ---")
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    
    results = []
    for item in golden_data:
        question = item["user_input"]
        ground_truth = item["reference"]
        
        # Retrieve
        facts = rag.retrieve(question)
        context_text = "\n".join(facts)
        
        if not context_text:
            context_text = "No relevant graph connections found."
            
        contexts = [context_text]
        
        # Generate
        prompt = f"Answer based on these facts:\n{context_text}\n\nQuestion: {question}"
        response = llm.invoke(prompt)
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
    
    print("Evaluating GraphRAG with RAGAS...")
    scores = evaluate(
        rag_dataset,
        metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
        llm=ChatOpenAI(model="gpt-4o")
    )
    
    final_scores = scores.to_pandas().select_dtypes(include=['number']).mean().to_dict()
    print(f"GraphRAG Scores: {final_scores}")
    
    # Save Results
    with open(f"{RESULTS_DIR}/graph_rag_results.json", "w") as f:
        json.dump(final_scores, f, indent=2)
        
    print("Experiment Complete.")

if __name__ == "__main__":
    run_experiment()
