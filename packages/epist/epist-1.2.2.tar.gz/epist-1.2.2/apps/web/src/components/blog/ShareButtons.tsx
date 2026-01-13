"use client";

import { Share2, Linkedin, Twitter, Check } from "lucide-react";
import { useState } from "react";

interface ShareButtonsProps {
    url: string;
    title: string;
}

export function ShareButtons({ url, title }: ShareButtonsProps) {
    const [copied, setCopied] = useState(false);

    const handleCopy = async () => {
        try {
            await navigator.clipboard.writeText(url);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        } catch (err) {
            console.error("Failed to copy:", err);
        }
    };

    const shareOnTwitter = () => {
        const twitterUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(title)}&url=${encodeURIComponent(url)}`;
        window.open(twitterUrl, "_blank", "noopener,noreferrer");
    };

    const shareOnLinkedIn = () => {
        const linkedinUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`;
        window.open(linkedinUrl, "_blank", "noopener,noreferrer");
    };

    return (
        <div className="flex items-center gap-3">
            <button
                onClick={handleCopy}
                title="Copy link"
                className="p-2 rounded-full bg-secondary border border-border text-muted-foreground hover:text-foreground hover:border-primary/50 transition-all group relative"
            >
                {copied ? <Check size={18} className="text-emerald-500" /> : <Share2 size={18} />}
                {copied && (
                    <span className="absolute -top-10 left-1/2 -translate-x-1/2 px-2 py-1 bg-card text-foreground text-xs rounded border border-border shadow-elevated whitespace-nowrap">
                        Copied!
                    </span>
                )}
            </button>
            <button
                onClick={shareOnLinkedIn}
                title="Share on LinkedIn"
                className="p-2 rounded-full bg-secondary border border-border text-muted-foreground hover:text-[#0077b5] hover:border-[#0077b5]/50 transition-all"
            >
                <Linkedin size={18} />
            </button>
            <button
                onClick={shareOnTwitter}
                title="Share on Twitter"
                className="p-2 rounded-full bg-secondary border border-border text-muted-foreground hover:text-[#1DA1F2] hover:border-[#1DA1F2]/50 transition-all"
            >
                <Twitter size={18} />
            </button>
        </div>
    );
}
