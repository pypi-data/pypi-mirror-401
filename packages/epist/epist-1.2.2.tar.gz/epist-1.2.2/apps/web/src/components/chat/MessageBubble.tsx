import ReactMarkdown from 'react-markdown';
import { Bot, User, Play } from "lucide-react";
import { Citation } from "@/lib/api";

interface MessageBubbleProps {
    role: 'user' | 'assistant' | 'system';
    content: string;
    citations?: Citation[];
}

export function MessageBubble({ role, content, citations }: MessageBubbleProps) {
    const isUser = role === 'user';

    return (
        <div className={`flex gap-4 ${isUser ? 'flex-row-reverse' : 'flex-row'} mb-6`}>
            {/* Avatar */}
            <div className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${isUser ? 'bg-indigo-600' : 'bg-emerald-600'}`}>
                {isUser ? <User size={18} className="text-white" /> : <Bot size={18} className="text-white" />}
            </div>

            {/* Content */}
            <div className={`flex flex-col gap-2 max-w-[80%] ${isUser ? 'items-end' : 'items-start'}`}>
                <div className={`px-4 py-3 rounded-2xl ${isUser
                        ? 'bg-indigo-600/10 border border-indigo-500/20 text-indigo-100 rounded-tr-none'
                        : 'bg-slate-900 border border-slate-800 text-slate-300 rounded-tl-none'
                    }`}>
                    <div className="prose prose-invert prose-sm max-w-none">
                        <ReactMarkdown>{content}</ReactMarkdown>
                    </div>
                </div>

                {/* Citations */}
                {citations && citations.length > 0 && (
                    <div className="flex flex-wrap gap-2 mt-1">
                        {citations.map((citation) => (
                            <button
                                key={citation.id}
                                className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-slate-900 border border-slate-800 hover:border-indigo-500/50 hover:bg-indigo-500/10 transition-all text-xs text-slate-400 hover:text-indigo-300 group"
                                title={citation.text}
                            >
                                <Play size={10} className="group-hover:fill-current" />
                                <span>{formatTime(citation.start)} - {formatTime(citation.end)}</span>
                            </button>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}

function formatTime(seconds: number): string {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}
