import { useState } from "react";
import { Search, RefreshCw, Filter, ChevronRight, Clock, Cpu, Database, Brain, ExternalLink } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { cn } from "@/lib/utils";

type TraceStatus = "success" | "error" | "warning";
type ComponentType = "retriever" | "llm" | "embedder" | "reranker";

interface Trace {
  id: string;
  traceId: string;
  status: TraceStatus;
  component: ComponentType;
  latency: number;
  timestamp: string;
  tokens?: number;
  model?: string;
}

const mockTraces: Trace[] = [
  { id: "1", traceId: "tr_8x7k2m9n4p5q1r3s", status: "success", component: "retriever", latency: 145, timestamp: "2024-12-22T10:30:00Z", tokens: 512 },
  { id: "2", traceId: "tr_2n4p5q1r3s8x7k2m", status: "success", component: "llm", latency: 892, timestamp: "2024-12-22T10:29:45Z", tokens: 2048, model: "gpt-4" },
  { id: "3", traceId: "tr_5q1r3s8x7k2m9n4p", status: "error", component: "embedder", latency: 45, timestamp: "2024-12-22T10:29:30Z" },
  { id: "4", traceId: "tr_1r3s8x7k2m9n4p5q", status: "success", component: "reranker", latency: 234, timestamp: "2024-12-22T10:29:15Z", tokens: 1024 },
  { id: "5", traceId: "tr_3s8x7k2m9n4p5q1r", status: "warning", component: "retriever", latency: 567, timestamp: "2024-12-22T10:29:00Z", tokens: 256 },
  { id: "6", traceId: "tr_8x7k2m9n4p5q1r3t", status: "success", component: "llm", latency: 1234, timestamp: "2024-12-22T10:28:45Z", tokens: 4096, model: "gpt-4" },
  { id: "7", traceId: "tr_9n4p5q1r3s8x7k2n", status: "success", component: "embedder", latency: 78, timestamp: "2024-12-22T10:28:30Z" },
  { id: "8", traceId: "tr_4p5q1r3s8x7k2m9o", status: "error", component: "llm", latency: 2100, timestamp: "2024-12-22T10:28:15Z", model: "gpt-4" },
];

const statusConfig: Record<TraceStatus, { label: string; className: string }> = {
  success: { label: "Success", className: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" },
  error: { label: "Error", className: "bg-destructive/10 text-destructive border-destructive/20" },
  warning: { label: "Warning", className: "bg-amber-500/10 text-amber-400 border-amber-500/20" },
};

const componentConfig: Record<ComponentType, { label: string; icon: typeof Cpu; color: string }> = {
  retriever: { label: "Retriever", icon: Database, color: "text-blue-400" },
  llm: { label: "LLM", icon: Brain, color: "text-purple-400" },
  embedder: { label: "Embedder", icon: Cpu, color: "text-cyan-400" },
  reranker: { label: "Reranker", icon: Filter, color: "text-amber-400" },
};

const Traces = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [componentFilter, setComponentFilter] = useState<string>("all");
  const [isRefreshing, setIsRefreshing] = useState(false);

  const filteredTraces = mockTraces.filter((trace) => {
    const matchesSearch = trace.traceId.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus = statusFilter === "all" || trace.status === statusFilter;
    const matchesComponent = componentFilter === "all" || trace.component === componentFilter;
    return matchesSearch && matchesStatus && matchesComponent;
  });

  const handleRefresh = () => {
    setIsRefreshing(true);
    setTimeout(() => setIsRefreshing(false), 1000);
  };

  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    
    if (diffMins < 1) return "Just now";
    if (diffMins < 60) return `${diffMins}m ago`;
    return date.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit" });
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground mb-1">Traces</h1>
          <p className="text-muted-foreground">Monitor system performance and request logs.</p>
        </div>
        <Button
          variant="outline"
          onClick={handleRefresh}
          className="gap-2"
        >
          <RefreshCw className={cn("w-4 h-4", isRefreshing && "animate-spin")} />
          Refresh
        </Button>
      </div>

      {/* Filters */}
      <div className="p-4 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input
              placeholder="Search by trace ID..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 bg-background/50 border-border/50"
            />
          </div>

          <Select value={statusFilter} onValueChange={setStatusFilter}>
            <SelectTrigger className="w-full sm:w-40 bg-background/50 border-border/50">
              <SelectValue placeholder="Status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Status</SelectItem>
              <SelectItem value="success">Success</SelectItem>
              <SelectItem value="error">Error</SelectItem>
              <SelectItem value="warning">Warning</SelectItem>
            </SelectContent>
          </Select>

          <Select value={componentFilter} onValueChange={setComponentFilter}>
            <SelectTrigger className="w-full sm:w-40 bg-background/50 border-border/50">
              <SelectValue placeholder="Component" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Components</SelectItem>
              <SelectItem value="retriever">Retriever</SelectItem>
              <SelectItem value="llm">LLM</SelectItem>
              <SelectItem value="embedder">Embedder</SelectItem>
              <SelectItem value="reranker">Reranker</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* Traces Table */}
      <div className="rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50 overflow-hidden">
        {/* Table Header */}
        <div className="hidden md:grid grid-cols-[100px_1fr_140px_100px_120px_80px] gap-4 px-6 py-3 bg-background/50 border-b border-border/50">
          <span className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Status</span>
          <span className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Trace ID</span>
          <span className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Component</span>
          <span className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Latency</span>
          <span className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Time</span>
          <span className="text-xs font-medium text-muted-foreground uppercase tracking-wide"></span>
        </div>

        {/* Table Body */}
        <div className="divide-y divide-border/50">
          {filteredTraces.length === 0 ? (
            <div className="p-12 text-center">
              <p className="text-muted-foreground">No traces found matching your filters.</p>
            </div>
          ) : (
            filteredTraces.map((trace) => {
              const ComponentIcon = componentConfig[trace.component].icon;
              return (
                <div
                  key={trace.id}
                  className="grid md:grid-cols-[100px_1fr_140px_100px_120px_80px] gap-4 px-6 py-4 hover:bg-background/30 transition-colors cursor-pointer group"
                >
                  <div className="flex items-center">
                    <Badge variant="outline" className={cn("text-xs", statusConfig[trace.status].className)}>
                      {statusConfig[trace.status].label}
                    </Badge>
                  </div>

                  <div className="flex items-center gap-2">
                    <code className="text-sm font-mono text-foreground">{trace.traceId}</code>
                    {trace.model && (
                      <Badge variant="outline" className="text-xs bg-muted/50">
                        {trace.model}
                      </Badge>
                    )}
                  </div>

                  <div className="flex items-center gap-2">
                    <ComponentIcon className={cn("w-4 h-4", componentConfig[trace.component].color)} />
                    <span className="text-sm text-muted-foreground">{componentConfig[trace.component].label}</span>
                  </div>

                  <div className="flex items-center gap-1.5">
                    <Clock className="w-3.5 h-3.5 text-muted-foreground" />
                    <span className={cn(
                      "text-sm font-mono",
                      trace.latency > 1000 ? "text-amber-400" : "text-foreground"
                    )}>
                      {trace.latency}ms
                    </span>
                  </div>

                  <div className="flex items-center">
                    <span className="text-sm text-muted-foreground">{formatTime(trace.timestamp)}</span>
                  </div>

                  <div className="flex items-center justify-end">
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-8 w-8 opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                      <ExternalLink className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>

      {/* Summary Stats */}
      <div className="grid gap-4 md:grid-cols-4">
        <div className="p-4 rounded-xl bg-card/50 backdrop-blur-xl border border-border/50">
          <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">Total Traces</p>
          <p className="text-2xl font-bold text-foreground">{mockTraces.length}</p>
        </div>
        <div className="p-4 rounded-xl bg-card/50 backdrop-blur-xl border border-border/50">
          <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">Success Rate</p>
          <p className="text-2xl font-bold text-emerald-400">
            {Math.round((mockTraces.filter((t) => t.status === "success").length / mockTraces.length) * 100)}%
          </p>
        </div>
        <div className="p-4 rounded-xl bg-card/50 backdrop-blur-xl border border-border/50">
          <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">Avg Latency</p>
          <p className="text-2xl font-bold text-foreground">
            {Math.round(mockTraces.reduce((acc, t) => acc + t.latency, 0) / mockTraces.length)}ms
          </p>
        </div>
        <div className="p-4 rounded-xl bg-card/50 backdrop-blur-xl border border-border/50">
          <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">Errors</p>
          <p className="text-2xl font-bold text-destructive">
            {mockTraces.filter((t) => t.status === "error").length}
          </p>
        </div>
      </div>
    </div>
  );
};

export default Traces;
