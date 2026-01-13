import { Key, Copy } from "lucide-react";

interface PersistedKeyBannerProps {
    persistedKey: string;
    onCopy: (text: string) => void;
    onClear: () => void;
}

export function PersistedKeyBanner({ persistedKey, onCopy, onClear }: PersistedKeyBannerProps) {
    return (
        <div className="mb-8 p-4 bg-amber-500/10 border border-amber-500/20 rounded-xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div className="flex gap-3">
                <div className="p-2 bg-amber-500/20 rounded-lg text-amber-400 shrink-0">
                    <Key size={20} />
                </div>
                <div>
                    <h3 className="font-semibold text-amber-200">Last Generated API Key</h3>
                    <p className="text-sm text-amber-200/70 mb-2">This key is saved locally. Make sure to copy it.</p>
                    <div className="flex items-center gap-2">
                        <code className="px-2 py-1 bg-black/30 rounded text-amber-100 font-mono text-sm break-all">
                            {persistedKey}
                        </code>
                        <button
                            onClick={() => onCopy(persistedKey)}
                            className="p-1.5 text-amber-400 hover:text-white hover:bg-amber-500/20 rounded transition-colors"
                            title="Copy"
                        >
                            <Copy size={14} />
                        </button>
                    </div>
                </div>
            </div>
            <button
                onClick={onClear}
                className="text-xs font-medium text-amber-400 hover:text-amber-300 px-3 py-1.5 hover:bg-amber-500/10 rounded transition-colors"
            >
                Clear
            </button>
        </div>
    );
}
