# 📖 Epist.ai Cookbook

**Recipes and examples for building audio intelligence applications using the [Epist SDK](https://epist.ai).**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

## 💡 What is Epist?

Epist is a **memory layer for spoken knowledge**. 

Unlike standard transcription APIs that just give you a wall of text, Epist creates a **Temporal Graph**. It allows you to **RAG (Reasoning Augmented Generation) over audio files** and get answers cited with exact timestamps.

If you are building podcast search, meeting assistants, or voice-first apps, Epist handles the complexity of "time" for you.

---

## 🚀 Quick Start

1. **Get your API Key** from the [Epist Dashboard](https://epist.ai).

2. **Clone this repo:**
   ```bash
   git clone https://github.com/Seifollahi/epist-cookbook.git
   cd epist-cookbook
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your API Key:**
   ```bash
   # Copy the example env file
   cp .env.example .env
   
   # Edit .env and paste your key: EPIST_API_KEY="your_key_here"
   ```

5. **Run the text example:**
   ```bash
   python 01_basics/hello_world.py
   ```

---

## 📂 Repository Structure

We've organized the recipes by **Use Case** so you can find exactly what you're building.

```text
epist-cookbook/
├── README.md                <-- The "Sales Page" for the code (You are here)
├── requirements.txt         <-- pip install epist python-dotenv
├── data/                    <-- Place your sample.mp3 here
├── 01_basics/
│   └── hello_world.py       <-- The 2-minute "Aha!" moment
├── 02_podcasts/
│   └── deep_search.py       <-- Searching long-form audio with timestamps
└── 03_meetings/
    └── action_items.py      <-- Extracting tasks + who assigned them
```

---

## 👩‍🍳 Recipes

| Recipe | Difficulty | Description |
| :--- | :--- | :--- |
| **[Hello World](01_basics/hello_world.py)** | 🟢 Easy | Upload a file, index it, and ask a question. Start here. |
| **[Podcast Deep Search](02_podcasts/deep_search.py)** | 🟡 Medium | Index a 1-hour episode and find specific topics with timestamp links. |
| **[Meeting Action Items](03_meetings/action_items.py)** | 🟡 Medium | Extract action items and identify who said them. |

---

## 💡 Why use this over LangChain/Vector DBs?

* **No Chunking Logic**: We handle the segmentation based on speaker turns and prosody. You don't need to guess if `chunk_size=1000` is correct.
* **Temporal Awareness**: We know that minute `14:02` happened after minute `05:00`. Standard Vector DBs flatten time concepts; we preserve the graph of the conversation.
* **Citations**: Every answer comes with start and end timestamps (`confidences` included), ready to link to your media player.

## 🤝 Contributing

Got a cool recipe? Open a PR! We love seeing what people build with Audio RAG.
