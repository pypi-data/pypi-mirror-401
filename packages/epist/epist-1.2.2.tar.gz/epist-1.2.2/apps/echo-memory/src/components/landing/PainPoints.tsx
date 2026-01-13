import { motion } from "framer-motion";
import { Search, HelpCircle, Quote, TrendingUp } from "lucide-react";

const painPoints = [
  {
    icon: HelpCircle,
    title: '"It was discussed, but where?"',
    description:
      "Stop scrubbing through 60-minute recordings to find a 10-second decision. Epist indexes the concept, locating the exact moment instantly.",
  },
  {
    icon: Quote,
    title: '"I need exact wording, not summaries."',
    description:
      "LLM summaries hallucinate or gloss over nuance. Epist provides the verbatim transcript segment anchored to the original audio timestamp.",
  },
  {
    icon: TrendingUp,
    title: '"How did our thinking evolve?"',
    description:
      "Reason over chronology. Epist maps the evolution of a project across weeks of meetings, voice notes, and interviews.",
  },
];

const PainPoints = () => {
  return (
    <section className="py-24 md:py-32 px-6 border-t border-border/50 bg-gradient-to-b from-zinc-950/80 to-background">
      <div className="max-w-6xl mx-auto">
        <div className="grid md:grid-cols-3 gap-8 md:gap-6 relative">
          {/* Vertical Dividers */}
          <div className="hidden md:block absolute top-8 bottom-8 left-1/3 w-px bg-gradient-to-b from-transparent via-border/50 to-transparent" />
          <div className="hidden md:block absolute top-8 bottom-8 right-1/3 w-px bg-gradient-to-b from-transparent via-border/50 to-transparent" />

          {painPoints.map((point, index) => (
            <motion.div
              key={point.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-50px" }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="space-y-4 px-4 md:px-6 group"
            >
              <div className="w-10 h-10 rounded-xl bg-secondary/50 border border-border/50 flex items-center justify-center text-muted-foreground group-hover:text-primary group-hover:border-primary/30 group-hover:bg-primary/5 transition-all duration-300">
                <point.icon size={20} />
              </div>
              <h3 className="text-lg font-semibold text-foreground leading-snug">
                {point.title}
              </h3>
              <p className="text-sm text-muted-foreground leading-relaxed">
                {point.description}
              </p>
            </motion.div>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="mt-16 md:mt-20 text-center"
        >
          <p className="text-[13px] text-zinc-500 font-medium tracking-wide uppercase">
            Audio is where decisions hide. Epist makes them retrievable.
          </p>
        </motion.div>
      </div>
    </section>
  );
};

export default PainPoints;
