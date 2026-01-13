"use client";

import { useState, useRef, useEffect } from "react";
import {
    Send, Loader2, Play, Clock, Upload, Code, FileJson,
    MessageSquare, Search, List, Settings2, Zap, ChevronDown, Copy, Check, Terminal, Activity
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";

import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import {
    Collapsible,
    CollapsibleContent,
    CollapsibleTrigger,
} from "@/components/ui/collapsible";
import {
    Tooltip,
    TooltipContent,
    TooltipProvider,
    TooltipTrigger,
} from "@/components/ui/tooltip";
import { cn } from "@/lib/utils";
import { useToast } from "@/hooks/use-toast";
import { api, SearchResult, Transcript, ChatMessage, TraceEvent, RequestLog } from "@/lib/api";
import TraceWaterfall from "@/components/observability/TraceWaterfall";


export default function Playground() {
    const { toast } = useToast();

    // State from old Playground
    const [isLoading, setIsLoading] = useState(false);
    const [result, setResult] = useState<SearchResult[] | null>(null); // Replaces QueryResult
    const [transcript, setTranscript] = useState<Transcript | null>(null);
    const [currentTraceId, setCurrentTraceId] = useState<string | null>(null);
    const [traceEvents, setTraceEvents] = useState<TraceEvent[]>([]);
    const [currentLogs, setCurrentLogs] = useState<RequestLog[]>([]);
    const [isLoadingObservability, setIsLoadingObservability] = useState(false);
    const [audioUrl, setAudioUrl] = useState<string | null>(null);
    const [currentAudioId, setCurrentAudioId] = useState<string | null>(null);
    const [currentTime, setCurrentTime] = useState(0);

    const audioRef = useRef<HTMLAudioElement>(null);

    // New Design State
    const [inputMode, setInputMode] = useState<"upload" | "json">("upload");
    const [searchMode, setSearchMode] = useState<"standard" | "pro">("standard");
    const [advancedOpen, setAdvancedOpen] = useState(false);
    const [rrfK, setRrfK] = useState([60]);
    const [rerankModel, setRerankModel] = useState('cohere');
    const [chatModel, setChatModel] = useState("gpt-3.5-turbo");
    const [jsonConfig, setJsonConfig] = useState(`{
  "audio_url": "",
  "rag_enabled": true,
  "language": "en",
  "model": "whisper-large-v3",
  "diarization": true
}`);
    interface PlaygroundMessage extends ChatMessage {
        metadata?: {
            model: string;
            tier: string;
            rrf_k: number;
            rerank_model?: string;
            latency?: number;
            timestamp: string;
        };
        citations?: SearchResult[];
    }

    const [chatMessages, setChatMessages] = useState<PlaygroundMessage[]>([]);
    const [chatInput, setChatInput] = useState("");
    const [copied, setCopied] = useState(false);
    const [outputTab, setOutputTab] = useState("json");
    const [response, setResponse] = useState<string | null>(null); // Raw JSON response
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);

    // Restore State Logic (Simplified for brevity, similar to old playground)
    useEffect(() => {
        const restoreState = async () => {
            const savedAudioId = localStorage.getItem('playground_audio_id');
            if (savedAudioId) {
                setCurrentAudioId(savedAudioId);
                setIsLoading(true);
                try {
                    // Restore logic here... (omitted to avoid overly complex restoration for this pass)
                    // For now, let's just respect detailed state restoration if needed, but the primary goal is visual port.
                    // Re-implementing basic status check:
                    const statusRes = await api.getAudioStatus(savedAudioId);
                    setResponse(JSON.stringify(statusRes, null, 2));
                    if (statusRes.status === 'completed') {
                        const transcriptData = await api.getTranscript(savedAudioId);
                        setTranscript(transcriptData);
                        try {
                            const audioBlob = await api.getAudioContent(savedAudioId);
                            setAudioUrl(URL.createObjectURL(audioBlob));
                        } catch (e) { console.error(e); }
                    }
                } catch (error) {
                    console.error("Failed to restore state", error);
                } finally {
                    setIsLoading(false);
                }
            }
        };
        restoreState();
    }, []);

    const handleTranscribe = async () => {
        setIsLoading(true);
        setOutputTab('json');
        try {
            // Clear previous session state before new transcription
            setResult(null);
            setTranscript(null);
            setChatMessages([]);
            setCurrentTraceId(null);
            setTraceEvents([]);
            setCurrentLogs([]);
            setResponse(null);

            let res;
            if (inputMode === 'upload' && selectedFile) {
                res = await api.uploadAudio(selectedFile);
                localStorage.setItem('playground_audio_id', res.id);
                setCurrentAudioId(res.id);
                pollStatus(res.id);
            } else if (inputMode === 'json') {
                const config = JSON.parse(jsonConfig);
                if (!config.audio_url) throw new Error("audio_url is required");
                setAudioUrl(config.audio_url); // Optimistically set URL
                res = await api.transcribeUrl(config.audio_url, config.rag_enabled, config.language);
                localStorage.setItem('playground_audio_id', res.id);
                setCurrentAudioId(res.id);
                pollStatus(res.id);
            }
            setResponse(JSON.stringify({
                request: inputMode === 'upload' ? {
                    filename: selectedFile?.name,
                    size: selectedFile?.size
                } : JSON.parse(jsonConfig),
                response: res
            }, null, 2));
            toast({ title: "Request submitted", description: "Processing started..." });
        } catch (error) {
            console.error(error);
            toast({ variant: "destructive", title: "Error", description: (error as Error).message });
            setIsLoading(false);
        }
    };

    const pollStatus = (id: string) => {
        const pollInterval = setInterval(async () => {
            try {
                const statusRes = await api.getAudioStatus(id);
                setResponse(prev => {
                    if (!prev) return JSON.stringify({ status: statusRes }, null, 2);
                    try {
                        const current = JSON.parse(prev);
                        return JSON.stringify({ ...current, status: statusRes }, null, 2);
                    } catch {
                        return JSON.stringify({ status: statusRes }, null, 2);
                    }
                });

                if (statusRes.status === 'completed') {
                    clearInterval(pollInterval);
                    setIsLoading(false);
                    const transcriptData = await api.getTranscript(id);
                    setTranscript(transcriptData);
                    setOutputTab('transcript');
                    toast({ title: "Completed", description: "Transcription finished successfully." });
                } else if (statusRes.status === 'failed') {
                    clearInterval(pollInterval);
                    setIsLoading(false);
                    toast({ variant: "destructive", title: "Failed", description: "Transcription failed." });
                }
            } catch {
                clearInterval(pollInterval);
                setIsLoading(false);
            }
        }, 2000);
    };



    const handleChatSend = async (overrideInput?: string) => {
        const input = overrideInput || chatInput;
        if (!input.trim()) return;

        const userMessage: PlaygroundMessage = { role: "user", content: input };
        const newMessages = [...chatMessages, userMessage];
        setChatMessages(newMessages);
        setChatInput("");
        setIsLoading(true);
        setOutputTab('chat');

        try {
            const stream = await api.chat(
                newMessages,
                true,
                searchMode === 'pro' ? 'pro' : 'free',
                rrfK[0],
                rerankModel,
                currentAudioId || undefined,
                chatModel
            ) as ReadableStream;
            const reader = stream.getReader();
            const decoder = new TextDecoder();
            let assistantContent = "";
            let collectedCitations: SearchResult[] = [];
            let rId = "";
            const rawChunks: unknown[] = [];

            setChatMessages(prev => [...prev, {
                role: "assistant",
                content: "",
                metadata: {
                    model: chatModel,
                    tier: searchMode === 'pro' ? 'pro' : 'free',
                    rrf_k: rrfK[0],
                    rerank_model: searchMode === 'pro' ? rerankModel : undefined,
                    timestamp: new Date().toLocaleTimeString()
                }
            }]);

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                const lines = chunk.split("\n\n");
                for (const line of lines) {
                    if (line.startsWith("data: ")) {
                        const dataStr = line.replace("data: ", "");
                        if (dataStr === "[DONE]") {
                            rawChunks.push("[DONE]");
                            continue;
                        }
                        try {
                            const data = JSON.parse(dataStr);
                            rawChunks.push(data);
                            if (data.trace_id) {
                                rId = data.trace_id;
                                setCurrentTraceId(data.trace_id);
                            }
                            if (data.citations) {
                                const uniqueCitations = Array.from(
                                    new Map(data.citations.map((c: SearchResult) => [c.text, c])).values()
                                ) as SearchResult[];
                                collectedCitations = uniqueCitations;
                                setResult(uniqueCitations);
                            }
                            if (data.content) {
                                assistantContent += data.content;
                                setChatMessages(prev => {
                                    const msgs = [...prev];
                                    const last = msgs[msgs.length - 1];
                                    last.content = assistantContent;
                                    if (collectedCitations.length > 0) {
                                        last.citations = collectedCitations;
                                    }
                                    return msgs;
                                });
                            }
                        } catch { /* ignore partial json */ }
                    }
                }
            }

            // Reconstruct final structure for JSON tab
            setResponse(JSON.stringify({
                request: {
                    messages: newMessages,
                    tier: searchMode === 'pro' ? 'pro' : 'free',
                    rrf_k: rrfK[0],
                    rerank_model: rerankModel
                },
                response: {
                    trace_id: rId,
                    content: assistantContent,
                    citations: collectedCitations,
                    raw_stream: rawChunks
                }
            }, null, 2));

        } catch (error) {
            toast({ variant: "destructive", title: "Chat Error", description: (error as Error).message });
        } finally {
            setIsLoading(false);
        }
    };

    // Fetch observability data when trace ID changes
    useEffect(() => {
        if (!currentTraceId) {
            setTraceEvents([]);
            setCurrentLogs([]);
            return;
        }

        const fetchObservability = async () => {
            setIsLoadingObservability(true);
            try {
                // Fetch trace details
                const events = await api.getTraceDetails(currentTraceId);
                setTraceEvents(events);

                // Fetch matching logs
                const logs = await api.getLogs(5, 0, undefined, undefined, undefined, undefined, currentTraceId);
                setCurrentLogs(logs);
            } catch (err) {
                console.error("Failed to fetch observability data:", err);
            } finally {
                setIsLoadingObservability(false);
            }
        };

        fetchObservability();
    }, [currentTraceId]);

    const handleCopyJson = () => {
        if (!response) return;
        navigator.clipboard.writeText(response);
        setCopied(true);
        toast({ title: "Copied!", description: "JSON response copied to clipboard." });
        setTimeout(() => setCopied(false), 2000);
    };

    const formatTime = (seconds: number) => {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, "0")}`;
    };

    const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files?.[0]) {
            const file = e.target.files[0];
            setSelectedFile(file);
            setAudioUrl(URL.createObjectURL(file));

            // Clear previous session state
            setResult(null);
            setTranscript(null);
            setChatMessages([]);
            setCurrentTraceId(null);
            setTraceEvents([]);
            setCurrentLogs([]);
            setResponse(null);
            localStorage.removeItem('playground_audio_id');
        }
    };

    return (
        <div className="max-w-7xl mx-auto space-y-6">
            {/* Page Header */}
            <div className="mb-6">
                <h1 className="text-2xl font-bold tracking-tight text-foreground mb-1">Playground</h1>
                <p className="text-muted-foreground">Test APIs, transcribe audio, and chat with your recordings.</p>
            </div>

            {/* Main Layout - Split View */}
            <div className="grid gap-6 lg:grid-cols-[400px_1fr]">
                {/* Left Panel - Configuration & Settings */}
                <div className="space-y-4">
                    {/* Input Mode */}
                    <div className="p-4 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50">
                        <div className="flex gap-2 mb-4">
                            <Button
                                variant={inputMode === "upload" ? "default" : "outline"}
                                size="sm"
                                onClick={() => setInputMode("upload")}
                                className="flex-1 gap-2"
                            >
                                <Upload className="w-4 h-4" />
                                Upload
                            </Button>
                            <Button
                                variant={inputMode === "json" ? "default" : "outline"}
                                size="sm"
                                onClick={() => setInputMode("json")}
                                className="flex-1 gap-2"
                            >
                                <FileJson className="w-4 h-4" />
                                URL
                            </Button>
                        </div>

                        {inputMode === "upload" ? (
                            <div
                                className="border-2 border-dashed border-border/50 rounded-xl p-6 text-center hover:border-primary/30 transition-colors cursor-pointer"
                                onClick={() => fileInputRef.current?.click()}
                            >
                                <input
                                    type="file"
                                    ref={fileInputRef}
                                    className="hidden"
                                    accept="audio/*"
                                    onChange={handleFileSelect}
                                />
                                <Upload className="w-8 h-8 text-muted-foreground mx-auto mb-2" />
                                <p className="text-xs text-foreground font-medium mb-1 truncate max-w-[280px] mx-auto block" title={selectedFile ? selectedFile.name : undefined}>
                                    {selectedFile ? selectedFile.name : "Choose audio file"}
                                </p>
                                <Button className="mt-4 w-full gap-2" size="sm" onClick={(e) => { e.stopPropagation(); handleTranscribe(); }} disabled={!selectedFile || isLoading}>
                                    <Zap className="w-4 h-4" />
                                    Transcribe
                                </Button>
                            </div>
                        ) : (
                            <div className="space-y-4">
                                <Textarea
                                    value={jsonConfig}
                                    onChange={(e) => setJsonConfig(e.target.value)}
                                    className="min-h-[150px] font-mono text-xs bg-background/50 border-border/50"
                                    placeholder='{"audio_url": "..."}'
                                />
                                <Button className="w-full gap-2" size="sm" onClick={handleTranscribe} disabled={isLoading}>
                                    <Send className="w-4 h-4" />
                                    Execute
                                </Button>
                            </div>
                        )}
                    </div>

                    {/* Search Settings */}
                    <div className="p-4 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50">
                        <div className="flex items-center justify-between mb-4">
                            <h3 className="text-sm font-semibold text-foreground">RAG Settings</h3>
                            <div className="flex flex-col gap-2">
                                <div className="flex gap-1 justify-end">
                                    <Button
                                        variant={searchMode === "standard" ? "secondary" : "ghost"}
                                        size="sm"
                                        onClick={() => setSearchMode("standard")}
                                        className="h-7 text-xs"
                                    >
                                        Base
                                    </Button>
                                    <Button
                                        variant={searchMode === "pro" ? "secondary" : "ghost"}
                                        size="sm"
                                        onClick={() => setSearchMode("pro")}
                                        className="h-7 text-xs gap-1"
                                    >
                                        <Zap className="w-3 h-3" />
                                        Pro
                                    </Button>
                                </div>
                                <Select value={chatModel} onValueChange={setChatModel}>
                                    <SelectTrigger className="h-7 text-[10px] bg-background/50 border-border/50 uppercase font-bold tracking-tight">
                                        <SelectValue placeholder="Model" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="gpt-3.5-turbo">GPT-3.5 Turbo</SelectItem>
                                        <SelectItem value="gpt-4-turbo">GPT-4 Turbo</SelectItem>
                                        <SelectItem value="gpt-4o">GPT-4o</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>
                        </div>

                        <Collapsible open={advancedOpen} onOpenChange={setAdvancedOpen}>
                            <CollapsibleTrigger asChild>
                                <Button variant="ghost" size="sm" className="w-full justify-between text-muted-foreground h-8">
                                    <span className="flex items-center gap-2 text-xs">
                                        <Settings2 className="w-3.5 h-3.5" />
                                        Advanced Controls
                                    </span>
                                    <ChevronDown className={cn("w-3.5 h-3.5 transition-transform", advancedOpen && "rotate-180")} />
                                </Button>
                            </CollapsibleTrigger>
                            <CollapsibleContent className="pt-3 space-y-4">
                                <div>
                                    <div className="flex items-center justify-between mb-2">
                                        <Label className="text-[10px] text-muted-foreground uppercase">RRF K</Label>
                                        <span className="text-[10px] font-mono text-foreground">{rrfK[0]}</span>
                                    </div>
                                    <Slider
                                        value={rrfK}
                                        onValueChange={setRrfK}
                                        min={1}
                                        max={100}
                                        step={1}
                                    />
                                </div>
                                <div className="space-y-1.5">
                                    <Label className="text-[10px] text-muted-foreground uppercase">Rerank Model</Label>
                                    <Select value={rerankModel} onValueChange={setRerankModel}>
                                        <SelectTrigger className="h-8 text-xs bg-background/50 border-border/50">
                                            <SelectValue />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="cohere">Cohere v3</SelectItem>
                                            <SelectItem value="bge">BGE Rerank</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>
                            </CollapsibleContent>
                        </Collapsible>
                    </div>

                    {/* Audio Player - Bottom Left */}
                    <div className="p-4 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50">
                        <Label className="text-[10px] font-medium text-muted-foreground uppercase tracking-widest mb-3 block">Audio Reference</Label>
                        {audioUrl ? (
                            <audio
                                ref={audioRef}
                                src={audioUrl}
                                controls
                                className="w-full h-8"
                                onTimeUpdate={(e) => setCurrentTime(e.currentTarget.currentTime)}
                            />
                        ) : (
                            <div className="text-center py-2 text-[10px] text-muted-foreground border border-dashed border-border/50 rounded-lg">
                                No audio loaded
                            </div>
                        )}
                    </div>
                </div>

                {/* Right Panel - Output Area */}
                <div className="flex flex-col min-h-[600px] rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50 overflow-hidden">
                    <Tabs value={outputTab} onValueChange={setOutputTab} className="flex-1 flex flex-col">
                        <div className="px-4 py-2 border-b border-border/50 flex items-center justify-between bg-muted/20">
                            <TabsList className="bg-transparent h-8 p-0 gap-4">
                                <TabsTrigger value="chat" className="data-[state=active]:bg-transparent data-[state=active]:shadow-none data-[state=active]:text-primary border-none p-0 h-full gap-2 text-xs font-semibold">
                                    <MessageSquare className="w-3.5 h-3.5" />
                                    Assistant
                                </TabsTrigger>
                                <TabsTrigger value="transcript" className="data-[state=active]:bg-transparent data-[state=active]:shadow-none data-[state=active]:text-primary border-none p-0 h-full gap-2 text-xs font-semibold" disabled={!transcript}>
                                    <List className="w-3.5 h-3.5" />
                                    Transcript
                                </TabsTrigger>
                                <TabsTrigger value="search" className="data-[state=active]:bg-transparent data-[state=active]:shadow-none data-[state=active]:text-primary border-none p-0 h-full gap-2 text-xs font-semibold">
                                    <Search className="w-3.5 h-3.5" />
                                    Segments
                                </TabsTrigger>
                                <TabsTrigger value="json" className="data-[state=active]:bg-transparent data-[state=active]:shadow-none data-[state=active]:text-primary border-none p-0 h-full gap-2 text-xs font-semibold">
                                    <Code className="w-3.5 h-3.5" />
                                    Raw JSON
                                </TabsTrigger>
                                <TabsTrigger value="logs" className="data-[state=active]:bg-transparent data-[state=active]:shadow-none data-[state=active]:text-primary border-none p-0 h-full gap-2 text-xs font-semibold">
                                    <Terminal className="w-3.5 h-3.5" />
                                    Logs
                                </TabsTrigger>
                                <TabsTrigger value="trace" className="data-[state=active]:bg-transparent data-[state=active]:shadow-none data-[state=active]:text-primary border-none p-0 h-full gap-2 text-xs font-semibold">
                                    <Activity className="w-3.5 h-3.5" />
                                    Trace
                                </TabsTrigger>
                            </TabsList>
                        </div>

                        <div className="flex-1 overflow-auto p-4 relative flex flex-col items-stretch justify-start">
                            <TabsContent value="chat" className="m-0 h-full flex flex-col">
                                <div className="space-y-6 pb-20">
                                    {chatMessages.length === 0 ? (
                                        <div className="flex flex-col items-center justify-center p-12 text-center h-full opacity-40">
                                            <Zap className="w-12 h-12 mb-4 text-primary" />
                                            <h3 className="text-lg font-bold">Audio Intelligence</h3>
                                            <p className="text-sm max-w-[280px] mt-2 mb-8">Ask questions like &quot;Summarize the key takeaways&quot; or &quot;Where did they mention the pricing?&quot;</p>

                                            <div className="flex flex-col gap-2 w-full max-w-sm">
                                                <p className="text-[10px] uppercase tracking-wider font-bold mb-1">Try asking:</p>
                                                {[
                                                    "What were the key decisions made?",
                                                    "Summarize the action items",
                                                    "What concerns were raised?"
                                                ].map((q) => (
                                                    <Button
                                                        key={q}
                                                        variant="outline"
                                                        size="sm"
                                                        className="justify-start h-9 text-xs font-medium hover:bg-primary/5 hover:text-primary transition-all rounded-xl"
                                                        onClick={() => handleChatSend(q)}
                                                    >
                                                        <MessageSquare className="w-3 h-3 mr-2 opacity-50" />
                                                        {q}
                                                    </Button>
                                                ))}
                                            </div>
                                        </div>
                                    ) : (
                                        chatMessages.map((msg, i) => (
                                            <div
                                                key={i}
                                                className={cn(
                                                    "flex gap-4 group",
                                                    msg.role === "user" ? "justify-end" : "justify-start"
                                                )}
                                            >
                                                {msg.role === "assistant" && (
                                                    <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0 mt-1">
                                                        <Zap className="w-4 h-4 text-primary" />
                                                    </div>
                                                )}
                                                <div
                                                    className={cn(
                                                        "rounded-2xl px-4 py-2.5 max-w-[85%] text-sm leading-relaxed",
                                                        msg.role === "user"
                                                            ? "bg-primary text-primary-foreground shadow-sm"
                                                            : "bg-muted/50 border border-border/50 text-foreground"
                                                    )}
                                                >
                                                    {msg.content ? (
                                                        <div className="whitespace-pre-wrap">
                                                            {msg.role === "assistant" ? (
                                                                <TooltipProvider>
                                                                    {msg.content.split(/(\[Source \d+(?:[,\s]+Source \d+)*\])/g).map((part, index) => {
                                                                        const isMatch = part.match(/\[Source (\d+(?:[,\s]+Source \d+)*)\]/);
                                                                        if (isMatch) {
                                                                            // Extract all source numbers (e.g., "1, 5" or "1, Source 5")
                                                                            const numbers = part.match(/\d+/g);
                                                                            if (!numbers) return part;

                                                                            return (
                                                                                <span key={index} className="inline-flex items-center gap-0.5">
                                                                                    {numbers.map((numStr, nIdx) => {
                                                                                        const sourceNum = parseInt(numStr);
                                                                                        const citation = msg.citations?.[sourceNum - 1];

                                                                                        if (citation) {
                                                                                            const timeStr = formatTime(citation.start);
                                                                                            return (
                                                                                                <Tooltip key={nIdx}>
                                                                                                    <TooltipTrigger asChild>
                                                                                                        <span
                                                                                                            className="mx-0.5 inline-flex items-center gap-1 bg-primary/10 hover:bg-primary/20 text-primary px-1.5 py-0.5 rounded text-[10px] font-bold cursor-help transition-all border border-primary/20 active:scale-95 shadow-sm"
                                                                                                            onClick={() => {
                                                                                                                if (audioRef.current) {
                                                                                                                    audioRef.current.currentTime = citation.start;
                                                                                                                    audioRef.current.play();
                                                                                                                }
                                                                                                            }}
                                                                                                        >
                                                                                                            <span className="opacity-50 text-[9px]">{sourceNum}</span>
                                                                                                            <Clock className="w-2.5 h-2.5 opacity-80" />
                                                                                                            {timeStr}
                                                                                                        </span>
                                                                                                    </TooltipTrigger>
                                                                                                    <TooltipContent className="max-w-[300px] p-3 bg-card border-border shadow-2xl z-[100]">
                                                                                                        <div className="space-y-2">
                                                                                                            <div className="flex items-center justify-between">
                                                                                                                <span className="text-[10px] uppercase font-bold text-primary tracking-wider">Source {sourceNum}</span>
                                                                                                                <span className="text-[10px] font-mono opacity-60 bg-muted px-1 rounded">{timeStr}</span>
                                                                                                            </div>
                                                                                                            <p className="text-[11px] italic text-muted-foreground leading-relaxed line-clamp-4 leading-tight">
                                                                                                                &quot;{citation.text}&quot;
                                                                                                            </p>
                                                                                                            <div className="pt-1 flex justify-end border-t border-border/10">
                                                                                                                <span className="text-[9px] opacity-40 font-medium">Click to seek to {timeStr}</span>
                                                                                                            </div>
                                                                                                        </div>
                                                                                                    </TooltipContent>
                                                                                                </Tooltip>
                                                                                            );
                                                                                        }

                                                                                        return (
                                                                                            <span
                                                                                                key={nIdx}
                                                                                                className="inline-flex items-center justify-center bg-primary/20 text-primary px-1.5 py-0.5 rounded text-[10px] font-bold mx-0.5"
                                                                                            >
                                                                                                [{sourceNum}]
                                                                                            </span>
                                                                                        );
                                                                                    })}
                                                                                </span>
                                                                            );
                                                                        }
                                                                        return part;
                                                                    })}
                                                                </TooltipProvider>
                                                            ) : (
                                                                msg.content
                                                            )}
                                                        </div>
                                                    ) : (
                                                        <div className="flex gap-1 items-center h-5">
                                                            <div className="w-1.5 h-1.5 bg-foreground/20 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                                                            <div className="w-1.5 h-1.5 bg-foreground/20 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                                                            <div className="w-1.5 h-1.5 bg-foreground/20 rounded-full animate-bounce"></div>
                                                        </div>
                                                    )}

                                                    {msg.role === "assistant" && msg.metadata && (
                                                        <div className="mt-4 pt-3 border-t border-border/50 flex flex-wrap gap-x-4 gap-y-1 text-[10px] text-muted-foreground uppercase tracking-wider font-semibold">
                                                            <div className="flex items-center gap-1">
                                                                <Activity className="w-3 h-3" />
                                                                {msg.metadata.model}
                                                            </div>
                                                            <div className={cn(
                                                                "px-1.5 py-0.5 rounded-md",
                                                                msg.metadata.tier === 'pro' ? "bg-primary/10 text-primary" : "bg-muted text-muted-foreground"
                                                            )}>
                                                                {msg.metadata.tier === 'pro' ? 'Pro' : 'Standard'}
                                                            </div>
                                                            <div>RRF K: {msg.metadata.rrf_k}</div>
                                                            {msg.metadata.rerank_model && <div>Rerank: {msg.metadata.rerank_model}</div>}
                                                            <div className="ml-auto opacity-40">{msg.metadata.timestamp}</div>
                                                        </div>
                                                    )}

                                                    {msg.role === "assistant" && msg.citations && msg.citations.length > 0 && (
                                                        <div className="mt-4 space-y-2">
                                                            <p className="text-[10px] uppercase tracking-widest font-bold text-muted-foreground/60 border-b border-border/50 pb-1">Sources</p>
                                                            <div className="flex flex-col gap-2">
                                                                {msg.citations.map((cit, idx) => (
                                                                    <div
                                                                        key={idx}
                                                                        className="text-[11px] leading-relaxed p-2 rounded-lg bg-background/20 border border-border/30 hover:border-primary/30 transition-colors group/cit cursor-pointer active:scale-[0.98]"
                                                                        onClick={() => {
                                                                            if (audioRef.current) {
                                                                                audioRef.current.currentTime = cit.start;
                                                                                audioRef.current.play();
                                                                            }
                                                                        }}
                                                                    >
                                                                        <div className="flex items-start gap-2">
                                                                            <span className="font-bold text-primary flex-shrink-0 mt-0.5">[{idx + 1}]</span>
                                                                            <div>
                                                                                <p className="line-clamp-2 italic text-muted-foreground group-hover/cit:line-clamp-none transition-all cursor-help">
                                                                                    {cit.text}
                                                                                </p>
                                                                                <div className="mt-1 flex gap-2 text-[9px] opacity-60 font-mono">
                                                                                    <span className="flex items-center gap-0.5"><Clock className="w-2.5 h-2.5" />{formatTime(cit.start)}</span>
                                                                                    <span>{(cit.score * 100).toFixed(0)}% match</span>
                                                                                </div>
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                ))}
                                                            </div>
                                                        </div>
                                                    )}
                                                </div>
                                            </div>
                                        ))
                                    )}
                                </div>
                            </TabsContent>

                            <TabsContent value="transcript" className="m-0">
                                <div className="space-y-1">
                                    {transcript ? (
                                        [...transcript.segments]
                                            .sort((a, b) => a.start - b.start)
                                            .map((segment, i) => (
                                                <div
                                                    key={i}
                                                    className={cn(
                                                        "p-3 rounded-xl hover:bg-muted/30 cursor-pointer transition-all flex gap-4 items-start border border-transparent",
                                                        currentTime >= segment.start && currentTime <= segment.end && "bg-primary/5 border-primary/20"
                                                    )}
                                                    onClick={() => {
                                                        if (audioRef.current) {
                                                            audioRef.current.currentTime = segment.start;
                                                            audioRef.current.play();
                                                        }
                                                    }}
                                                >
                                                    <div className="text-[10px] font-mono text-muted-foreground w-12 pt-1 flex-shrink-0">
                                                        {formatTime(segment.start)}
                                                    </div>
                                                    <div className="text-sm py-1">
                                                        {segment.text}
                                                    </div>
                                                </div>
                                            ))
                                    ) : (
                                        <p className="text-center text-muted-foreground py-10 text-xs italic">Awaiting transcription...</p>
                                    )}
                                </div>
                            </TabsContent>

                            <TabsContent value="search" className="m-0 space-y-3">
                                {result && result.length > 0 ? (
                                    result.map((res, i) => (
                                        <div key={i} className="p-4 rounded-xl bg-muted/30 border border-border/50 group hover:border-primary/30 transition-colors">
                                            <p className="text-sm leading-relaxed mb-3">
                                                {res.text}
                                            </p>
                                            <div className="flex items-center gap-4 text-[10px] text-muted-foreground font-medium uppercase tracking-wider">
                                                <span className="flex items-center gap-1">
                                                    <Clock className="w-3 h-3" />
                                                    {formatTime(res.start)} - {formatTime(res.end)}
                                                </span>
                                                <span className="flex items-center gap-1">
                                                    <Zap className="w-3 h-3 text-amber-500" />
                                                    Match: {(res.score * 100).toFixed(0)}%
                                                </span>
                                                <Button
                                                    variant="secondary"
                                                    size="sm"
                                                    className="h-6 px-2 ml-auto text-[10px] opacity-0 group-hover:opacity-100 transition-opacity"
                                                    onClick={() => {
                                                        if (audioRef.current) {
                                                            audioRef.current.currentTime = res.start;
                                                            audioRef.current.play();
                                                        }
                                                    }}
                                                >
                                                    <Play className="w-2.5 h-2.5 mr-1" /> Play
                                                </Button>
                                            </div>
                                        </div>
                                    ))
                                ) : (
                                    <div className="text-center py-20 opacity-30">
                                        <Search className="w-12 h-12 mx-auto mb-4" />
                                        <p className="text-sm font-medium">Search across segments will appear here</p>
                                    </div>
                                )}
                            </TabsContent>

                            <TabsContent value="json" className="m-0">
                                <div className="relative group">
                                    <Button
                                        variant="secondary"
                                        size="icon"
                                        className="absolute top-2 right-2 h-7 w-7 opacity-0 group-hover:opacity-100 transition-opacity"
                                        onClick={handleCopyJson}
                                    >
                                        {copied ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Copy className="w-3.5 h-3.5" />}
                                    </Button>
                                    <pre className="p-4 rounded-xl bg-muted/30 border border-border/50 text-[11px] font-mono overflow-auto max-h-[500px]">
                                        {response || "// Execute a request to see raw output"}
                                    </pre>
                                </div>
                            </TabsContent>

                            <TabsContent value="logs" className="m-0">
                                <div className="space-y-2">
                                    {!currentTraceId ? (
                                        <div className="text-center py-20 opacity-30">
                                            <Terminal className="w-12 h-12 mx-auto mb-4" />
                                            <p className="text-sm font-medium">No active request</p>
                                        </div>
                                    ) : isLoadingObservability ? (
                                        <div className="flex items-center justify-center py-20">
                                            <div className="w-6 h-6 border-2 border-primary border-t-transparent rounded-full animate-spin"></div>
                                        </div>
                                    ) : currentLogs.length > 0 ? (
                                        <div className="space-y-3">
                                            {currentLogs.map((log) => (
                                                <div key={log.id} className="p-3 rounded-xl bg-muted/30 border border-border/50 font-mono text-[11px] space-y-1">
                                                    <div className="flex justify-between items-center opacity-60">
                                                        <span>{log.method} {log.path}</span>
                                                        <span>{log.latency_ms.toFixed(1)}ms</span>
                                                    </div>
                                                    <div className="flex justify-between items-center">
                                                        <span className={cn(
                                                            "font-bold",
                                                            log.status_code >= 400 ? "text-destructive" : "text-emerald-500"
                                                        )}>
                                                            HTTP {log.status_code}
                                                        </span>
                                                        <span>{new Date(log.created_at).toLocaleTimeString()}</span>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    ) : (
                                        <div className="text-center py-20 opacity-30">
                                            <p className="text-sm font-medium">No logs found for this request</p>
                                        </div>
                                    )}
                                </div>
                            </TabsContent>

                            <TabsContent value="trace" className="m-0 h-full">
                                <div className="h-full">
                                    {!currentTraceId ? (
                                        <div className="text-center py-20 opacity-30">
                                            <Activity className="w-12 h-12 mx-auto mb-4" />
                                            <p className="text-sm font-medium">No active request</p>
                                        </div>
                                    ) : isLoadingObservability ? (
                                        <div className="flex items-center justify-center py-20">
                                            <div className="w-6 h-6 border-2 border-primary border-t-transparent rounded-full animate-spin"></div>
                                        </div>
                                    ) : traceEvents.length > 0 ? (
                                        <div className="rounded-xl border border-border/50 overflow-hidden bg-muted/20">
                                            <TraceWaterfall events={traceEvents} />
                                        </div>
                                    ) : (
                                        <div className="text-center py-20 opacity-30">
                                            <p className="text-sm font-medium">No trace data available</p>
                                        </div>
                                    )}
                                </div>
                            </TabsContent>
                        </div>

                        {/* Unified Input Bar */}
                        <div className="p-4 pt-2 border-t border-border/50 bg-background/50 backdrop-blur-md">
                            <div className="relative flex items-end gap-2">
                                <div className="relative flex-1">
                                    <Textarea
                                        placeholder="Ask a question or search segments..."
                                        value={chatInput}
                                        onChange={(e) => {
                                            setChatInput(e.target.value);
                                        }}
                                        className="min-h-[44px] max-h-32 py-3 px-4 resize-none rounded-2xl bg-muted/50 border-border/50 focus:border-primary/50 text-sm"
                                        onKeyDown={(e) => {
                                            if (e.key === "Enter" && !e.shiftKey) {
                                                e.preventDefault();
                                                handleChatSend();
                                            }
                                        }}
                                    />
                                </div>
                                <Button
                                    size="icon"
                                    className="h-10 w-10 flex-shrink-0 rounded-xl"
                                    disabled={!chatInput.trim() || isLoading}
                                    onClick={() => handleChatSend()}
                                >
                                    {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
                                </Button>
                            </div>
                            <div className="flex items-center gap-4 mt-2 px-1">
                                <p className="text-[10px] text-muted-foreground">
                                    <span className="font-semibold text-foreground/50">Enter</span> to send
                                </p>
                                <div className="h-2 w-[1px] bg-border/50" />
                                <p className="text-[10px] text-muted-foreground">
                                    RAG enabled • {searchMode === "pro" ? "Pro Rerank" : "Standard Search"}
                                </p>
                            </div>
                        </div>
                    </Tabs>
                </div>
            </div>
        </div>
    );
}
