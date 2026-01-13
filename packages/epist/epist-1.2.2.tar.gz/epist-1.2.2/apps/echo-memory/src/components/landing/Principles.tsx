import { motion } from "framer-motion";
import { Waves, Search, Clock, ArrowRight } from "lucide-react";

const principles = [
  {
    icon: Waves,
    title: "Audio-Aware Segmentation",
    description:
      "Speech doesn't have paragraphs. We use prosody, silence detection, and speaker turns to chunk data semantically before embedding.",
  },
  {
    icon: Search,
    title: "Semantic Memory",
    description:
      'Meaning survives paraphrasing. Search for "money concerns" and Epist retrieves "budgetary constraints" automatically.',
  },
  {
    icon: Clock,
    title: "Time-Respecting Retrieval",
    description:
      'Answers always come with "when." We maintain a strict chronological graph to understand the order of events.',
  },
];

const Principles = () => {
  return (
    <section
      id="principles"
      className="py-24 md:py-32 px-6 bg-gradient-to-b from-secondary/10 to-transparent border-y border-border/50"
    >
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-end mb-12 md:mb-16 gap-6">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-3xl md:text-4xl font-bold tracking-tight max-w-lg text-balance"
          >
            Designed for the messy reality of human speech.
          </motion.h2>
          <motion.a
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            href="#"
            className="text-sm text-primary hover:text-indigo-300 font-medium flex items-center gap-2 group transition-colors"
          >
            Read the research
            <ArrowRight size={14} className="transition-transform group-hover:translate-x-1" />
          </motion.a>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {principles.map((principle, index) => (
            <motion.div
              key={principle.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-50px" }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="glass-hover p-8 rounded-2xl group cursor-default"
            >
              <div className="w-12 h-12 bg-secondary/50 rounded-xl flex items-center justify-center mb-6 border border-border/50 group-hover:border-primary/30 group-hover:bg-primary/5 transition-all duration-300 text-muted-foreground group-hover:text-primary">
                <principle.icon size={22} strokeWidth={1.5} />
              </div>
              <h3 className="text-lg font-semibold mb-3 text-foreground">
                {principle.title}
              </h3>
              <p className="text-sm text-muted-foreground leading-relaxed">
                {principle.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Principles;
