import os
import torch
import librosa
import numpy as np
import laion_clap # type: ignore
from transformers import ClapModel, ClapProcessor
import glob
import chromadb
import requests
from chromadb.config import Settings
import ssl

import urllib3

# Disable SSL Verification (Hack for Mac/Corporate Proxy)
ssl._create_default_https_context = ssl._create_unverified_context # type: ignore
urllib3.disable_warnings()

# --- Configuration ---
AUDIO_URL = "https://ia802804.us.archive.org/19/items/WilhelmScreamSample/WilhelmScream.wav"
DATA_DIR = "labs/data/audio_rag"
os.makedirs(DATA_DIR, exist_ok=True)
FILENAME = "wilhelm.wav"
FILEPATH = os.path.join(DATA_DIR, FILENAME)

CHUNK_DURATION = 1.0 
STEP_SIZE = 0.5 

# --- Helpers ---

def download_audio():
    if os.path.exists(FILEPATH):
        print(f"✅ Audio file exists: {FILEPATH}")
        return
    print(f"⬇️ Downloading {FILENAME}...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(AUDIO_URL, headers=headers, stream=True, verify=False)
    with open(FILEPATH, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024*1024):
            f.write(chunk)
    print("✅ Download complete.")

def load_models():
    print("🤖 Loading CLAP model (Transformers)...")
    # Using the standard laion/clap-htsat-unfused model
    model = ClapModel.from_pretrained("laion/clap-htsat-unfused")
    processor = ClapProcessor.from_pretrained("laion/clap-htsat-unfused")
    return model, processor

def chunk_audio_generator(filepath, duration=7.0, step=2.0, max_duration=120):
    """Yields (start_time, end_time, audio_data_resampled_numpy)"""
    print(f"✂️ Chunking audio (max {max_duration}s)...")
    import soundfile as sf
    import subprocess
    
    # Check if MP3 (Handle conversion locally if needed, but we are using WAV now)
    if filepath.endswith('.mp3'):
        # ... (Legacy MP3 code removed for simplicity/robustness)
        raise ValueError("MP3 not supported in this robust mode. Use WAV.")
    else:
        load_path = filepath
        
    # Load WAV (Soundfile works great with WAV)
    y, sample_rate = sf.read(load_path)
    
    # Resample if needed (ffmpeg should have handled it, but double check)
    # If using soundfile, y is numpy array
    
    # Trim to max_duration
    max_samples = int(max_duration * sample_rate)
    if len(y) > max_samples:
        y = y[:max_samples]
        
    total_samples = len(y)
    chunk_samples = int(duration * sample_rate)
    step_samples = int(step * sample_rate)
    
    for start in range(0, total_samples - chunk_samples, step_samples):
        end = start + chunk_samples
        chunk = y[start:end]
        yield start / sample_rate, end / sample_rate, chunk

# --- Main ---

def main():
    download_audio()
    
    # Force CPU to avoid OOM on MPS
    device = "cpu"
    print(f"💻 Using device: {device} (CPU forced to avoid OOM)")
    
    model, processor = load_models()
    model.to(device)
    
    # Setup Vector DB
    chroma_client = chromadb.Client(Settings(is_persistent=False))
    collection = chroma_client.create_collection(name="audio_native_rag")
    
    chunk_gen = chunk_audio_generator(FILEPATH, CHUNK_DURATION, STEP_SIZE, max_duration=120) # 2 mins for demo
    
    print("🧠 Embedding audio chunks...")
    
    for start, end, audio in chunk_gen:
        # Processor handles resampling if valid sampling_rate is passed, but we already did 48k
        inputs = processor(audios=[audio], sampling_rate=48000, return_tensors="pt", padding=True)
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        with torch.no_grad():
            # Get audio embeddings
            outputs = model.get_audio_features(**inputs)
        
        embedding = outputs[0].cpu().numpy().tolist()
        
        collection.add(
            embeddings=[embedding],
            metadatas=[{"start": start, "end": end, "text": f"Audio chunk {start}-{end}"}],
            ids=[f"t_{start}"],
            documents=[f"Audio [{start:.1f}-{end:.1f}]"]
        )
        print(f"   Processed {start:.1f}s", end='\r')
        
    print("\n✅ Indexing complete.")
    
    # --- Retrieval Test ---
    queries = [
        "orchestral music", 
        "scary alien noises",
        "dramatic speech",
        "silence", 
        "screaming",
        "applause",
        "jazz music"
    ]
    
    print("\n🔎 --- Audio Test Results ---")
    for q in queries:
        print(f"\nQuery: '{q}'")
        inputs = processor(text=[q], return_tensors="pt", padding=True)
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        with torch.no_grad():
            text_embed = model.get_text_features(**inputs)
            
        text_embed_list = text_embed[0].cpu().numpy().tolist()
        
        results = collection.query(
            query_embeddings=[text_embed_list],
            n_results=1
        )
        
        if results['metadatas'][0]:
            meta = results['metadatas'][0][0]
            dist = results['distances'][0][0]
            print(f"  Result: Time {meta['start']:.1f}s - {meta['end']:.1f}s (Dist: {dist:.4f})")
        else:
            print("  No result.")

if __name__ == "__main__":
    main()
