import urllib.request
import ssl
import os

def download_file(url, output_path):
    print(f"Downloading {url}...")
    try:
        # Create unverified context to avoid SSL errors
        context = ssl._create_unverified_context()
        
        with urllib.request.urlopen(url, context=context) as response, open(output_path, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
            
        print(f"Downloaded to {output_path}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def main():
    os.makedirs("labs/data", exist_ok=True)

    # 1. JFK Speech (Whisper.cpp sample)
    download_file(
        "https://github.com/ggerganov/whisper.cpp/raw/master/samples/jfk.wav",
        "labs/data/sample_podcast.mp3"
    )

    # 2. Male & Female Samples (for synthetic conversation)
    download_file(
        "https://www.signalogic.com/melp/EngSamples/Orig/male.wav",
        "labs/data/male.wav"
    )
    download_file(
        "https://www.signalogic.com/melp/EngSamples/Orig/female.wav",
        "labs/data/female.wav"
    )

if __name__ == "__main__":
    main()
