import { FileText, Book, Code, Zap, ExternalLink, ChevronRight } from "lucide-react";
import { cn } from "@/lib/utils";

const docSections = [
  {
    icon: Zap,
    title: "Quick Start",
    description: "Get up and running in minutes",
    links: [
      { title: "Installation", href: "#" },
      { title: "Authentication", href: "#" },
      { title: "Your First Query", href: "#" },
    ],
  },
  {
    icon: Code,
    title: "SDK Reference",
    description: "Complete API documentation",
    links: [
      { title: "Python SDK", href: "#" },
      { title: "JavaScript SDK", href: "#" },
      { title: "REST API", href: "#" },
    ],
  },
  {
    icon: Book,
    title: "Guides",
    description: "In-depth tutorials and examples",
    links: [
      { title: "Audio Processing", href: "#" },
      { title: "Semantic Search", href: "#" },
      { title: "Webhooks", href: "#" },
    ],
  },
  {
    icon: FileText,
    title: "Resources",
    description: "Additional learning materials",
    links: [
      { title: "Best Practices", href: "#" },
      { title: "FAQs", href: "#" },
      { title: "Changelog", href: "#" },
    ],
  },
];

const Docs = () => {
  return (
    <div className="max-w-5xl mx-auto space-y-6">
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold tracking-tight text-foreground mb-1">Documentation</h1>
        <p className="text-muted-foreground">Everything you need to integrate Epist into your application.</p>
      </div>

      {/* Quick Links Banner */}
      <div className="p-6 rounded-2xl bg-gradient-to-br from-primary/10 via-card/50 to-card/50 backdrop-blur-xl border border-primary/20">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h2 className="text-lg font-semibold text-foreground mb-1">New to Epist?</h2>
            <p className="text-sm text-muted-foreground">Start with our quickstart guide to learn the basics.</p>
          </div>
          <a
            href="#"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-primary text-primary-foreground text-sm font-medium hover:bg-primary/90 transition-colors"
          >
            Get Started
            <ExternalLink className="w-4 h-4" />
          </a>
        </div>
      </div>

      {/* Documentation Sections */}
      <div className="grid sm:grid-cols-2 gap-6">
        {docSections.map((section) => (
          <div
            key={section.title}
            className="p-6 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50 hover:border-border transition-all group"
          >
            <div className="flex items-start gap-4 mb-4">
              <div className="p-3 rounded-xl bg-primary/10 border border-primary/20 group-hover:bg-primary/20 transition-colors">
                <section.icon className="w-5 h-5 text-primary" />
              </div>
              <div>
                <h3 className="text-base font-semibold text-foreground mb-1">{section.title}</h3>
                <p className="text-sm text-muted-foreground">{section.description}</p>
              </div>
            </div>

            <div className="space-y-2 pl-[52px]">
              {section.links.map((link) => (
                <a
                  key={link.title}
                  href={link.href}
                  className={cn(
                    "flex items-center justify-between py-2 px-3 -mx-3 rounded-lg",
                    "text-sm text-muted-foreground hover:text-foreground hover:bg-muted/50 transition-colors"
                  )}
                >
                  {link.title}
                  <ChevronRight className="w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity" />
                </a>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Code Example */}
      <div className="p-6 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50">
        <h3 className="text-base font-semibold text-foreground mb-4">Quick Example</h3>
        <div className="rounded-xl bg-background border border-border overflow-hidden">
          <div className="flex items-center justify-between px-4 py-2 border-b border-border bg-muted/30">
            <span className="text-xs font-mono text-muted-foreground">main.py</span>
            <button className="text-xs text-muted-foreground hover:text-foreground transition-colors">
              Copy
            </button>
          </div>
          <pre className="p-4 text-sm font-mono text-muted-foreground overflow-x-auto">
            <code>{`import epist

client = epist.Client()

# Upload and index audio
audio = client.upload("./meeting.mp3")
index = client.index.create([audio.id])

# Query with natural language
result = index.query("What decisions were made?")
print(result.text)
# >> "The team decided to..."

print(result.citations)
# >> [{"start": 124.5, "end": 138.2}]`}</code>
          </pre>
        </div>
      </div>
    </div>
  );
};

export default Docs;
