import React, { useState } from 'react';
import { Epist, SearchResult } from 'epist';
import { Search, Loader2, AlertCircle } from 'lucide-react';

export interface AudioSearchWidgetProps {
    apiKey: string;
    baseUrl?: string;
    placeholder?: string;
    limit?: number;
    className?: string;
}

export const AudioSearchWidget: React.FC<AudioSearchWidgetProps> = ({
    apiKey,
    baseUrl,
    placeholder = "Search audio knowledge base...",
    limit = 5,
    className = ""
}) => {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState<SearchResult[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleSearch = async () => {
        if (!query.trim()) return;

        setIsLoading(true);
        setError(null);

        try {
            const client = new Epist({ apiKey, baseUrl });
            const searchResults = await client.search(query, limit);
            setResults(searchResults);
        } catch (err: any) {
            console.error("Epist Search Error:", err);
            setError(err.message || "Failed to search");
        } finally {
            setIsLoading(false);
        }
    };

    const formatTime = (seconds: number) => {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    return (
        <div className={`epist-widget font-sans ${className}`}>
            <div className="relative flex items-center mb-4">
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                    placeholder={placeholder}
                    className="w-full px-4 py-2 pr-10 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                />
                <button
                    onClick={handleSearch}
                    disabled={isLoading || !query}
                    className="absolute right-2 p-1.5 text-gray-400 hover:text-indigo-500 disabled:opacity-50 transition-colors"
                >
                    {isLoading ? <Loader2 className="animate-spin" size={20} /> : <Search size={20} />}
                </button>
            </div>

            {error && (
                <div className="flex items-center gap-2 text-sm text-red-500 mb-4 bg-red-50 p-3 rounded-lg border border-red-100">
                    <AlertCircle size={16} />
                    {error}
                </div>
            )}

            <div className="space-y-3">
                {results.map((result) => (
                    <div key={result.id} className="p-3 bg-white border border-gray-200 rounded-lg hover:shadow-sm transition-shadow">
                        <div className="flex justify-between items-start mb-1">
                            <div className="flex items-center gap-2 text-xs text-gray-500">
                                <span className="font-mono bg-gray-100 px-1.5 py-0.5 rounded">
                                    {formatTime(result.start)} - {formatTime(result.end)}
                                </span>
                                <span className="text-indigo-600 font-medium">
                                    {(result.score * 100).toFixed(0)}% Match
                                </span>
                            </div>
                        </div>
                        <p className="text-sm text-gray-700 leading-relaxed line-clamp-2">
                            {result.text}
                        </p>
                    </div>
                ))}
                {results.length === 0 && !isLoading && !error && query && (
                    <p className="text-center text-gray-400 text-sm py-4">No results found</p>
                )}
            </div>
        </div>
    );
};
