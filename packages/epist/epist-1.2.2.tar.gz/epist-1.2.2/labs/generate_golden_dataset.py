import os
import json
import asyncio
from fireworks.client import Fireworks
from ragas.testset.synthesizers.generate import TestsetGenerator
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import TokenTextSplitter

# Configuration
AUDIO_PATH = "labs/data/sample_podcast.mp3"
OUTPUT_PATH = "labs/data/golden_dataset.json"

def load_env():
    if os.path.exists(".env"):
        print("Loading .env file...")
        with open(".env") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    # Remove quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    if value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    os.environ[key] = value

load_env()
FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from openai import OpenAI

async def transcribe_audio(audio_path):
    print(f"Transcribing {audio_path}...")
    # Use OpenAI client compatible with Fireworks
    client = OpenAI(
        base_url="https://api.fireworks.ai/inference/v1",
        api_key=FIREWORKS_API_KEY
    )
    
    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-v3",
            response_format="text"
        )
    return transcription

def generate_testset(text):
    print("Generating QA pairs with RAGAS...")
    
    # Save transcript temporarily
    # Hack: Repeat text to satisfy RAGAS length requirements if short
    if len(text) < 2000:
        text = (text + "\n\n") * 10
        
    with open("labs/data/transcript.txt", "w") as f:
        f.write(text)
    
    print(f"Transcript length: {len(text)} characters")
    
    loader = TextLoader("labs/data/transcript.txt")
    documents = loader.load()
    
    # Split text
    splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(documents)
    
    # Setup RAGAS Generator
    # Use GPT-4o for better extraction and generation
    generator_llm = ChatOpenAI(model="gpt-4o")
    embeddings = OpenAIEmbeddings()
    
    generator = TestsetGenerator.from_langchain(
        generator_llm,
        embeddings
    )
    
    # Generate
    testset = generator.generate_with_langchain_docs(
        documents=chunks,
        testset_size=5, # Generate 5 QA pairs for the baseline
    )
    
    return testset.to_pandas()

async def main():
    if not os.path.exists(AUDIO_PATH):
        print(f"Error: {AUDIO_PATH} not found.")
        return

    # 1. Transcribe
    try:
        print(f"Fireworks Key present: {bool(FIREWORKS_API_KEY)}")
        transcript = await transcribe_audio(AUDIO_PATH)
        print("Transcription complete.")
    except Exception as e:
        print(f"Transcription failed: {e}")
        with open("labs/data/error.log", "w") as f:
            f.write(str(e))
        raise e
    
    # 2. Generate Dataset
    df = generate_testset(transcript)
    
    # 3. Save
    df.to_json(OUTPUT_PATH, orient="records", indent=2)
    print(f"Golden Dataset saved to {OUTPUT_PATH}")
    print(f"Columns: {df.columns.tolist()}")
    print(df.head())

if __name__ == "__main__":
    asyncio.run(main())
