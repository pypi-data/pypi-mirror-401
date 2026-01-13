"use client";

import { Play, Code, Key, MessageSquare, Activity, FileText, Search, Server, BookOpen } from "lucide-react";
import { CodeBlock } from "../CodeBlock";

interface DocsContentProps {
    isDashboard?: boolean;
    examples?: {
        quickstart: { python: string; javascript: string };
        chat: { python: string; javascript: string };
    };
}

const DownloadLink = ({ lang, type }: { lang: 'python' | 'javascript', type: 'quickstart' | 'chat' }) => (
    <a
        href={`/examples/${lang}/${type}.${lang === 'python' ? 'py' : 'js'}`}
        download
        className="text-xs flex items-center gap-1 text-indigo-400 hover:text-indigo-300 transition-colors ml-4"
    >
        <FileText size={12} />
        Download {lang === 'python' ? '.py' : '.js'}
    </a>
);

export function DocsContent({ isDashboard = false, examples }: DocsContentProps) {
    const sections = [
        { id: "introduction", title: "Introduction" },
        { id: "authentication", title: "Authentication" },
        { id: "audio", title: "Audio & Transcription" },
        { id: "search", title: "Semantic Search" },
        { id: "chat", title: "Chat (RAG)" },
        { id: "tutorials", title: "Tutorials" },
        { id: "observability", title: "Observability" },
        { id: "sdks", title: "SDKs & Tools" },
    ];

    const scrollToSection = (id: string) => {
        const element = document.getElementById(id);
        if (element) {
            element.scrollIntoView({ behavior: "smooth" });
        }
    };

    return (
        <div className={`${isDashboard ? 'pt-8' : 'pt-24'} pb-24 min-h-screen bg-slate-950`}>
            <div className="max-w-8xl mx-auto px-6 flex flex-col lg:flex-row gap-16">
                <aside className="lg:w-64 shrink-0 hidden lg:block">
                    <div className="sticky top-32 space-y-10">
                        <div>
                            <h3 className="text-sm font-semibold text-slate-200 mb-4 tracking-wide uppercase">Contents</h3>
                            <nav className="space-y-1 relative border-l border-slate-800 ml-2 pl-4">
                                {sections.map((section) => (
                                    <button
                                        key={section.id}
                                        onClick={() => scrollToSection(section.id)}
                                        className="block text-sm text-slate-400 hover:text-indigo-400 hover:translate-x-1 transition-all text-left w-full py-1.5"
                                    >
                                        {section.title}
                                    </button>
                                ))}
                            </nav>
                        </div>
                    </div>
                </aside>

                <main className="flex-1 max-w-4xl min-w-0">
                    <div className="prose prose-invert prose-slate prose-lg max-w-none 
                        prose-headings:scroll-mt-32 prose-headings:font-bold prose-headings:tracking-tight 
                        prose-h1:text-4xl prose-h1:mb-6 prose-h1:text-white
                        prose-h2:text-2xl prose-h2:mt-16 prose-h2:mb-6 prose-h2:text-slate-100 prose-h2:border-b prose-h2:border-slate-800 prose-h2:pb-4
                        prose-h3:text-xl prose-h3:mt-10 prose-h3:mb-4 prose-h3:text-slate-200
                        prose-p:text-slate-400 prose-p:leading-relaxed prose-p:mb-6
                        prose-strong:text-slate-200 prose-strong:font-semibold
                        prose-code:text-indigo-300 prose-code:bg-indigo-500/10 prose-code:rounded prose-code:px-1.5 prose-code:py-0.5 prose-code:before:content-none prose-code:after:content-none
                        prose-a:text-indigo-400 prose-a:no-underline prose-a:border-b prose-a:border-indigo-500/30 hover:prose-a:border-indigo-500 transition-colors
                        prose-ul:my-6 prose-ul:list-disc prose-ul:pl-6 prose-li:text-slate-400 prose-li:mb-2
                    ">

                        <section id="introduction">
                            <h1>Documentation</h1>
                            <p className="lead text-xl">
                                Welcome to the Epist.ai Developer Hub. Integrate powerful audio intelligence into your applications with our production-ready API.
                            </p>

                            <div className="not-prose grid sm:grid-cols-2 gap-6 my-10">
                                <div className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800 hover:border-indigo-500/50 hover:bg-slate-900 transition-all group cursor-pointer" onClick={() => scrollToSection('audio')}>
                                    <div className="flex items-center gap-3 mb-3">
                                        <div className="p-2 rounded bg-indigo-500/10 text-indigo-400 group-hover:scale-110 transition-transform"><Play size={20} /></div>
                                        <h3 className="font-semibold text-slate-200">Quickstart</h3>
                                    </div>
                                    <p className="text-sm text-slate-400">Transcribe and search your first file in minutes.</p>
                                </div>
                                <div className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800 hover:border-purple-500/50 hover:bg-slate-900 transition-all group cursor-pointer" onClick={() => scrollToSection('sdks')}>
                                    <div className="flex items-center gap-3 mb-3">
                                        <div className="p-2 rounded bg-purple-500/10 text-purple-400 group-hover:scale-110 transition-transform"><Code size={20} /></div>
                                        <h3 className="font-semibold text-slate-200">SDKs & Tools</h3>
                                    </div>
                                    <p className="text-sm text-slate-400">Libraries for Python, Node.js, and MCP.</p>
                                </div>
                            </div>
                        </section>

                        <section id="authentication">
                            <div className="flex items-center gap-3 text-indigo-400 mb-2 mt-16">
                                <Key size={24} />
                                <span className="text-sm font-mono uppercase tracking-wider font-semibold">Security</span>
                            </div>
                            <h2 className="!mt-2 !border-none !pb-0">Authentication & Limits</h2>
                            <p>
                                Authenticate all requests using the <code>X-API-Key</code> header.
                                Secure your keys and manage them in the <a href="/dashboard/api-keys">Dashboard</a>.
                            </p>

                            <div className="not-prose my-6">
                                <CodeBlock
                                    variants={{
                                        bash: `# Example Request - Check API Status
curl -H "X-API-Key: sk_live_..." https://api.epist.ai/api/v1/health`,
                                        python: `# Check API Status
import requests

response = requests.get(
    "https://api.epist.ai/api/v1/health",
    headers={"X-API-Key": "sk_live_..."}
)
print(response.json())`,
                                        javascript: `// Check API Status
const response = await fetch("https://api.epist.ai/api/v1/health", {
    headers: { "X-API-Key": "sk_live_..." }
});
console.log(await response.json());`
                                    }}
                                />
                            </div>

                            <div className="my-8 p-4 rounded-lg bg-amber-500/5 border border-amber-500/20 flex gap-4 items-start not-prose">
                                <div className="text-amber-500 mt-1"><Activity size={20} /></div>
                                <div>
                                    <h4 className="text-amber-200 font-semibold text-sm mb-1">Security Best Practice</h4>
                                    <p className="text-amber-200/70 text-sm m-0">Never reproduce your API keys in client-side code (browsers, mobile apps). Always route requests through your own backend server.</p>
                                </div>
                            </div>

                            <h3>Rate Limits</h3>
                            <div className="not-prose my-6 border border-slate-800 rounded-xl overflow-hidden">
                                <table className="w-full text-left border-collapse">
                                    <thead>
                                        <tr className="bg-slate-900 border-b border-slate-800">
                                            <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wider text-slate-400">Resource</th>
                                            <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wider text-slate-400">Limit per Minute</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-slate-800">
                                        <tr className="hover:bg-slate-900/40 transition-colors bg-slate-950">
                                            <td className="px-6 py-4 font-mono text-sm text-indigo-300">/v1/transcribe</td>
                                            <td className="px-6 py-4 text-sm text-slate-400">10 requests</td>
                                        </tr>
                                        <tr className="hover:bg-slate-900/40 transition-colors bg-slate-950">
                                            <td className="px-6 py-4 font-mono text-sm text-indigo-300">/v1/search</td>
                                            <td className="px-6 py-4 text-sm text-slate-400">100 requests</td>
                                        </tr>
                                        <tr className="hover:bg-slate-900/40 transition-colors bg-slate-950">
                                            <td className="px-6 py-4 font-mono text-sm text-indigo-300">General</td>
                                            <td className="px-6 py-4 text-sm text-slate-400">1,000 requests</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>

                            <h3>Error Codes</h3>
                            <div className="not-prose my-6 border border-slate-800 rounded-xl overflow-hidden">
                                <table className="w-full text-left border-collapse">
                                    <thead>
                                        <tr className="bg-slate-900 border-b border-slate-800">
                                            <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wider text-slate-400">Code</th>
                                            <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wider text-slate-400">Description</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-slate-800">
                                        <tr className="hover:bg-slate-900/40 transition-colors bg-slate-950">
                                            <td className="px-6 py-4 font-mono text-sm text-emerald-400">200 OK</td>
                                            <td className="px-6 py-4 text-sm text-slate-400">Request was successful.</td>
                                        </tr>
                                        <tr className="hover:bg-slate-900/40 transition-colors bg-slate-950">
                                            <td className="px-6 py-4 font-mono text-sm text-amber-400">401 Unauthorized</td>
                                            <td className="px-6 py-4 text-sm text-slate-400">Missing or invalid API key.</td>
                                        </tr>
                                        <tr className="hover:bg-slate-900/40 transition-colors bg-slate-950">
                                            <td className="px-6 py-4 font-mono text-sm text-amber-400">429 Too Many Requests</td>
                                            <td className="px-6 py-4 text-sm text-slate-400">Rate limit exceeded.</td>
                                        </tr>
                                        <tr className="hover:bg-slate-900/40 transition-colors bg-slate-950">
                                            <td className="px-6 py-4 font-mono text-sm text-red-400">500 Internal Error</td>
                                            <td className="px-6 py-4 text-sm text-slate-400">Something went wrong on our end.</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </section>

                        <section id="audio">
                            <div className="flex items-center gap-3 text-pink-400 mb-2 mt-16">
                                <FileText size={24} />
                                <span className="text-sm font-mono uppercase tracking-wider font-semibold">Core API</span>
                            </div>
                            <h2 className="!mt-2 !border-none !pb-0">Audio & Transcription</h2>
                            <p>
                                Upload audio files directly or provide a URL. Our engine automatically handles speaker diarization, timestamps, and semantic indexing.
                            </p>

                            <div className="flex items-center justify-between mb-2 mt-8">
                                <h3>Upload Local File</h3>
                                <div className="flex gap-4">
                                    <DownloadLink lang="javascript" type="quickstart" />
                                    <DownloadLink lang="python" type="quickstart" />
                                </div>
                            </div>
                            <div className="not-prose my-4">
                                <CodeBlock
                                    variants={{
                                        javascript: examples?.quickstart.javascript || `// Loading...`,
                                        python: examples?.quickstart.python || `# Loading...`
                                    }}
                                />
                            </div>

                            <h3>Transcribe Remote URL</h3>
                            <div className="not-prose my-4">
                                <CodeBlock
                                    variants={{
                                        bash: `curl -X POST https://api.epist.ai/api/v1/audio/transcribe_url \\
  -H "X-API-Key: $EPIST_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
    "audio_url": "https://storage.example.com/podcast.mp3",
    "rag_enabled": true,
    "language": "en"
  }'`,
                                        python: `# Transcribe Remote URL
import requests

response = requests.post(
    "https://api.epist.ai/api/v1/audio/transcribe_url",
    headers={
        "X-API-Key": "YOUR_API_KEY",
        "Content-Type": "application/json"
    },
    json={
        "audio_url": "https://storage.example.com/podcast.mp3",
        "rag_enabled": True,
        "language": "en"
    }
)
print(response.json())`,
                                        javascript: `// Transcribe Remote URL
const response = await fetch("https://api.epist.ai/api/v1/audio/transcribe_url", {
    method: "POST",
    headers: {
        "X-API-Key": process.env.EPIST_API_KEY,
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        audio_url: "https://storage.example.com/podcast.mp3",
        rag_enabled: true,
        language: "en"
    })
});`
                                    }}
                                />
                            </div>
                        </section>

                        <section id="search">
                            <div className="flex items-center gap-3 text-emerald-400 mb-2 mt-16">
                                <Search size={24} />
                                <span className="text-sm font-mono uppercase tracking-wider font-semibold">Retrieval</span>
                            </div>
                            <h2 className="!mt-2 !border-none !pb-0">Semantic Search</h2>
                            <p>
                                Perform hybrid search (Dense Vector + Sparse Keyword) across your audio knowledge base.
                                This endpoint is optimized for RAG applications.
                            </p>
                            <div className="not-prose my-4">
                                <CodeBlock
                                    variants={{
                                        javascript: `const results = await fetch('https://api.epist.ai/api/v1/search', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': process.env.EPIST_API_KEY
  },
  body: JSON.stringify({
    query: 'What was the conclusion on the Q3 roadmap?',
    limit: 5,
    rrf_k: 60
  })
});`,
                                        python: `# Semantic Search
import requests

response = requests.post(
    "https://api.epist.ai/api/v1/search",
    headers={
        "X-API-Key": "YOUR_API_KEY",
        "Content-Type": "application/json"
    },
    json={
        "query": "What was the conclusion on the Q3 roadmap?",
        "limit": 5,
        "rrf_k": 60
    }
)
results = response.json()`
                                    }}
                                />
                            </div>
                        </section>

                        <section id="chat">
                            <div className="flex items-center gap-3 text-blue-400 mb-2 mt-16">
                                <MessageSquare size={24} />
                                <span className="text-sm font-mono uppercase tracking-wider font-semibold">Generative</span>
                            </div>
                            <h2 className="!mt-2 !border-none !pb-0">Chat (RAG)</h2>
                            <p>
                                A drop-in replacement for OpenAI Chat Completions that has access to your audio data.
                                Citations are automatically included in the response.
                            </p>

                            <div className="flex items-center justify-between mt-8 mb-2">
                                <span className="font-semibold text-slate-200">Example Code</span>
                                <div className="flex gap-4">
                                    <DownloadLink lang="javascript" type="chat" />
                                    <DownloadLink lang="python" type="chat" />
                                </div>
                            </div>

                            <div className="not-prose my-4">
                                <CodeBlock
                                    variants={{
                                        javascript: examples?.chat.javascript || `// Loading...`,
                                        python: examples?.chat.python || `# Loading...`
                                    }}
                                />
                            </div>

                            <div className="my-6 p-4 rounded-lg bg-indigo-500/5 border border-indigo-500/20 not-prose">
                                <h4 className="text-indigo-300 font-semibold mb-2 flex items-center gap-2">
                                    <Activity size={18} /> Citations Included
                                </h4>
                                <p className="text-indigo-200/70 text-sm m-0">
                                    Each response message includes a <code>citations</code> array. Each citation maps generated text to specific <code>start_time</code> and <code>end_time</code> in the source audio.
                                </p>
                            </div>
                        </section>

                        <section id="tutorials">
                            <div className="flex items-center gap-3 text-cyan-400 mb-2 mt-16">
                                <BookOpen size={24} />
                                <span className="text-sm font-mono uppercase tracking-wider font-semibold">Guides</span>
                            </div>
                            <h2 className="!mt-2 !border-none !pb-0">Tutorial: getting Started</h2>
                            <p>
                                Learn how to integrate powerful audio intelligence into your applications. This tutorial covers file uploads, URL transcription, status polling, and semantic search.
                            </p>

                            <h3>1. Python SDK Integration</h3>
                            <p>The Python SDK is the recommended way to interact with Epist. It handles authentication, error handling, and file uploads automatically.</p>

                            <h4 className="text-slate-200 mt-4 mb-2">Installation</h4>
                            <CodeBlock language="bash" code={`pip install epist`} />

                            <h4 className="text-slate-200 mt-6 mb-2">Complete Example</h4>
                            <p className="mb-4">Create a file named <code>epist_demo.py</code>. This script demonstrates the full lifecycle.</p>
                            <CodeBlock language="python" code={`import os
import time
from epist import Epist

# Initialize the client
# Ensure EPIST_API_KEY is set in your environment or passed explicitly
client = Epist(api_key="YOUR_API_KEY")

def main():
    # --- 1. Upload a Local File ---
    print("\\n[1] Uploading 'interview.mp3'...")
    try:
        # Uploads are synchronous but processing is asynchronous
        upload_res = client.upload_file("interview.mp3")
        task_id = upload_res["id"]
        print(f"Upload successful. Task ID: {task_id}")
    except Exception as e:
        print(f"Upload failed: {e}")
        return

    # --- 2. Poll for Completion ---
    # We must wait for the audio to be processed before we can search it.
    print(f"\\n[2] Polling status for task: {task_id}")
    while True:
        status_res = client.get_status(task_id)
        status = status_res.get("status")
        print(f"Status: {status}")
        
        if status == "completed":
            print("Processing complete!")
            break
        elif status == "failed":
            print(f"Task failed: {status_res.get('error')}")
            return
        
        time.sleep(2)

    # --- 3. Semantic Search ---
    # Now that the file is indexed, we can ask questions about it.
    query = "What was discussed about the roadmap?"
    print(f"\\n[3] Searching knowledge base for: '{query}'")
    
    search_res = client.search(query=query, limit=3)
    
    for idx, item in enumerate(search_res, 1):
        print(f"\\nResult {idx}:")
        print(f"Text: {item.get('text', '')[:150]}...")
        print(f"Score: {item.get('score')}")

if __name__ == "__main__":
    main()`} />

                            <h3>2. Node.js Integration</h3>
                            <p>For Node.js applications, use the <code>epist</code> package to interact with the API.</p>

                            <h4 className="text-slate-200 mt-4 mb-2">Installation</h4>
                            <CodeBlock language="bash" code={`npm install epist`} />

                            <h4 className="text-slate-200 mt-6 mb-2">Complete Example</h4>
                            <CodeBlock language="javascript" code={`const { Epist } = require('epist');

// Initialize the client
const client = new Epist({ 
    apiKey: "YOUR_API_KEY",
    baseUrl: "https://epist-api-staging-920152096400.us-central1.run.app/api/v1"
});

async function main() {
    // --- 1. Transcribe from URL ---
    const audioUrl = "https://storage.googleapis.com/cloud-samples-data/speech/brooklyn_bridge.flac";
    console.log(\`\\n[1] Transcribing URL: \${audioUrl}\`);

    try {
        const urlRes = await client.transcribeUrl(audioUrl, true);
        const taskId = urlRes.id;
        console.log(\`Task started. ID: \${taskId}\`);

        // --- 2. Poll Status ---
        await pollStatus(client, taskId);

        // --- 3. Search ---
        const query = "How old is the bridge?";
        console.log(\`\\n[3] Searching for: '\${query}'\`);
        const searchRes = await client.search(query, 1);
        
        searchRes.forEach(result => {
             console.log(\`\\nAnswer: \${result.text}\`);
        });

    } catch (error) {
        console.error("Error:", error.message);
    }
}

async function pollStatus(client, id) {
    while (true) {
        const res = await client.getStatus(id);
        const status = res.status;
        console.log(\`Status: \${status}\`);
        
        if (status === 'completed' || status === 'failed') break;
        await new Promise(r => setTimeout(r, 2000));
    }
}

main();`} />

                        </section>

                        <section id="observability">
                            <h2 className="text-slate-200 !mt-16 text-3xl font-bold">Observability</h2>
                            <p>Debug and monitor your integrations with built-in tracing.</p>

                            <div className="grid md:grid-cols-2 gap-6 not-prose my-6">
                                <div>
                                    <h4 className="text-slate-200 font-semibold mb-2">Request Logs</h4>
                                    <CodeBlock
                                        variants={{
                                            bash: `curl .../api/v1/logs?limit=50`,
                                            python: `requests.get(".../logs", params={"limit": 50})`,
                                            javascript: `fetch(".../logs?limit=50")`
                                        }}
                                    />
                                </div>
                                <div>
                                    <h4 className="text-slate-200 font-semibold mb-2">Traces</h4>
                                    <CodeBlock
                                        variants={{
                                            bash: `curl .../api/v1/traces/{id}`,
                                            python: `requests.get(f".../traces/{trace_id}")`,
                                            javascript: `fetch(\`.../traces/\${traceId}\`)`
                                        }}
                                    />
                                </div>
                            </div>
                        </section>

                        <section id="sdks">
                            <div className="flex items-center gap-3 text-purple-400 mb-2 mt-16">
                                <Server size={24} />
                                <span className="text-sm font-mono uppercase tracking-wider font-semibold">Ecosystem</span>
                            </div>
                            <h2 className="!mt-2 !border-none !pb-0">SDKs & Tools</h2>

                            <h3 className="!mt-8">MCP Server</h3>
                            <p>Connect your audio data to Claude Desktop using the Model Context Protocol.</p>
                            <div className="not-prose my-4">
                                <CodeBlock language="bash" code={`pip install epist-mcp-server && epist-mcp install`} />
                            </div>

                            <h3 className="!mt-8">Python Client</h3>
                            <div className="not-prose my-4">
                                <CodeBlock language="bash" code={`pip install epist`} />
                            </div>

                            <h3 className="!mt-8">JavaScript Client</h3>
                            <div className="not-prose my-4">
                                <CodeBlock language="bash" code={`npm install epist`} />
                            </div>

                            <h3 className="!mt-8">Embeddable Widget</h3>
                            <p>Add semantic search to any website with a single script tag.</p>
                            <div className="not-prose my-4">
                                <CodeBlock language="html" code={`<script src="https://cdn.epist.ai/widget.js"></script>`} />
                            </div>
                        </section>

                    </div>
                </main>
            </div>
        </div>
    );
}
