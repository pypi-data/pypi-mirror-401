"use client";

import { motion } from "framer-motion";
import { MessageSquare, ArrowRight, Play } from "lucide-react";

const Hero = () => {
  return (
    <section className="relative pt-32 md:pt-40 pb-24 px-6 overflow-hidden">
      {/* Ambient Glows */}
      <div className="glow-spot top-[-20%] left-[10%] w-[600px] h-[600px] bg-indigo-500/20 animate-pulse-glow" />
      <div className="glow-spot bottom-[10%] right-[-5%] w-[500px] h-[500px] bg-purple-600/15 animate-pulse-glow delay-1000" />
      <div className="glow-spot top-[40%] left-[50%] w-[300px] h-[300px] bg-indigo-400/10 animate-pulse-glow delay-500" />

      <div className="max-w-7xl mx-auto text-center relative z-10">
        {/* Badge */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.4, 0, 0.2, 1] }}
          className="inline-flex items-center gap-2.5 px-4 py-1.5 rounded-full border border-primary/20 bg-primary/5 text-[12px] font-medium text-indigo-300 mb-8 backdrop-blur-sm"
        >
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75" />
            <span className="relative inline-flex rounded-full h-2 w-2 bg-primary" />
          </span>
          Public Beta: Epist SDK v1.2
        </motion.div>

        {/* Headline */}
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1, ease: [0.4, 0, 0.2, 1] }}
          className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight text-gradient mb-6 md:mb-8 max-w-4xl mx-auto leading-[1.1] text-balance"
        >
          A memory layer for{" "}
          <br className="hidden md:block" />
          spoken knowledge.
        </motion.h1>

        {/* Subheadline */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2, ease: [0.4, 0, 0.2, 1] }}
          className="text-base md:text-lg text-muted-foreground max-w-xl mx-auto mb-10 leading-relaxed font-light"
        >
          Epist turns audio into a searchable, time-aware knowledge base. Reason
          over conversations, meetings, and voice notes—don&apos;t just transcribe
          them.
        </motion.p>

        {/* CTAs */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3, ease: [0.4, 0, 0.2, 1] }}
          className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-20 md:mb-28"
        >
          <a href="#demo" className="w-full sm:w-auto">
            <button className="btn-primary group flex items-center gap-2 w-full justify-center">
              <Play size={16} className="transition-transform group-hover:scale-110" />
              Try with sample audio
              <ArrowRight size={16} className="transition-transform group-hover:translate-x-1" />
            </button>
          </a>
          <a href="#quickstart" className="w-full sm:w-auto">
            <button className="btn-secondary w-full justify-center flex items-center gap-2">
              <span className="font-mono text-primary">{"<>"}</span>
              View Python Quickstart
            </button>
          </a>
        </motion.div>

        {/* Hero Visual: Temporal Graph */}
        <motion.div
          initial={{ opacity: 0, y: 40, scale: 0.98 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.4, ease: [0.4, 0, 0.2, 1] }}
          className="max-w-5xl mx-auto relative group"
        >
          {/* Glow behind card */}
          <div className="absolute -inset-4 bg-gradient-to-r from-indigo-500/20 via-purple-500/10 to-indigo-500/20 rounded-2xl blur-2xl opacity-50 group-hover:opacity-70 transition-opacity duration-700" />

          <div className="relative glass rounded-2xl border border-border/50 p-1.5 overflow-hidden shadow-card">
            {/* Inner glow line at top */}
            <div className="absolute top-0 left-[10%] right-[10%] h-px bg-gradient-to-r from-transparent via-indigo-500/50 to-transparent" />

            <div className="bg-background/80 rounded-xl p-6 md:p-10 text-left">
              {/* Window header */}
              <div className="flex items-center justify-between mb-10 md:mb-12 border-b border-border/50 pb-6">
                <div className="flex items-center gap-3">
                  <div className="flex gap-2">
                    <div className="w-3 h-3 rounded-full bg-red-500/30 border border-red-500/50 hover:bg-red-500/50 transition-colors cursor-pointer" />
                    <div className="w-3 h-3 rounded-full bg-yellow-500/30 border border-yellow-500/50 hover:bg-yellow-500/50 transition-colors cursor-pointer" />
                    <div className="w-3 h-3 rounded-full bg-green-500/30 border border-green-500/50 hover:bg-green-500/50 transition-colors cursor-pointer" />
                  </div>
                  <span className="ml-4 text-xs font-mono text-muted-foreground">
                    epist-temporal-engine
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                  <span className="text-[10px] font-mono text-muted-foreground uppercase tracking-widest">
                    Live Index
                  </span>
                </div>
              </div>

              {/* Timeline Visualization */}
              <div className="relative py-12 md:py-16">
                {/* Axis */}
                <div className="absolute top-1/2 left-0 w-full h-px bg-gradient-to-r from-transparent via-border to-transparent" />

                {/* Nodes */}
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.6 }}
                  className="absolute top-1/2 left-[10%] w-2.5 h-2.5 -mt-[5px] rounded-full bg-zinc-700 group-hover:bg-zinc-500 transition-all duration-500"
                />

                {/* Main highlighted node */}
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.7, type: "spring", stiffness: 200 }}
                  className="absolute top-1/2 left-[35%] w-5 h-5 -mt-[10px] rounded-full bg-primary border-[3px] border-background shadow-glow z-10 cursor-pointer hover:scale-110 transition-transform"
                >
                  {/* Tooltip */}
                  <div className="absolute -top-14 left-1/2 -translate-x-1/2 bg-card/95 backdrop-blur-sm border border-border px-4 py-2 rounded-lg text-[11px] font-mono text-zinc-300 whitespace-nowrap shadow-elevated">
                    <div className="text-[9px] text-primary uppercase tracking-wider mb-0.5">Context</div>
                    Architecture Sync
                    <div className="absolute -bottom-1.5 left-1/2 -translate-x-1/2 w-3 h-3 bg-card border-r border-b border-border rotate-45" />
                  </div>
                  {/* Pulse ring */}
                  <div className="absolute inset-0 rounded-full border-2 border-primary animate-ping opacity-30" />
                </motion.div>

                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.8 }}
                  className="absolute top-1/2 left-[60%] w-2.5 h-2.5 -mt-[5px] rounded-full bg-zinc-700 group-hover:bg-zinc-500 transition-all duration-500 delay-100"
                />
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.9 }}
                  className="absolute top-1/2 left-[85%] w-2.5 h-2.5 -mt-[5px] rounded-full bg-zinc-700 group-hover:bg-zinc-500 transition-all duration-500 delay-200"
                />

                {/* Connection gradient line */}
                <div className="absolute top-1/2 left-[35%] w-[25%] h-0.5 -mt-[1px] bg-gradient-to-r from-primary/80 to-transparent" />
              </div>

              {/* Answer Block */}
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1, duration: 0.5 }}
                className="flex gap-4 items-start bg-primary/[0.04] border border-primary/10 p-5 md:p-6 rounded-xl mt-4"
              >
                <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center text-primary flex-shrink-0">
                  <MessageSquare size={16} />
                </div>
                <div className="min-w-0">
                  <div className="text-[11px] font-bold text-primary uppercase tracking-wider mb-2">
                    Answer Derived from Audio
                  </div>
                  <p className="text-sm md:text-[15px] text-muted-foreground leading-relaxed">
                    The migration timeline was finalized during the{" "}
                    <span className="text-foreground border-b border-dashed border-zinc-600 hover:border-primary hover:text-primary transition-colors cursor-help">
                      Architecture Sync (14:02)
                    </span>
                    . Sarah explicitly requested a two-week buffer for load
                    testing, which David approved at{" "}
                    <span className="text-foreground border-b border-dashed border-zinc-600 hover:border-primary hover:text-primary transition-colors cursor-help">
                      14:05
                    </span>
                    .
                  </p>
                </div>
              </motion.div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default Hero;
