import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2, Bot, User, Play } from 'lucide-react';
import { api, ChatMessage, Citation } from '@/lib/api';


interface ChatInterfaceProps {
    onSeek: (time: number) => void;
    messages: ChatMessage[];
    setMessages: React.Dispatch<React.SetStateAction<ChatMessage[]>>;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({ onSeek, messages, setMessages }) => {
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [citations, setCitations] = useState<Citation[]>([]);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        const userMessage: ChatMessage = { role: 'user', content: input };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);
        setCitations([]);

        try {
            // Add placeholder for assistant message
            setMessages(prev => [...prev, { role: 'assistant', content: '' }]);

            const stream = await api.chat([...messages, userMessage], true);

            if (stream instanceof ReadableStream) {
                const reader = stream.getReader();
                const decoder = new TextDecoder();
                let assistantMessage = '';

                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;

                    const chunk = decoder.decode(value);
                    const lines = chunk.split('\n\n');

                    for (const line of lines) {
                        if (line.startsWith('data: ')) {
                            const data = line.slice(6);
                            if (data === '[DONE]') break;

                            try {
                                const parsed = JSON.parse(data);
                                if (parsed.content) {
                                    assistantMessage += parsed.content;
                                    setMessages(prev => {
                                        const newMessages = [...prev];
                                        newMessages[newMessages.length - 1].content = assistantMessage;
                                        return newMessages;
                                    });
                                }
                                if (parsed.citations) {
                                    setCitations(parsed.citations);
                                }
                            } catch (e) {
                                console.error('Error parsing stream:', e);
                            }
                        }
                    }
                }
            }
        } catch (error) {
            console.error('Chat error:', error);
            setMessages(prev => [...prev, { role: 'system', content: 'Error: Failed to send message.' }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-full relative">
            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-4 space-y-6 pb-20">
                {messages.length === 0 && (
                    <div className="text-center text-slate-500 mt-20">
                        <Bot size={48} className="mx-auto mb-4 opacity-50" />
                        <h3 className="text-lg font-medium mb-2">Ask about your audio</h3>
                        <p className="text-sm">&quot;What is discussed in the podcast?&quot;</p>
                        <p className="text-sm">&quot;Summarize the key points about AI.&quot;</p>
                    </div>
                )}

                {messages.map((msg, idx) => (
                    <div key={idx} className={`flex gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                        <div className={`shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${msg.role === 'user' ? 'bg-indigo-500' : msg.role === 'system' ? 'bg-red-500' : 'bg-emerald-600'}`}>
                            {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
                        </div>
                        <div className={`flex flex-col max-w-[80%] ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
                            <div className={`px-4 py-3 rounded-2xl ${msg.role === 'user'
                                ? 'bg-indigo-600 text-white rounded-tr-none'
                                : 'bg-slate-800 text-slate-200 rounded-tl-none'
                                }`}>
                                <p className="whitespace-pre-wrap text-sm leading-relaxed">{msg.content}</p>
                            </div>

                            {/* Citations (Only for assistant's last message if available) */}
                            {msg.role === 'assistant' && idx === messages.length - 1 && citations.length > 0 && (
                                <div className="mt-3 space-y-2 w-full">
                                    <p className="text-xs font-semibold text-slate-500 uppercase">Sources</p>
                                    {citations.map((citation) => (
                                        <div
                                            key={citation.id}
                                            onClick={() => onSeek(citation.start)}
                                            className="bg-slate-900/50 border border-slate-800 rounded p-2 text-xs hover:border-indigo-500/50 cursor-pointer transition-colors group"
                                        >
                                            <div className="flex items-center justify-between mb-1">
                                                <span className="text-indigo-400 font-mono">
                                                    {Math.floor(citation.start)}s - {Math.floor(citation.end)}s
                                                </span>
                                                <Play size={12} className="opacity-0 group-hover:opacity-100 text-indigo-400" />
                                            </div>
                                            <p className="text-slate-400 line-clamp-2">{citation.text}</p>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="absolute bottom-0 left-0 right-0 p-4 bg-slate-900 border-t border-slate-800">
                <form onSubmit={handleSubmit} className="relative">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask a question..."
                        className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-4 pr-12 py-3 text-sm text-slate-200 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all"
                        disabled={isLoading}
                    />
                    <button
                        type="submit"
                        disabled={!input.trim() || isLoading}
                        className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-slate-400 hover:text-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                        {isLoading ? <Loader2 className="animate-spin" size={18} /> : <Send size={18} />}
                    </button>
                </form>
            </div>
        </div>
    );
};
