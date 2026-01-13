import { FileText, MessageCircle, Github, ExternalLink } from "lucide-react";
import { cn } from "@/lib/utils";

const resources = [
    {
        icon: FileText,
        title: "Documentation",
        description: "API reference and guides",
        href: "#",
        color: "text-blue-400",
        bgColor: "bg-blue-500/10",
        borderColor: "border-blue-500/20",
    },
    {
        icon: MessageCircle,
        title: "Discord Community",
        description: "Get help from the community",
        href: "#",
        color: "text-indigo-400",
        bgColor: "bg-indigo-500/10",
        borderColor: "border-indigo-500/20",
    },
    {
        icon: Github,
        title: "GitHub Repo",
        description: "Star us & contribute",
        href: "#",
        color: "text-zinc-400",
        bgColor: "bg-zinc-500/10",
        borderColor: "border-zinc-500/20",
    },
];

const SupportCard = () => {
    return (
        <div className="p-6 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50">
            <h3 className="text-base font-semibold text-foreground mb-4">Learn & Support</h3>

            <div className="grid sm:grid-cols-3 gap-4">
                {resources.map((resource) => (
                    <a
                        key={resource.title}
                        href={resource.href}
                        target="_blank"
                        rel="noopener noreferrer"
                        className={cn(
                            "group flex flex-col p-4 rounded-xl border transition-all duration-200",
                            "bg-background/50 hover:bg-card",
                            "border-border/50 hover:border-border"
                        )}
                    >
                        <div className="flex items-center justify-between mb-3">
                            <div className={cn("p-2 rounded-lg", resource.bgColor, resource.borderColor, "border")}>
                                <resource.icon className={cn("w-4 h-4", resource.color)} />
                            </div>
                            <ExternalLink className="w-3 h-3 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
                        </div>
                        <h4 className="text-sm font-medium text-foreground mb-1">{resource.title}</h4>
                        <p className="text-xs text-muted-foreground">{resource.description}</p>
                    </a>
                ))}
            </div>
        </div>
    );
};

export default SupportCard;
