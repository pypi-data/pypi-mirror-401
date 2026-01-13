import { useState, useEffect, useRef } from "react";
import { Search, RefreshCw, Filter, Clock, AlertCircle, CheckCircle2, XCircle, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { cn } from "@/lib/utils";

type HttpMethod = "GET" | "POST" | "PUT" | "DELETE" | "PATCH";
type StatusCategory = "success" | "error" | "all";

interface LogEntry {
  id: string;
  method: HttpMethod;
  path: string;
  status: number;
  latency: number;
  timestamp: string;
  ip?: string;
}

const generateMockLogs = (): LogEntry[] => [
  { id: "1", method: "POST", path: "/api/v1/transcribe", status: 200, latency: 1234, timestamp: new Date().toISOString(), ip: "192.168.1.1" },
  { id: "2", method: "GET", path: "/api/v1/audio/abc123", status: 200, latency: 45, timestamp: new Date(Date.now() - 15000).toISOString(), ip: "10.0.0.5" },
  { id: "3", method: "POST", path: "/api/v1/search", status: 500, latency: 2100, timestamp: new Date(Date.now() - 30000).toISOString(), ip: "192.168.1.2" },
  { id: "4", method: "DELETE", path: "/api/v1/audio/def456", status: 204, latency: 89, timestamp: new Date(Date.now() - 45000).toISOString(), ip: "10.0.0.10" },
  { id: "5", method: "GET", path: "/api/v1/transcripts", status: 200, latency: 156, timestamp: new Date(Date.now() - 60000).toISOString(), ip: "192.168.1.3" },
  { id: "6", method: "POST", path: "/api/v1/chat", status: 429, latency: 12, timestamp: new Date(Date.now() - 90000).toISOString(), ip: "10.0.0.15" },
  { id: "7", method: "PUT", path: "/api/v1/audio/ghi789/visibility", status: 200, latency: 67, timestamp: new Date(Date.now() - 120000).toISOString(), ip: "192.168.1.4" },
  { id: "8", method: "GET", path: "/api/v1/health", status: 200, latency: 5, timestamp: new Date(Date.now() - 150000).toISOString(), ip: "10.0.0.20" },
  { id: "9", method: "POST", path: "/api/v1/embeddings", status: 401, latency: 23, timestamp: new Date(Date.now() - 180000).toISOString(), ip: "192.168.1.5" },
  { id: "10", method: "GET", path: "/api/v1/segments", status: 200, latency: 234, timestamp: new Date(Date.now() - 210000).toISOString(), ip: "10.0.0.25" },
];

const methodColors: Record<HttpMethod, string> = {
  GET: "text-emerald-400",
  POST: "text-blue-400",
  PUT: "text-amber-400",
  DELETE: "text-destructive",
  PATCH: "text-purple-400",
};

const Logs = () => {
  const [logs, setLogs] = useState<LogEntry[]>(generateMockLogs());
  const [searchQuery, setSearchQuery] = useState("");
  const [timeRange, setTimeRange] = useState("1h");
  const [statusFilter, setStatusFilter] = useState<StatusCategory>("all");
  const [methodFilter, setMethodFilter] = useState<string>("all");
  const [autoRefresh, setAutoRefresh] = useState(false);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (autoRefresh) {
      intervalRef.current = setInterval(() => {
        handleRefresh();
      }, 5000);
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    }
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [autoRefresh]);

  const handleRefresh = () => {
    setIsRefreshing(true);
    setTimeout(() => {
      setLogs(generateMockLogs());
      setIsRefreshing(false);
    }, 500);
  };

  const filteredLogs = logs.filter((log) => {
    const matchesSearch = log.path.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus =
      statusFilter === "all" ||
      (statusFilter === "success" && log.status >= 200 && log.status < 400) ||
      (statusFilter === "error" && log.status >= 400);
    const matchesMethod = methodFilter === "all" || log.method === methodFilter;
    return matchesSearch && matchesStatus && matchesMethod;
  });

  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffSecs = Math.floor(diffMs / 1000);
    
    if (diffSecs < 5) return "Just now";
    if (diffSecs < 60) return `${diffSecs}s ago`;
    if (diffSecs < 3600) return `${Math.floor(diffSecs / 60)}m ago`;
    return date.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit" });
  };

  const getStatusIcon = (status: number) => {
    if (status >= 200 && status < 300) return <CheckCircle2 className="w-4 h-4 text-emerald-500" />;
    if (status >= 400 && status < 500) return <AlertCircle className="w-4 h-4 text-amber-500" />;
    if (status >= 500) return <XCircle className="w-4 h-4 text-destructive" />;
    return <CheckCircle2 className="w-4 h-4 text-muted-foreground" />;
  };

  const getStatusColor = (status: number) => {
    if (status >= 200 && status < 300) return "bg-emerald-500/10 text-emerald-400 border-emerald-500/20";
    if (status >= 400 && status < 500) return "bg-amber-500/10 text-amber-400 border-amber-500/20";
    if (status >= 500) return "bg-destructive/10 text-destructive border-destructive/20";
    return "bg-muted text-muted-foreground border-border";
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground mb-1">Logs</h1>
          <p className="text-muted-foreground">Real-time request logs for debugging and auditing.</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-card/50 border border-border/50">
            <Switch
              id="auto-refresh"
              checked={autoRefresh}
              onCheckedChange={setAutoRefresh}
            />
            <Label htmlFor="auto-refresh" className="text-sm text-muted-foreground cursor-pointer">
              Auto-refresh
            </Label>
            {autoRefresh && (
              <Loader2 className="w-3 h-3 text-primary animate-spin ml-1" />
            )}
          </div>
          <Button
            variant="outline"
            onClick={handleRefresh}
            className="gap-2"
            disabled={isRefreshing}
          >
            <RefreshCw className={cn("w-4 h-4", isRefreshing && "animate-spin")} />
            Refresh
          </Button>
        </div>
      </div>

      {/* Filters */}
      <div className="p-4 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50">
        <div className="flex flex-col lg:flex-row gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input
              placeholder="Search by path..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 bg-background/50 border-border/50"
            />
          </div>

          <Select value={timeRange} onValueChange={setTimeRange}>
            <SelectTrigger className="w-full lg:w-32 bg-background/50 border-border/50">
              <Clock className="w-4 h-4 mr-2 text-muted-foreground" />
              <SelectValue placeholder="Time" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="15m">15 min</SelectItem>
              <SelectItem value="1h">1 hour</SelectItem>
              <SelectItem value="24h">24 hours</SelectItem>
              <SelectItem value="all">All time</SelectItem>
            </SelectContent>
          </Select>

          <Select value={statusFilter} onValueChange={(v) => setStatusFilter(v as StatusCategory)}>
            <SelectTrigger className="w-full lg:w-32 bg-background/50 border-border/50">
              <SelectValue placeholder="Status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All</SelectItem>
              <SelectItem value="success">2xx/3xx</SelectItem>
              <SelectItem value="error">4xx/5xx</SelectItem>
            </SelectContent>
          </Select>

          <Select value={methodFilter} onValueChange={setMethodFilter}>
            <SelectTrigger className="w-full lg:w-32 bg-background/50 border-border/50">
              <SelectValue placeholder="Method" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All</SelectItem>
              <SelectItem value="GET">GET</SelectItem>
              <SelectItem value="POST">POST</SelectItem>
              <SelectItem value="PUT">PUT</SelectItem>
              <SelectItem value="DELETE">DELETE</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* Logs Table */}
      <div className="rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50 overflow-hidden">
        {/* Table Header */}
        <div className="hidden md:grid grid-cols-[60px_80px_1fr_80px_100px_100px] gap-4 px-6 py-3 bg-background/50 border-b border-border/50">
          <span className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Status</span>
          <span className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Method</span>
          <span className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Path</span>
          <span className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Code</span>
          <span className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Latency</span>
          <span className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Time</span>
        </div>

        {/* Table Body */}
        <div className="divide-y divide-border/50 max-h-[600px] overflow-y-auto">
          {filteredLogs.length === 0 ? (
            <div className="p-12 text-center">
              <Filter className="w-12 h-12 text-muted-foreground/30 mx-auto mb-4" />
              <p className="text-muted-foreground">No logs found matching your filters.</p>
            </div>
          ) : (
            filteredLogs.map((log) => (
              <div
                key={log.id}
                className="grid md:grid-cols-[60px_80px_1fr_80px_100px_100px] gap-4 px-6 py-3 hover:bg-background/30 transition-colors"
              >
                <div className="flex items-center">
                  {getStatusIcon(log.status)}
                </div>

                <div className="flex items-center">
                  <span className={cn("text-sm font-mono font-medium", methodColors[log.method])}>
                    {log.method}
                  </span>
                </div>

                <div className="flex items-center">
                  <code className="text-sm font-mono text-foreground truncate">{log.path}</code>
                </div>

                <div className="flex items-center">
                  <Badge variant="outline" className={cn("text-xs font-mono", getStatusColor(log.status))}>
                    {log.status}
                  </Badge>
                </div>

                <div className="flex items-center">
                  <span className={cn(
                    "text-sm font-mono",
                    log.latency > 1000 ? "text-amber-400" : "text-muted-foreground"
                  )}>
                    {log.latency}ms
                  </span>
                </div>

                <div className="flex items-center">
                  <span className="text-sm text-muted-foreground">{formatTime(log.timestamp)}</span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid gap-4 md:grid-cols-4">
        <div className="p-4 rounded-xl bg-card/50 backdrop-blur-xl border border-border/50">
          <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">Total Requests</p>
          <p className="text-2xl font-bold text-foreground">{logs.length}</p>
        </div>
        <div className="p-4 rounded-xl bg-card/50 backdrop-blur-xl border border-border/50">
          <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">Success Rate</p>
          <p className="text-2xl font-bold text-emerald-400">
            {Math.round((logs.filter((l) => l.status >= 200 && l.status < 400).length / logs.length) * 100)}%
          </p>
        </div>
        <div className="p-4 rounded-xl bg-card/50 backdrop-blur-xl border border-border/50">
          <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">Avg Latency</p>
          <p className="text-2xl font-bold text-foreground">
            {Math.round(logs.reduce((acc, l) => acc + l.latency, 0) / logs.length)}ms
          </p>
        </div>
        <div className="p-4 rounded-xl bg-card/50 backdrop-blur-xl border border-border/50">
          <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">Errors</p>
          <p className="text-2xl font-bold text-destructive">
            {logs.filter((l) => l.status >= 400).length}
          </p>
        </div>
      </div>
    </div>
  );
};

export default Logs;
