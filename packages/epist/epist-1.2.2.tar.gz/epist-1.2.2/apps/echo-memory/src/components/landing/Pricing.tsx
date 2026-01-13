import { motion } from "framer-motion";
import { Check, Sparkles } from "lucide-react";

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

        <div className="grid md:grid-cols-2 gap-6">
          {/* Free Tier */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="p-8 rounded-2xl border border-border/50 bg-card/50 text-left hover:border-border transition-all"
          >
            <div className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground mb-2">Sandbox</div>
            <div className="text-4xl font-bold mb-6 text-foreground">$0<span className="text-base font-normal text-muted-foreground">/mo</span></div>
            <ul className="text-sm space-y-3 text-muted-foreground mb-8">
              <li className="flex items-center gap-3"><Check size={16} className="text-zinc-600 flex-shrink-0" /> 5 hours audio processing / mo</li>
              <li className="flex items-center gap-3"><Check size={16} className="text-zinc-600 flex-shrink-0" /> Standard temporal graph</li>
              <li className="flex items-center gap-3"><Check size={16} className="text-zinc-600 flex-shrink-0" /> No credit card required</li>
            </ul>
            <button className="w-full btn-secondary">Start Building</button>
          </motion.div>

          {/* Pro Tier */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="p-8 rounded-2xl border border-primary/20 bg-primary/[0.02] text-left relative overflow-hidden"
          >
            <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-primary/50 to-transparent" />
            <div className="absolute top-6 right-6 badge-primary"><Sparkles size={10} /> Production</div>
            <div className="text-[11px] font-bold uppercase tracking-widest text-primary mb-2">Pro</div>
            <div className="text-4xl font-bold mb-6 text-foreground">$49<span className="text-base font-normal text-muted-foreground">/mo</span></div>
            <ul className="text-sm space-y-3 text-zinc-300 mb-8">
              <li className="flex items-center gap-3"><Check size={16} className="text-primary flex-shrink-0" /> 50 hours included + usage billing</li>
              <li className="flex items-center gap-3"><Check size={16} className="text-primary flex-shrink-0" /> High-priority reasoning engine</li>
              <li className="flex items-center gap-3"><Check size={16} className="text-primary flex-shrink-0" /> Shared workspace seats</li>
            </ul>
            <button className="w-full btn-primary">Select Pro</button>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default Pricing;
