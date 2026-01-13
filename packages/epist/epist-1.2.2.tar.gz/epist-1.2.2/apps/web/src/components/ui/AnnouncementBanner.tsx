"use client";

import { useState } from "react";
import { X, Sparkles } from "lucide-react";

interface AnnouncementBannerProps {
    title: string;
    message: string;
    href?: string;
    actionLabel?: string;
    storageKey?: string;
}

export function AnnouncementBanner({
    title,
    message,
    href,
    actionLabel = "Check it out",
    storageKey
}: AnnouncementBannerProps) {
    const [isVisible, setIsVisible] = useState(() => {
        if (typeof window !== 'undefined' && storageKey) {
            return !localStorage.getItem(storageKey);
        }
        return true;
    });

    if (!isVisible) return null;

    const handleDismiss = () => {
        setIsVisible(false);
        if (storageKey) {
            localStorage.setItem(storageKey, 'dismissed');
        }
    };

    return (
        <div className="relative overflow-hidden bg-indigo-900/30 border border-indigo-500/30 rounded-xl p-4 mb-8 flex items-start sm:items-center justify-between gap-4">
            {/* Background decoration */}
            <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-r from-indigo-500/10 to-purple-500/10 pointer-events-none" />

            <div className="relative flex gap-3 items-start sm:items-center">
                <div className="p-2 bg-indigo-500/20 rounded-lg text-indigo-400 shrink-0">
                    <Sparkles size={20} />
                </div>
                <div className="flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-3">
                    <span className="font-semibold text-white">{title}</span>
                    <span className="hidden sm:inline text-slate-600">•</span>
                    <span className="text-slate-300 text-sm">{message}</span>
                </div>
            </div>

            <div className="relative flex items-center gap-3 shrink-0">
                {href && (
                    <a
                        href={href}
                        className="text-sm font-medium text-indigo-400 hover:text-indigo-300 transition-colors whitespace-nowrap"
                    >
                        {actionLabel} →
                    </a>
                )}
                <button
                    onClick={handleDismiss}
                    className="text-slate-400 hover:text-white transition-colors p-1"
                    aria-label="Dismiss"
                >
                    <X size={18} />
                </button>
            </div>
        </div>
    );
}
