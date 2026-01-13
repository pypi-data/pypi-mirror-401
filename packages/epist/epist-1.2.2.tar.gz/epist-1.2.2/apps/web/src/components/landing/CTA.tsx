"use client";

import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";
import Link from "next/link";

const CTA = () => {
  return (
    <section className="py-24 md:py-32 px-6">
      <motion.div
        initial={{ opacity: 0, scale: 0.98 }}
        whileInView={{ opacity: 1, scale: 1 }}
        viewport={{ once: true }}
        className="max-w-4xl mx-auto glass rounded-3xl p-10 md:p-16 lg:p-20 text-center relative overflow-hidden border border-border/50"
      >
        <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-primary/40 to-transparent" />
        <div className="absolute -top-32 -left-32 w-64 h-64 bg-primary/10 blur-[100px] rounded-full" />

        <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold tracking-tight mb-6 relative z-10 text-foreground text-balance">
          Not everything important<br className="hidden sm:block" /> is written down.
        </h2>
        <p className="text-lg text-muted-foreground mb-10 max-w-lg mx-auto relative z-10">
          Epist exists to make spoken knowledge durable, searchable, and usable.
        </p>
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 relative z-10">
          <Link href="/dashboard">
            <button className="btn-primary group flex items-center gap-2">
              Get Started Free
              <ArrowRight size={16} className="transition-transform group-hover:translate-x-1" />
            </button>
          </Link>
          <Link href="/blog" className="text-muted-foreground hover:text-foreground text-sm font-medium transition-colors">
            Read the philosophy →
          </Link>
        </div>
      </motion.div>
    </section>
  );
};

export default CTA;
