import wave

def combine_wavs(files, output_path):
    data = []
    params = None
    
    for f in files:
        with wave.open(f, 'rb') as w:
            if params is None:
                params = w.getparams()
            else:
                # Ensure formats match
                if w.getparams()[:3] != params[:3]:
                    print(f"Warning: Format mismatch in {f}. Skipping.")
                    continue
            
            data.append(w.readframes(w.getnframes()))
            
            # Add 1 second of silence (approx)
            silence_frames = int(params.framerate * 1) # 1 second
            silence = b'\x00' * (silence_frames * params.nchannels * params.sampwidth)
            data.append(silence)
            
    with wave.open(output_path, 'wb') as w:
        w.setparams(params)
        for d in data:
            w.writeframes(d)
            
    print(f"Created {output_path}")

def main():
    files = ["labs/data/male.wav", "labs/data/female.wav", "labs/data/male.wav", "labs/data/female.wav"]
    combine_wavs(files, "labs/data/conversation.wav")

if __name__ == "__main__":
    main()
