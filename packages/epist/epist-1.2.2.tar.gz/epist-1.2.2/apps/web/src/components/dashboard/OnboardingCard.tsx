"use client"

import { useState } from "react";
import { X, Upload, Key, FileText, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const steps = [
    {
        icon: Upload,
        title: "Upload your first audio",
        description: "Start by uploading an audio file to index",
        action: "Upload Audio",
        href: "/dashboard/audio",
    },
    {
        icon: Key,
        title: "Generate an API Key",
        description: "Create credentials to integrate with your app",
        action: "Create Key",
        href: "/dashboard/api-keys",
    },
    {
        icon: FileText,
        title: "Read the Docs",
        description: "Learn how to use the Epist SDK",
        action: "View Docs",
        href: "/docs",
    },
];

const OnboardingCard = () => {
    const [dismissed, setDismissed] = useState(false);
    const [completedSteps, setCompletedSteps] = useState<number[]>([]);

    if (dismissed) return null;

    const toggleStep = (index: number) => {
        setCompletedSteps((prev) =>
            prev.includes(index) ? prev.filter((i) => i !== index) : [...prev, index]
        );
    };

    return (
        <div className="relative p-6 rounded-2xl bg-gradient-to-br from-primary/10 via-card/50 to-card/50 backdrop-blur-xl border border-primary/20">
            {/* Dismiss button */}
            <Button
                variant="ghost"
                size="icon"
                className="absolute top-4 right-4 text-muted-foreground hover:text-foreground"
                onClick={() => setDismissed(true)}
            >
                <X className="w-4 h-4" />
            </Button>

            <div className="mb-6">
                <h3 className="text-lg font-bold text-foreground mb-1">Getting Started</h3>
                <p className="text-sm text-muted-foreground">
                    Complete these steps to get the most out of Epist
                </p>
            </div>

            <div className="grid sm:grid-cols-3 gap-4">
                {steps.map((step, index) => (
                    <div
                        key={index}
                        className={cn(
                            "group relative p-4 rounded-xl border transition-all duration-300 cursor-pointer",
                            completedSteps.includes(index)
                                ? "bg-emerald-500/10 border-emerald-500/30"
                                : "bg-card/50 border-border/50 hover:border-primary/30"
                        )}
                        onClick={() => toggleStep(index)}
                    >
                        <div className="flex items-start gap-3">
                            <div
                                className={cn(
                                    "p-2 rounded-lg transition-colors duration-300",
                                    completedSteps.includes(index)
                                        ? "bg-emerald-500/20"
                                        : "bg-primary/10 group-hover:bg-primary/20"
                                )}
                            >
                                <step.icon
                                    className={cn(
                                        "w-4 h-4",
                                        completedSteps.includes(index) ? "text-emerald-400" : "text-primary"
                                    )}
                                />
                            </div>
                            <div className="flex-1 min-w-0">
                                <p
                                    className={cn(
                                        "text-sm font-medium mb-1 transition-colors",
                                        completedSteps.includes(index)
                                            ? "text-emerald-400 line-through"
                                            : "text-foreground"
                                    )}
                                >
                                    {step.title}
                                </p>
                                <p className="text-xs text-muted-foreground line-clamp-2">
                                    {step.description}
                                </p>
                            </div>
                        </div>

                        {!completedSteps.includes(index) && (
                            <div className="mt-3 flex items-center text-xs font-medium text-primary group-hover:underline">
                                {step.action}
                                <ArrowRight className="w-3 h-3 ml-1" />
                            </div>
                        )}
                    </div>
                ))}
            </div>

            {/* Progress */}
            <div className="mt-6 flex items-center gap-3">
                <div className="flex-1 h-1.5 bg-border/50 rounded-full overflow-hidden">
                    <div
                        className="h-full bg-gradient-to-r from-primary to-primary/70 rounded-full transition-all duration-500"
                        style={{ width: `${(completedSteps.length / steps.length) * 100}%` }}
                    />
                </div>
                <span className="text-xs font-medium text-muted-foreground">
                    {completedSteps.length}/{steps.length}
                </span>
            </div>
        </div>
    );
};

export default OnboardingCard;
