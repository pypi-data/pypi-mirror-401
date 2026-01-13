import React from 'react';
import { Transcript } from '@/lib/api';
import { Play } from 'lucide-react';

interface TranscriptViewerProps {
    transcript: Transcript;
    onSeek: (time: number) => void;
    currentTime?: number;
}

export function TranscriptViewer({ transcript, onSeek, currentTime = 0 }: TranscriptViewerProps) {
    const formatTime = (seconds: number) => {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    return (
        <div className="flex flex-col h-full bg-slate-950 rounded-lg border border-slate-800 overflow-hidden">
            <div className="p-4 border-b border-slate-800 bg-slate-900/50 flex justify-between items-center">
                <h3 className="font-semibold text-slate-200">Transcript</h3>
                <span className="text-xs text-slate-500">{transcript.segments.length} segments</span>
            </div>
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {transcript.segments.map((segment) => {
                    const isActive = currentTime >= segment.start && currentTime <= segment.end;
                    return (
                        <div
                            key={segment.id}
                            className={`group flex gap-4 p-3 rounded-lg transition-colors ${isActive ? 'bg-indigo-500/10 border border-indigo-500/20' : 'hover:bg-slate-900 border border-transparent'}`}
                        >
                            <div className="flex flex-col items-center gap-2 pt-1">
                                <button
                                    onClick={() => onSeek(segment.start)}
                                    className={`p-1.5 rounded-full transition-colors ${isActive ? 'text-indigo-400 bg-indigo-500/20' : 'text-slate-500 bg-slate-800 group-hover:bg-indigo-500/20 group-hover:text-indigo-400'}`}
                                >
                                    <Play size={12} fill="currentColor" />
                                </button>
                                <span className="text-xs font-mono text-slate-500">{formatTime(segment.start)}</span>
                            </div>
                            <div className="flex-1">
                                <div className="flex items-center gap-2 mb-1">
                                    <span className={`text-xs font-bold uppercase tracking-wider ${isActive ? 'text-indigo-400' : 'text-slate-400'}`}>
                                        {segment.speaker || 'Speaker'}
                                    </span>
                                </div>
                                <p className={`text-sm leading-relaxed ${isActive ? 'text-slate-200' : 'text-slate-400'}`}>
                                    {segment.text}
                                </p>
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
