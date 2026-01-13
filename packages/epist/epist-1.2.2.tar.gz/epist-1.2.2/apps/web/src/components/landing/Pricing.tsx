"use client";

import { motion } from "framer-motion";
import { Check, Sparkles } from "lucide-react";
import Link from "next/link";

const Pricing = () => {
  return (
    <section id="pricing" className="py-24 md:py-32 px-6">
      <div className="max-w-4xl mx-auto text-center">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-3xl md:text-4xl font-bold mb-4 tracking-tight"
        >
          Start free. Scale with volume.
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="text-muted-foreground mb-12"
        >
          No credit card required to get started.
        </motion.p>

        <div className="grid md:grid-cols-3 gap-6">
          {/* Free Tier */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="p-8 rounded-2xl border border-border/50 bg-card/50 text-left hover:border-border transition-all flex flex-col"
          >
            <div className="mb-auto">
              <div className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground mb-2">Sandbox</div>
              <div className="text-4xl font-bold mb-6 text-foreground">$0<span className="text-base font-normal text-muted-foreground">/mo</span></div>
              <ul className="text-sm space-y-3 text-muted-foreground mb-8">
                <li className="flex items-center gap-3"><Check size={16} className="text-zinc-600 flex-shrink-0" /> 5 hours transcription / mo</li>
                <li className="flex items-center gap-3"><Check size={16} className="text-zinc-600 flex-shrink-0" /> Standard vector search</li>
                <li className="flex items-center gap-3"><Check size={16} className="text-zinc-600 flex-shrink-0" /> No credit card required</li>
              </ul>
            </div>
            <Link href="/dashboard" className="w-full mt-4">
              <button className="w-full btn-secondary">Start Free</button>
            </Link>
          </motion.div>

          {/* Starter Tier */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="p-8 rounded-2xl border border-primary/20 bg-primary/[0.02] text-left hover:border-primary/40 transition-all flex flex-col"
          >
            <div className="mb-auto">
              <div className="text-[11px] font-bold uppercase tracking-widest text-primary mb-2">Starter</div>
              <div className="text-4xl font-bold mb-6 text-foreground">$19<span className="text-base font-normal text-muted-foreground">/mo</span></div>
              <ul className="text-sm space-y-3 text-zinc-300 mb-8">
                <li className="flex items-center gap-3"><Check size={16} className="text-primary flex-shrink-0" /> 20 hours transcription / mo</li>
                <li className="flex items-center gap-3"><Check size={16} className="text-primary flex-shrink-0" /> Basic vector search</li>
                <li className="flex items-center gap-3"><Check size={16} className="text-primary flex-shrink-0" /> API Access</li>
              </ul>
            </div>
            <Link href="/dashboard" className="w-full mt-4">
              <button className="w-full btn-secondary border-primary/20 hover:bg-primary/10">Select Starter</button>
            </Link>
          </motion.div>

          {/* Pro Tier */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="p-8 rounded-2xl border border-purple-500/30 bg-purple-500/[0.03] text-left relative overflow-hidden flex flex-col"
          >
            <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-purple-500/50 to-transparent" />
            <div className="absolute top-6 right-6 badge-primary bg-purple-500/20 text-purple-200 border-purple-500/20"><Sparkles size={10} /> Best Value</div>

            <div className="mb-auto">
              <div className="text-[11px] font-bold uppercase tracking-widest text-purple-400 mb-2">Pro</div>
              <div className="text-4xl font-bold mb-6 text-foreground">$49<span className="text-base font-normal text-muted-foreground">/mo</span></div>
              <ul className="text-sm space-y-3 text-zinc-300 mb-8">
                <li className="flex items-center gap-3"><Check size={16} className="text-purple-400 flex-shrink-0" /> 100 hours transcription / mo</li>
                <li className="flex items-center gap-3"><Check size={16} className="text-purple-400 flex-shrink-0" /> High-priority Reranking</li>
                <li className="flex items-center gap-3"><Check size={16} className="text-purple-400 flex-shrink-0" /> API Access & Shared Seats</li>
              </ul>
            </div>
            <Link href="/dashboard" className="w-full mt-4">
              <button className="w-full btn-primary bg-purple-600 hover:bg-purple-700">Select Pro</button>
            </Link>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default Pricing;
