"use client";

import { useState } from "react";
import { Check, Copy } from "lucide-react";


interface CodeBlockProps {
    code?: string;
    variants?: Record<string, string>; // e.g., { python: "...", javascript: "..." }
    language?: string; // Default language if code is used, or initial active tab
    filename?: string;
}

export function CodeBlock({ code, variants, language = "bash", filename }: CodeBlockProps) {
    const [copied, setCopied] = useState(false);
    // If variants exist, use the first key as default active language if generic 'language' isn't in variants
    const availableLanguages = variants ? Object.keys(variants) : [];
    const [activeLang, setActiveLang] = useState(
        (variants && language && variants[language]) ? language : (availableLanguages[0] || language)
    );

    const activeCode = variants ? variants[activeLang] : code || "";

    const handleCopy = () => {
        navigator.clipboard.writeText(activeCode);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div className="relative group rounded-lg overflow-hidden bg-slate-950 border border-slate-800 my-4">
            <div className="flex items-center justify-between border-b border-slate-800 bg-slate-900/50">
                {/* Tabs or Filename */}
                <div className="flex">
                    {variants ? (
                        availableLanguages.map(lang => (
                            <button
                                key={lang}
                                onClick={() => setActiveLang(lang)}
                                className={`px-4 py-2 text-xs font-medium border-r border-slate-800 transition-colors ${activeLang === lang
                                        ? "bg-slate-800 text-indigo-400"
                                        : "text-slate-500 hover:text-slate-300 hover:bg-slate-900"
                                    }`}
                            >
                                {lang === 'javascript' ? 'JavaScript' : lang === 'python' ? 'Python' : lang}
                            </button>
                        ))
                    ) : (
                        <div className="px-4 py-2 text-xs text-slate-500 font-mono flex items-center gap-2">
                            <div className="flex gap-1.5">
                                <div className="w-2.5 h-2.5 rounded-full bg-slate-700" />
                                <div className="w-2.5 h-2.5 rounded-full bg-slate-700" />
                            </div>
                            {filename && <span className="ml-2 text-slate-400">{filename}</span>}
                        </div>
                    )}
                </div>

                {/* Copy Button */}
                <div className="flex items-center gap-2 pr-2">
                    {!variants && <span className="text-xs text-slate-600 mr-2">{language}</span>}
                    <button
                        onClick={handleCopy}
                        className="p-1.5 rounded hover:bg-slate-800 text-slate-500 hover:text-white transition-colors"
                        title="Copy code"
                    >
                        {copied ? <Check size={14} className="text-green-500" /> : <Copy size={14} />}
                    </button>
                </div>
            </div>

            <pre className="p-4 overflow-x-auto text-sm font-mono leading-relaxed text-indigo-100">
                {activeCode}
            </pre>
        </div>
    );
}
