import { useState, useRef, useEffect } from "react";
import { ChatInput } from "./ChatInput";
import { MessageBubble } from "./MessageBubble";
import { api, ChatMessage, Citation } from "@/lib/api";
import { toast } from "sonner";

interface ExtendedMessage extends ChatMessage {
    citations?: Citation[];
}

export function ChatInterface() {
    const [messages, setMessages] = useState<ExtendedMessage[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async (content: string) => {
        const userMessage: ExtendedMessage = { role: "user", content };
        setMessages(prev => [...prev, userMessage]);
        setIsLoading(true);

        try {
            // Create placeholder for assistant message
            const assistantMessage: ExtendedMessage = { role: "assistant", content: "" };
            setMessages(prev => [...prev, assistantMessage]);

            const stream = await api.chat([...messages, userMessage], true);

            if (stream instanceof ReadableStream) {
                const reader = stream.getReader();
                const decoder = new TextDecoder();
                let fullContent = "";

                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;

                    const chunk = decoder.decode(value);
                    const lines = chunk.split("\n\n");

                    for (const line of lines) {
                        if (line.startsWith("data: ")) {
                            const data = line.slice(6);
                            if (data === "[DONE]") continue;

                            try {
                                const parsed = JSON.parse(data);
                                if (parsed.content) {
                                    fullContent += parsed.content;
                                    setMessages(prev => {
                                        const newMessages = [...prev];
                                        const lastMsg = newMessages[newMessages.length - 1];
                                        if (lastMsg.role === "assistant") {
                                            lastMsg.content = fullContent;
                                        }
                                        return newMessages;
                                    });
                                }
                                if (parsed.citations) {
                                    setMessages(prev => {
                                        const newMessages = [...prev];
                                        const lastMsg = newMessages[newMessages.length - 1];
                                        if (lastMsg.role === "assistant") {
                                            lastMsg.citations = parsed.citations;
                                        }
                                        return newMessages;
                                    });
                                }
                            } catch (e) {
                                console.error("Error parsing stream chunk", e);
                            }
                        }
                    }
                }
            } else {
                // Fallback for non-streaming (shouldn't happen with current config)
                setMessages(prev => {
                    const newMessages = [...prev];
                    newMessages[newMessages.length - 1] = {
                        role: "assistant",
                        // eslint-disable-next-line @typescript-eslint/no-explicit-any
                        content: (stream as any).choices[0].message.content,
                        // eslint-disable-next-line @typescript-eslint/no-explicit-any
                        citations: (stream as any).citations
                    };
                    return newMessages;
                });
            }
        } catch (error) {
            console.error("Chat error:", error);
            toast.error("Failed to send message");
            // Remove the empty assistant message if it failed immediately
            setMessages(prev => prev.slice(0, -1));
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-[calc(100vh-6rem)] max-w-4xl mx-auto">
            <div className="flex-1 overflow-y-auto p-6 space-y-6">
                {messages.length === 0 ? (
                    <div className="h-full flex flex-col items-center justify-center text-center space-y-4 opacity-50">
                        <div className="w-16 h-16 bg-slate-800 rounded-2xl flex items-center justify-center">
                            <span className="text-4xl">👋</span>
                        </div>
                        <div>
                            <h3 className="text-xl font-semibold text-slate-200">Welcome to Audio Chat</h3>
                            <p className="text-slate-400 max-w-md mt-2">
                                Ask questions about your uploaded audio files. I&apos;ll search through transcripts and provide answers with citations.
                            </p>
                        </div>
                    </div>
                ) : (
                    messages.map((msg, idx) => (
                        <MessageBubble
                            key={idx}
                            role={msg.role}
                            content={msg.content}
                            citations={msg.citations}
                        />
                    ))
                )}
                <div ref={messagesEndRef} />
            </div>

            <div className="p-4">
                <ChatInput onSend={handleSend} disabled={isLoading} />
            </div>
        </div>
    );
}
