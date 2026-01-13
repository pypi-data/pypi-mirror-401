"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { Search, RefreshCw, Filter, Clock, AlertCircle, CheckCircle2, XCircle } from "lucide-react";
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

import { api } from "@/lib/api";
import { useAuth } from "@/components/auth/AuthProvider";

type HttpMethod = "GET" | "POST" | "PUT" | "DELETE" | "PATCH";
type StatusCategory = "success" | "error" | "all";
type TimeFormat = "relative" | "absolute";

interface LogEntry {
    id: string;
    method: HttpMethod;
    path: string;
    status: number;
    latency: number;
    timestamp: string;
    ip?: string;
}

const methodColors: Record<string, string> = {
    GET: "text-emerald-400",
    POST: "text-blue-400",
    PUT: "text-amber-400",
    DELETE: "text-destructive",
    PATCH: "text-purple-400",
};

const getMethodColor = (method: string) => {
    return methodColors[method.toUpperCase()] || "text-muted-foreground";
};

export default function LogsPage() {
    const { user, loading: authLoading } = useAuth();
    const [logs, setLogs] = useState<LogEntry[]>([]);
    const [searchQuery, setSearchQuery] = useState("");
    const [timeRange, setTimeRange] = useState("15m");
    const [statusFilter, setStatusFilter] = useState<StatusCategory>("all");
    const [methodFilter, setMethodFilter] = useState<string>("all");
    const [isRefreshing, setIsRefreshing] = useState(false);
    const [timeFormat, setTimeFormat] = useState<TimeFormat>("relative");


    const fetchLogs = useCallback(async (showRefreshing = true) => {
        if (!user) return;
        if (showRefreshing) setIsRefreshing(true);

        try {
            let startTime: string | undefined;
            if (timeRange !== "all") {
                const now = new Date();
                if (timeRange === "15m") now.setMinutes(now.getMinutes() - 15);
                else if (timeRange === "1h") now.setHours(now.getHours() - 1);
                else if (timeRange === "24h") now.setHours(now.getHours() - 24);
                startTime = now.toISOString();
            }

            const data = await api.getLogs(
                100,
                0,
                undefined,
                methodFilter !== "all" ? methodFilter : undefined,
                startTime
            );

            const mappedLogs: LogEntry[] = data.map(l => ({
                id: l.id,
                method: l.method as HttpMethod,
                path: l.path,
                status: l.status_code,
                latency: l.latency_ms,
                timestamp: l.created_at,
                ip: l.ip_address
            }));

            setLogs(mappedLogs);
        } catch (error) {
            console.error("Failed to fetch logs:", error);
        } finally {
            setIsRefreshing(false);
        }
    }, [user, timeRange, methodFilter]);

    useEffect(() => {
        if (!authLoading && user) {
            fetchLogs();

            // Set up auto-refresh every 30 seconds
            const interval = setInterval(() => {
                fetchLogs(false);
            }, 30000);

            return () => clearInterval(interval);
        }
    }, [user, authLoading, timeRange, methodFilter, fetchLogs]);

    const filteredLogs = logs.filter((log) => {
        const matchesSearch = log.path.toLowerCase().includes(searchQuery.toLowerCase());
        const matchesStatus =
            statusFilter === "all" ||
            (statusFilter === "success" && log.status >= 200 && log.status < 400) ||
            (statusFilter === "error" && log.status >= 400);
        return matchesSearch && matchesStatus;
    });

    const formatTime = (timestamp: string) => {
        const date = new Date(timestamp);
        if (timeFormat === "absolute") {
            return date.toLocaleString("en-US", {
                month: "short",
                day: "numeric",
                hour: "2-digit",
                minute: "2-digit",
                second: "2-digit",
                hour12: false
            });
        }

        const now = new Date();
        const diffMs = now.getTime() - date.getTime();
        const diffSecs = Math.floor(diffMs / 1000);

        if (diffSecs < 5) return "Just now";
        if (diffSecs < 60) return `${diffSecs}s ago`;
        if (diffSecs < 3600) return `${Math.floor(diffSecs / 60)}m ago`;
        if (diffSecs < 86400) return `${Math.floor(diffSecs / 3600)}h ago`;
        return date.toLocaleDateString();
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
                        <Label htmlFor="time-format" className="text-sm text-muted-foreground cursor-pointer">
                            Abs
                        </Label>
                        <Switch
                            id="time-format"
                            checked={timeFormat === "absolute"}
                            onCheckedChange={(checked) => setTimeFormat(checked ? "absolute" : "relative")}
                        />
                    </div>
                    <div className="hidden sm:flex items-center gap-2 px-3 py-2 rounded-lg bg-emerald-500/5 border border-emerald-500/10">
                        <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                        <span className="text-xs font-medium text-emerald-500">Live</span>
                    </div>
                    <Button
                        variant="outline"
                        onClick={() => fetchLogs()}
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
                            className="pl-12 bg-background/50 border-border/50"
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
                                    <span className={cn("text-sm font-mono font-medium", getMethodColor(log.method))}>
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
                                        {log.latency.toFixed(1)}ms
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
                        {logs.length > 0
                            ? `${Math.round((logs.filter((l) => l.status >= 200 && l.status < 400).length / logs.length) * 100)}%`
                            : "0%"}
                    </p>
                </div>
                <div className="p-4 rounded-xl bg-card/50 backdrop-blur-xl border border-border/50">
                    <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">Avg Latency</p>
                    <p className="text-2xl font-bold text-foreground">
                        {logs.length > 0
                            ? `${Math.round(logs.reduce((acc, l) => acc + l.latency, 0) / logs.length)}ms`
                            : "0ms"}
                    </p>
                </div>
                <div className="p-4 rounded-xl bg-card/50 backdrop-blur-xl border border-border/50">
                    <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">Errors</p>
                    <p className="text-2xl font-bold text-destructive">
                        {logs.filter((l) => l.status >= 400).length}
                    </p>
                </div>
            </div>
        </div >
    );
}
