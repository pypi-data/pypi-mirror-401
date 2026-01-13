"use client";

import { Eye, EyeOff, Copy, Check } from "lucide-react";
import { useState } from "react";

interface ApiKeyDisplayProps {
    apiKey: string;
    name?: string;
    createdAt?: string;
}

export function ApiKeyDisplay({ apiKey, name, createdAt }: ApiKeyDisplayProps) {
    const [revealed, setRevealed] = useState(false);
    const [copied, setCopied] = useState(false);

    const maskedKey = apiKey.slice(0, 7) + "•".repeat(20) + apiKey.slice(-4);

    const copyToClipboard = () => {
        navigator.clipboard.writeText(apiKey);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div className="api-key-container bg-zinc-900 border border-zinc-800 rounded-lg p-4">
            {name && (
                <div className="flex items-center justify-between mb-3">
                    <h4 className="text-sm font-semibold text-zinc-100">{name}</h4>
                    {createdAt && <span className="text-xs text-zinc-500">Created {createdAt}</span>}
                </div>
            )}
            <div className="flex items-center gap-2">
                <div className="flex-1 api-key">
                    <span className="text-zinc-100">
                        {revealed ? apiKey : maskedKey}
                    </span>
                </div>
                <button
                    onClick={() => setRevealed(!revealed)}
                    className="p-2 rounded-md bg-zinc-800 hover:bg-zinc-700 transition-colors border border-zinc-700"
                    title={revealed ? "Hide" : "Reveal"}
                >
                    {revealed ? (
                        <EyeOff className="w-4 h-4 text-zinc-400" />
                    ) : (
                        <Eye className="w-4 h-4 text-zinc-400" />
                    )}
                </button>
                <button
                    onClick={copyToClipboard}
                    className="p-2 rounded-md bg-zinc-800 hover:bg-zinc-700 transition-colors border border-zinc-700"
                    title={copied ? "Copied!" : "Copy"}
                >
                    {copied ? (
                        <Check className="w-4 h-4 text-green-400" />
                    ) : (
                        <Copy className="w-4 h-4 text-zinc-400" />
                    )}
                </button>
            </div>
        </div>
    );
}
