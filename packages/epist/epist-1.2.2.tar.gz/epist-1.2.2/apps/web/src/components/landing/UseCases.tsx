"use client";

import { motion } from "framer-motion";
import { Building2, Mic, Users, Headphones } from "lucide-react";

const useCases = [
  { icon: Building2, title: "Meeting Archives", description: "Searchable company memory" },
  { icon: Mic, title: "Podcast Intelligence", description: "Deep discovery & show notes" },
  { icon: Users, title: "Research Memory", description: "Synthesize user interviews" },
  { icon: Headphones, title: "Internal Tools", description: "Support call QA & Compliance" },
];

const UseCases = () => {
  return (
    <section className="py-20 md:py-24 px-6 border-t border-border/50 bg-gradient-to-b from-zinc-950/50 to-background">
      <div className="max-w-7xl mx-auto">
        <motion.h2
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="text-xs font-semibold text-muted-foreground uppercase tracking-widest text-center mb-10"
        >
          Built as infrastructure. Used everywhere.
        </motion.h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {useCases.map((useCase, index) => (
            <motion.div
              key={useCase.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: index * 0.1 }}
              className="card-interactive p-6 rounded-xl text-center group"
            >
              <div className="w-10 h-10 mx-auto mb-4 rounded-lg bg-secondary/50 border border-border/50 flex items-center justify-center text-muted-foreground group-hover:text-primary group-hover:border-primary/30 transition-all">
                <useCase.icon size={20} />
              </div>
              <div className="text-foreground font-semibold mb-1">{useCase.title}</div>
              <p className="text-xs text-muted-foreground">{useCase.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default UseCases;
