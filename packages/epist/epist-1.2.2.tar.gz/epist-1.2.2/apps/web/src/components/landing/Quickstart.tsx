"use client";

import { motion } from "framer-motion";
import { Upload, Cpu, Zap, Copy, Check } from "lucide-react";
import { useState } from "react";

const steps = [
  { icon: Upload, title: "Upload", description: "Supports mp3, wav, m4a, flac up to 500MB" },
  { icon: Cpu, title: "Index", description: "Async processing with webhooks" },
  { icon: Zap, title: "Reason", description: "Sub-second query latency" },
];

const codeExample = `import epist

client = epist.Client()

# 1. Ingest & Index (Async)
audio = client.upload("./meeting_recording.mp3")
index = client.index.create([audio.id])

# 2. Query with Citational Reasoning
answer = index.query(
    "What was the verdict on the database migration?"
)

print(answer.text)
# >> "The team agreed to migrate to Postgres..."

print(answer.citations)
# >> [{"start": 842.5, "end": 855.2, "confidence": 0.98}]`;

const Quickstart = () => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(codeExample);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <section id="quickstart" className="py-24 md:py-32 px-6">
      <div className="max-w-6xl mx-auto">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="space-y-8"
          >
            <h2 className="text-3xl md:text-4xl font-bold tracking-tight">
              Three lines to indexed{" "}
              <br className="hidden sm:block" />
              <span className="text-gradient">intelligence.</span>
            </h2>
            <p className="text-muted-foreground leading-relaxed text-lg">
              We abstracted the hard parts. No vector DBs. No chunking logic. No
              RAG plumbing. Just your audio and a question.
            </p>

            <div className="space-y-5 border-l-2 border-border/50 pl-6">
              {steps.map((step, index) => (
                <motion.div
                  key={step.title}
                  initial={{ opacity: 0, x: -10 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                  className="flex items-start gap-4 group"
                >
                  <div className="w-8 h-8 rounded-lg bg-secondary/50 border border-border/50 flex items-center justify-center text-muted-foreground group-hover:text-primary group-hover:border-primary/30 transition-all duration-200 flex-shrink-0">
                    <step.icon size={16} />
                  </div>
                  <div>
                    <span className="text-sm font-semibold text-foreground block mb-0.5">
                      {step.title}
                    </span>
                    <span className="text-sm text-muted-foreground">
                      {step.description}
                    </span>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="relative"
          >
            {/* Glow */}
            <div className="absolute -inset-4 bg-gradient-to-tr from-primary/15 to-purple-500/10 blur-2xl opacity-50" />

            <div className="relative glass rounded-2xl overflow-hidden border border-border/50 shadow-card">
              {/* Header */}
              <div className="bg-background/80 px-4 py-3 flex justify-between items-center border-b border-border/50">
                <div className="flex gap-2">
                  <div className="w-3 h-3 rounded-full bg-zinc-800 hover:bg-red-500/50 transition-colors cursor-pointer" />
                  <div className="w-3 h-3 rounded-full bg-zinc-800 hover:bg-yellow-500/50 transition-colors cursor-pointer" />
                  <div className="w-3 h-3 rounded-full bg-zinc-800 hover:bg-green-500/50 transition-colors cursor-pointer" />
                </div>
                <span className="text-[11px] font-mono text-muted-foreground">
                  main.py
                </span>
                <button
                  onClick={handleCopy}
                  className="p-1.5 rounded-md hover:bg-secondary transition-colors text-muted-foreground hover:text-foreground"
                  title="Copy code"
                >
                  {copied ? <Check size={14} className="text-emerald-500" /> : <Copy size={14} />}
                </button>
              </div>

              {/* Code block */}
              <div className="p-6 md:p-8 font-mono text-[13px] leading-relaxed bg-background/50 overflow-x-auto">
                <pre className="text-muted-foreground">
                  <code>
                    <span className="text-purple-400">import</span>{" "}
                    <span className="text-foreground">epist</span>
                    {"\n\n"}
                    <span className="text-foreground">client</span>{" "}
                    <span className="text-zinc-500">=</span>{" "}
                    <span className="text-foreground">epist</span>
                    <span className="text-zinc-500">.</span>
                    <span className="text-indigo-400">Client</span>
                    <span className="text-zinc-500">()</span>
                    {"\n\n"}
                    <span className="text-zinc-600"># 1. Ingest & Index (Async)</span>
                    {"\n"}
                    <span className="text-foreground">audio</span>{" "}
                    <span className="text-zinc-500">=</span>{" "}
                    <span className="text-foreground">client</span>
                    <span className="text-zinc-500">.</span>
                    <span className="text-indigo-400">upload</span>
                    <span className="text-zinc-500">(</span>
                    <span className="text-emerald-400">&quot;./meeting_recording.mp3&quot;</span>
                    <span className="text-zinc-500">)</span>
                    {"\n"}
                    <span className="text-foreground">index</span>{" "}
                    <span className="text-zinc-500">=</span>{" "}
                    <span className="text-foreground">client</span>
                    <span className="text-zinc-500">.</span>
                    <span className="text-foreground">index</span>
                    <span className="text-zinc-500">.</span>
                    <span className="text-indigo-400">create</span>
                    <span className="text-zinc-500">([</span>
                    <span className="text-foreground">audio</span>
                    <span className="text-zinc-500">.</span>
                    <span className="text-foreground">id</span>
                    <span className="text-zinc-500">])</span>
                    {"\n\n"}
                    <span className="text-zinc-600"># 2. Query with Citational Reasoning</span>
                    {"\n"}
                    <span className="text-foreground">answer</span>{" "}
                    <span className="text-zinc-500">=</span>{" "}
                    <span className="text-foreground">index</span>
                    <span className="text-zinc-500">.</span>
                    <span className="text-indigo-400">query</span>
                    <span className="text-zinc-500">(</span>
                    {"\n"}
                    {"    "}
                    <span className="text-emerald-400">&quot;What was the verdict on the database migration?&quot;</span>
                    {"\n"}
                    <span className="text-zinc-500">)</span>
                    {"\n\n"}
                    <span className="text-purple-400">print</span>
                    <span className="text-zinc-500">(</span>
                    <span className="text-foreground">answer</span>
                    <span className="text-zinc-500">.</span>
                    <span className="text-foreground">text</span>
                    <span className="text-zinc-500">)</span>
                    {"\n"}
                    <span className="text-zinc-600"># {">>"} &quot;The team agreed to migrate to Postgres...&quot;</span>
                    {"\n\n"}
                    <span className="text-purple-400">print</span>
                    <span className="text-zinc-500">(</span>
                    <span className="text-foreground">answer</span>
                    <span className="text-zinc-500">.</span>
                    <span className="text-foreground">citations</span>
                    <span className="text-zinc-500">)</span>
                    {"\n"}
                    <span className="text-zinc-600"># {">>"} [{`{"start": 842.5, "end": 855.2, "confidence": 0.98}`}]</span>
                  </code>
                </pre>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default Quickstart;
