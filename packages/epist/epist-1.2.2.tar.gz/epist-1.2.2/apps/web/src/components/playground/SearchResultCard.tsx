import React from 'react';
import { SearchResult } from '@/lib/api';
import { Play, Zap } from 'lucide-react';

interface SearchResultCardProps {
    result: SearchResult;
    onSeek: (time: number) => void;
}

export function SearchResultCard({ result, onSeek }: SearchResultCardProps) {
    const formatTime = (seconds: number) => {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    return (
        <div className="p-4 rounded-lg bg-slate-900 border border-slate-800 hover:border-indigo-500/30 transition-all group">
            <div className="flex justify-between items-start mb-2">
                <div className="flex items-center gap-2">
                    <span className="text-xs font-mono text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded">
                        {formatTime(result.start)} - {formatTime(result.end)}
                    </span>
                    <div className="flex items-center gap-2">
                        <div className="flex items-center gap-1 text-xs text-slate-500" title="Relevance Score">
                            <Zap size={12} className={result.methods.includes('rerank') ? "text-green-400" : "text-amber-400"} fill="currentColor" />
                            <span className={result.methods.includes('rerank') ? "font-bold text-green-400" : ""}>
                                {(result.score * 100).toFixed(1)}%
                            </span>
                        </div>
                        {result.methods.includes('rerank') && (
                            <span className="text-[10px] uppercase font-bold text-green-400 bg-green-500/10 px-1.5 py-0.5 rounded border border-green-500/20">
                                Reranked
                            </span>
                        )}
                    </div>
                </div>
                <button
                    onClick={() => onSeek(result.start)}
                    className="p-1.5 text-slate-400 hover:text-white hover:bg-indigo-500 rounded transition-colors"
                    title="Play segment"
                >
                    <Play size={14} fill="currentColor" />
                </button>
            </div>
            <p className="text-sm text-slate-300 leading-relaxed">
                ...{result.text}...
            </p>
        </div>
    );
}
