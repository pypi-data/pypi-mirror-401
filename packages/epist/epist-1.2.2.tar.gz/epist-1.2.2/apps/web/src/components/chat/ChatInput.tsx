import { Send, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useState, useRef, useEffect } from "react";

interface ChatInputProps {
    onSend: (message: string) => void;
    disabled?: boolean;
}

export function ChatInput({ onSend, disabled }: ChatInputProps) {
    const [input, setInput] = useState("");
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    const handleSend = () => {
        if (!input.trim() || disabled) return;
        onSend(input.trim());
        setInput("");
        // Reset height
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    // Auto-resize textarea
    useEffect(() => {
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
            textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
        }
    }, [input]);

    return (
        <div className="relative flex items-end gap-2 p-4 bg-slate-900/50 border-t border-slate-800 backdrop-blur-sm">
            <div className="relative flex-1 bg-slate-950 border border-slate-800 rounded-xl focus-within:border-indigo-500/50 focus-within:ring-1 focus-within:ring-indigo-500/50 transition-all">
                <textarea
                    ref={textareaRef}
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Ask a question about your audio..."
                    disabled={disabled}
                    rows={1}
                    className="w-full bg-transparent text-slate-200 placeholder:text-slate-500 px-4 py-3 focus:outline-none resize-none min-h-[48px] max-h-[200px]"
                />
            </div>
            <Button
                onClick={handleSend}
                disabled={!input.trim() || disabled}
                className="h-[48px] w-[48px] p-0 rounded-xl flex-shrink-0"
            >
                {disabled ? <Loader2 className="animate-spin" size={20} /> : <Send size={20} />}
            </Button>
        </div>
    );
}
