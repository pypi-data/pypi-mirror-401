"use client";

import { motion } from "framer-motion";
import { Command } from "lucide-react";

const Demo = () => {
  return (
    <section id="demo" className="py-24 md:py-32 px-6">
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="mb-12 text-center"
        >
          <h2 className="text-3xl md:text-4xl font-bold tracking-tight mb-4 text-balance">
            Ask real questions of real audio.
          </h2>
          <p className="text-muted-foreground text-lg">
            No keywords. Just natural language reasoning over your data.
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="relative group"
        >
          {/* Glow effect */}
          <div className="absolute -inset-4 bg-gradient-to-r from-indigo-500/10 via-purple-500/5 to-indigo-500/10 rounded-3xl blur-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-700" />

          <div className="relative glass rounded-2xl overflow-hidden border border-border/50 shadow-card">
            {/* Header */}
            <div className="bg-secondary/30 px-6 py-4 flex items-center justify-between border-b border-border/50">
              <div className="flex items-center gap-3">
                <span className="text-xs text-muted-foreground font-mono">
                  workspace:{" "}
                  <span className="text-foreground">product_eng_syncs</span>
                </span>
                <span className="badge-success">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                  Ready
                </span>
              </div>
              <div className="hidden sm:flex items-center gap-2 text-[11px] text-muted-foreground">
                <Command size={12} />
                <span>+ K to search</span>
              </div>
            </div>

            <div className="p-6 md:p-10">
              <div className="space-y-8">
                {/* Query Input */}
                <div className="relative group/input">
                  <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                    <span className="text-primary font-mono text-lg font-bold">
                      ›
                    </span>
                  </div>
                  <input
                    type="text"
                    readOnly
                    value="What concerns were raised about the mobile layout?"
                    className="w-full bg-background/50 border border-border/50 text-foreground text-sm rounded-xl py-4 pl-10 pr-24 focus:outline-none focus:border-primary/50 font-mono cursor-text transition-all duration-200 hover:border-border hover:bg-background/70"
                  />
                  <div className="absolute right-4 top-1/2 -translate-y-1/2 flex items-center gap-2">
                    <kbd className="hidden sm:inline-flex items-center gap-1 text-[10px] text-zinc-500 bg-secondary border border-border px-2 py-1 rounded font-mono">
                      <Command size={10} />K
                    </kbd>
                  </div>
                </div>

                {/* Answer Block */}
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: 0.3 }}
                  className="flex gap-5"
                >
                  <div className="flex flex-col items-center gap-1 flex-shrink-0">
                    <div className="w-7 h-7 rounded-lg bg-primary flex items-center justify-center text-primary-foreground text-[11px] font-bold shadow-glow">
                      E
                    </div>
                    <div className="w-px h-full bg-gradient-to-b from-border to-transparent my-2" />
                  </div>
                  <div className="space-y-5 pb-2 min-w-0">
                    <p className="text-sm md:text-[15px] text-zinc-300 leading-relaxed">
                      The primary concern was the{" "}
                      <span className="text-foreground font-medium bg-primary/10 px-1 rounded">
                        click target size
                      </span>{" "}
                      on smaller devices. Design argued that the current 44px hit
                      area causes mis-clicks in the navigation drawer.
                    </p>
                    <div className="flex flex-wrap gap-2">
                      <SourceButton time="08:24" file="Design Review.mp3" />
                      <SourceButton time="14:02" file="Product Sync.mp3" />
                    </div>
                  </div>
                </motion.div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

const SourceButton = ({ time, file }: { time: string; file: string }) => (
  <button className="flex items-center gap-2.5 px-3.5 py-2 bg-secondary/50 hover:bg-secondary border border-border/50 hover:border-border rounded-lg text-[12px] text-muted-foreground hover:text-foreground transition-all duration-200 group">
    <span className="relative flex h-2 w-2">
      <span className="w-2 h-2 rounded-full bg-emerald-500 group-hover:animate-pulse" />
    </span>
    <span className="font-mono font-medium">{time}</span>
    <span className="text-border">|</span>
    <span className="truncate max-w-[120px]">{file}</span>
  </button>
);

export default Demo;
