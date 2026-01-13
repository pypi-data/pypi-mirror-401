import { Github, FileText, Shield, Lock, Newspaper } from "lucide-react";
import Link from "next/link";

const footerLinks = [
  { label: "Documentation", href: "/docs", icon: FileText, isRoute: true },
  { label: "Blog", href: "/blog", icon: Newspaper, isRoute: true },
  { label: "GitHub", href: "https://github.com/Seifollahi/epist", icon: Github },
  { label: "Terms", href: "/legal/terms-of-service", icon: Shield, isRoute: true },
  { label: "Privacy", href: "/legal/privacy-policy", icon: Lock, isRoute: true },
];

const Footer = () => {
  return (
    <footer className="py-12 px-6 border-t border-border/50 bg-background">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-8">
        <Link href="/" className="flex items-center gap-2.5 group">
          <div className="w-5 h-5 bg-zinc-800 rounded-md flex items-center justify-center text-[10px] text-muted-foreground font-mono font-bold group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
            E
          </div>
          <span className="text-sm font-bold tracking-tight text-foreground">Epist.ai</span>
        </Link>
        <nav className="flex flex-wrap justify-center gap-6 text-[13px] font-medium text-muted-foreground">
          {footerLinks.map((link) =>
            link.isRoute ? (
              <Link key={link.label} href={link.href} className="hover:text-foreground transition-colors">
                {link.label}
              </Link>
            ) : (
              <a key={link.label} href={link.href} className="hover:text-foreground transition-colors">
                {link.label}
              </a>
            )
          )}
        </nav>
        <div className="text-[11px] text-zinc-600 font-mono">
          © 2024 System One Research
        </div>
      </div>
    </footer>
  );
};

export default Footer;
