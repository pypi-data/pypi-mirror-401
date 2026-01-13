import { useState } from "react";
import { 
  Send, Loader2, Play, Pause, Clock, ChevronRight, Upload, Code, FileJson, 
  MessageSquare, Search, List, Settings2, Zap, ChevronDown, Copy, Check 
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import { Badge } from "@/components/ui/badge";
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
import { cn } from "@/lib/utils";
import { useToast } from "@/hooks/use-toast";

interface Citation {
  start: number;
  end: number;
  source: string;
  confidence: number;
}

interface QueryResult {
  text: string;
  citations: Citation[];
}

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

const sampleQueries = [
  "What were the key decisions made?",
  "Summarize the action items",
  "What concerns were raised?",
];

const sampleJsonConfig = `{
  "rag_enabled": true,
  "language": "en",
  "model": "whisper-large-v3",
  "diarization": true
}`;

const sampleResponse = {
  id: "audio_8x7k2m9n4p5q1r3s",
  status: "ready",
  duration: 378.5,
  segments: 42,
  transcript: {
    text: "The team discussed three main priorities for Q1...",
    confidence: 0.96
  }
};

const Playground = () => {
  const [query, setQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<QueryResult | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [inputMode, setInputMode] = useState<"upload" | "json">("upload");
  const [searchMode, setSearchMode] = useState<"standard" | "pro">("standard");
  const [advancedOpen, setAdvancedOpen] = useState(false);
  const [rrfK, setRrfK] = useState([60]);
  const [jsonConfig, setJsonConfig] = useState(sampleJsonConfig);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [chatInput, setChatInput] = useState("");
  const [copied, setCopied] = useState(false);
  const [outputTab, setOutputTab] = useState("json");
  const { toast } = useToast();

  const handleQuery = async () => {
    if (!query.trim()) return;
    
    setIsLoading(true);
    await new Promise((resolve) => setTimeout(resolve, 1500));
    
    setResult({
      text: `Based on the audio analysis, the team discussed three main priorities for Q1: improving the onboarding flow, launching the mobile app beta, and expanding the enterprise sales team. The timeline was set for mid-February, with Sarah leading the mobile initiative and David overseeing enterprise expansion.`,
      citations: [
        { start: 124.5, end: 138.2, source: "Q4 Strategy Meeting.mp3", confidence: 0.96 },
        { start: 245.8, end: 262.1, source: "Q4 Strategy Meeting.mp3", confidence: 0.92 },
      ],
    });
    
    setIsLoading(false);
  };

  const handleChatSend = async () => {
    if (!chatInput.trim()) return;
    
    const userMessage: ChatMessage = { role: "user", content: chatInput };
    setChatMessages([...chatMessages, userMessage]);
    setChatInput("");
    
    setIsLoading(true);
    await new Promise((resolve) => setTimeout(resolve, 1000));
    
    const assistantMessage: ChatMessage = {
      role: "assistant",
      content: "Based on the transcript, the team agreed to prioritize the mobile app launch. Sarah will lead development with a target release in February. They also discussed potential risks including limited QA resources."
    };
    setChatMessages(prev => [...prev, assistantMessage]);
    setIsLoading(false);
  };

  const handleCopyJson = () => {
    navigator.clipboard.writeText(JSON.stringify(sampleResponse, null, 2));
    setCopied(true);
    toast({ title: "Copied!", description: "JSON response copied to clipboard." });
    setTimeout(() => setCopied(false), 2000);
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, "0")}`;
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Page Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold tracking-tight text-foreground mb-1">Playground</h1>
        <p className="text-muted-foreground">Test APIs and query your audio library interactively.</p>
      </div>

      {/* Main Layout - Split View */}
      <div className="grid gap-6 lg:grid-cols-[1fr_1fr]">
        {/* Left Panel - Input */}
        <div className="space-y-4">
          {/* Mode Toggle */}
          <div className="p-4 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50">
            <div className="flex gap-2 mb-4">
              <Button
                variant={inputMode === "upload" ? "default" : "outline"}
                size="sm"
                onClick={() => setInputMode("upload")}
                className="gap-2"
              >
                <Upload className="w-4 h-4" />
                File Upload
              </Button>
              <Button
                variant={inputMode === "json" ? "default" : "outline"}
                size="sm"
                onClick={() => setInputMode("json")}
                className="gap-2"
              >
                <FileJson className="w-4 h-4" />
                JSON / URL
              </Button>
            </div>

            {inputMode === "upload" ? (
              <div className="border-2 border-dashed border-border/50 rounded-xl p-8 text-center hover:border-primary/30 transition-colors cursor-pointer">
                <Upload className="w-10 h-10 text-muted-foreground mx-auto mb-3" />
                <p className="text-sm text-foreground font-medium mb-1">Drop audio files here</p>
                <p className="text-xs text-muted-foreground">or click to browse (MP3, WAV, M4A)</p>
                <Button className="mt-4 gap-2">
                  <Zap className="w-4 h-4" />
                  Transcribe
                </Button>
              </div>
            ) : (
              <div className="space-y-4">
                <div>
                  <Label className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-2 block">
                    Configuration JSON
                  </Label>
                  <Textarea
                    value={jsonConfig}
                    onChange={(e) => setJsonConfig(e.target.value)}
                    className="min-h-[200px] font-mono text-sm bg-background/50 border-border/50"
                  />
                </div>
                <Button className="w-full gap-2">
                  <Send className="w-4 h-4" />
                  Execute Request
                </Button>
              </div>
            )}
          </div>

          {/* Controls / Tuning */}
          <div className="p-4 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold text-foreground">Search Settings</h3>
              <div className="flex gap-2">
                <Button
                  variant={searchMode === "standard" ? "default" : "outline"}
                  size="sm"
                  onClick={() => setSearchMode("standard")}
                >
                  Standard
                </Button>
                <Button
                  variant={searchMode === "pro" ? "default" : "outline"}
                  size="sm"
                  onClick={() => setSearchMode("pro")}
                  className="gap-1"
                >
                  <Zap className="w-3 h-3" />
                  Pro (Rerank)
                </Button>
              </div>
            </div>

            <Collapsible open={advancedOpen} onOpenChange={setAdvancedOpen}>
              <CollapsibleTrigger asChild>
                <Button variant="ghost" size="sm" className="w-full justify-between text-muted-foreground">
                  <span className="flex items-center gap-2">
                    <Settings2 className="w-4 h-4" />
                    Advanced Settings
                  </span>
                  <ChevronDown className={cn("w-4 h-4 transition-transform", advancedOpen && "rotate-180")} />
                </Button>
              </CollapsibleTrigger>
              <CollapsibleContent className="pt-4 space-y-4">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <Label className="text-xs text-muted-foreground">RRF K Value</Label>
                    <span className="text-xs font-mono text-foreground">{rrfK[0]}</span>
                  </div>
                  <Slider
                    value={rrfK}
                    onValueChange={setRrfK}
                    min={1}
                    max={100}
                    step={1}
                    className="w-full"
                  />
                </div>
                <div>
                  <Label className="text-xs text-muted-foreground mb-2 block">Rerank Model</Label>
                  <Select defaultValue="cohere">
                    <SelectTrigger className="bg-background/50 border-border/50">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="cohere">Cohere Rerank v3</SelectItem>
                      <SelectItem value="bge">BGE Reranker</SelectItem>
                      <SelectItem value="cross">Cross-Encoder</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </CollapsibleContent>
            </Collapsible>
          </div>

          {/* Query Input */}
          <div className="p-4 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50">
            <Label className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-2 block">
              Natural Language Query
            </Label>
            <div className="relative">
              <Textarea
                placeholder="Ask a question about your audio files..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="min-h-[100px] resize-none bg-background/50 border-border/50 focus:border-primary/50 pr-24"
                onKeyDown={(e) => {
                  if (e.key === "Enter" && e.metaKey) handleQuery();
                }}
              />
              <div className="absolute bottom-3 right-3">
                <Button
                  size="sm"
                  onClick={handleQuery}
                  disabled={!query.trim() || isLoading}
                  className="gap-2"
                >
                  {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                  Query
                </Button>
              </div>
            </div>
            <div className="flex flex-wrap gap-2 mt-3">
              <span className="text-xs text-muted-foreground">Try:</span>
              {sampleQueries.map((sample) => (
                <button
                  key={sample}
                  onClick={() => setQuery(sample)}
                  className="text-xs px-3 py-1.5 rounded-full bg-muted/50 text-muted-foreground hover:bg-muted hover:text-foreground transition-colors"
                >
                  {sample}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Right Panel - Output */}
        <div className="space-y-4">
          <div className="p-4 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50 min-h-[400px]">
            <Tabs value={outputTab} onValueChange={setOutputTab}>
              <TabsList className="bg-background/50 mb-4">
                <TabsTrigger value="json" className="gap-2">
                  <Code className="w-4 h-4" />
                  JSON
                </TabsTrigger>
                <TabsTrigger value="transcript" className="gap-2">
                  <List className="w-4 h-4" />
                  Transcript
                </TabsTrigger>
                <TabsTrigger value="search" className="gap-2">
                  <Search className="w-4 h-4" />
                  Search
                </TabsTrigger>
                <TabsTrigger value="chat" className="gap-2">
                  <MessageSquare className="w-4 h-4" />
                  Chat
                </TabsTrigger>
              </TabsList>

              <TabsContent value="json" className="mt-0">
                <div className="relative">
                  <Button
                    variant="ghost"
                    size="icon"
                    className="absolute top-2 right-2 h-8 w-8"
                    onClick={handleCopyJson}
                  >
                    {copied ? <Check className="w-4 h-4 text-emerald-500" /> : <Copy className="w-4 h-4" />}
                  </Button>
                  <pre className="p-4 rounded-xl bg-background/50 border border-border/50 text-sm font-mono text-foreground overflow-auto max-h-[400px]">
                    {JSON.stringify(sampleResponse, null, 2)}
                  </pre>
                </div>
              </TabsContent>

              <TabsContent value="transcript" className="mt-0">
                <div className="p-4 rounded-xl bg-background/50 border border-border/50">
                  <p className="text-sm text-foreground leading-relaxed">
                    The team gathered to discuss Q1 priorities. Sarah mentioned, "We need to focus on the mobile app launch - it's been delayed twice already." 
                    David responded, "I agree, but we also can't ignore the enterprise pipeline. We have three major deals in the works."
                    The discussion continued with specific timeline commitments...
                  </p>
                </div>
              </TabsContent>

              <TabsContent value="search" className="mt-0">
                {result ? (
                  <div className="space-y-4">
                    <p className="text-sm text-foreground leading-relaxed p-4 rounded-xl bg-background/50 border border-border/50">
                      {result.text}
                    </p>
                    <div className="space-y-2">
                      <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Sources</p>
                      <div className="flex flex-wrap gap-2">
                        {result.citations.map((citation, index) => (
                          <button
                            key={index}
                            className={cn(
                              "flex items-center gap-2 px-3 py-2 rounded-xl text-xs",
                              "bg-background/50 border border-border/50",
                              "hover:border-primary/30 hover:bg-primary/5 transition-all"
                            )}
                          >
                            <div className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                            <Clock className="w-3 h-3 text-muted-foreground" />
                            <span className="font-mono">{formatTime(citation.start)}</span>
                            <span className="text-muted-foreground">|</span>
                            <span className="text-muted-foreground truncate max-w-[120px]">{citation.source}</span>
                            <ChevronRight className="w-3 h-3 text-muted-foreground" />
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="flex flex-col items-center justify-center h-[300px] text-center">
                    <Search className="w-12 h-12 text-muted-foreground/30 mb-4" />
                    <p className="text-muted-foreground">Run a query to see search results</p>
                  </div>
                )}
              </TabsContent>

              <TabsContent value="chat" className="mt-0">
                <div className="flex flex-col h-[400px]">
                  <div className="flex-1 overflow-y-auto space-y-4 mb-4">
                    {chatMessages.length === 0 ? (
                      <div className="flex flex-col items-center justify-center h-full text-center">
                        <MessageSquare className="w-12 h-12 text-muted-foreground/30 mb-4" />
                        <p className="text-muted-foreground">Chat with your audio using RAG</p>
                      </div>
                    ) : (
                      chatMessages.map((msg, i) => (
                        <div
                          key={i}
                          className={cn(
                            "p-3 rounded-xl text-sm",
                            msg.role === "user"
                              ? "bg-primary/10 text-foreground ml-8"
                              : "bg-background/50 border border-border/50 mr-8"
                          )}
                        >
                          {msg.content}
                        </div>
                      ))
                    )}
                  </div>
                  <div className="flex gap-2">
                    <Input
                      placeholder="Ask a follow-up question..."
                      value={chatInput}
                      onChange={(e) => setChatInput(e.target.value)}
                      className="bg-background/50 border-border/50"
                      onKeyDown={(e) => e.key === "Enter" && handleChatSend()}
                    />
                    <Button onClick={handleChatSend} disabled={!chatInput.trim() || isLoading}>
                      <Send className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </TabsContent>
            </Tabs>
          </div>

          {/* Audio Player Preview */}
          <div className="p-4 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Karaoke Player</span>
              <Badge variant="outline" className="text-xs">Preview</Badge>
            </div>
            <div className="flex items-center gap-4">
              <Button
                size="icon"
                variant="outline"
                className="rounded-full h-12 w-12"
                onClick={() => setIsPlaying(!isPlaying)}
              >
                {isPlaying ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5 ml-0.5" />}
              </Button>

              <div className="flex-1">
                <div className="h-2 bg-border rounded-full overflow-hidden">
                  <div className="h-full w-1/3 bg-primary rounded-full transition-all" />
                </div>
                <div className="flex justify-between mt-1.5">
                  <span className="text-xs text-muted-foreground font-mono">2:04</span>
                  <span className="text-xs text-muted-foreground font-mono">6:18</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Playground;
