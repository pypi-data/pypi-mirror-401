"use client";

import { useState, useEffect, useCallback } from "react";
import { Search, RefreshCw, Filter, Clock, Cpu, Database, Brain, ExternalLink, Box } from "lucide-react";
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
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { useAuth } from "@/components/auth/AuthProvider";

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

const statusConfig: Record<string, { label: string; className: string }> = {
    success: { label: "Success", className: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" },
    error: { label: "Error", className: "bg-destructive/10 text-destructive border-destructive/20" },
    warning: { label: "Warning", className: "bg-amber-500/10 text-amber-400 border-amber-500/20" },
};

const getStatusConfig = (status: string) => {
    return statusConfig[status.toLowerCase()] || {
        label: status.charAt(0).toUpperCase() + status.slice(1),
        className: "bg-muted text-muted-foreground border-border"
    };
};

const componentConfig: Record<string, { label: string; icon: typeof Cpu; color: string }> = {
    retriever: { label: "Retriever", icon: Database, color: "text-blue-400" },
    llm: { label: "LLM", icon: Brain, color: "text-purple-400" },
    embedder: { label: "Embedder", icon: Cpu, color: "text-cyan-400" },
    reranker: { label: "Reranker", icon: Filter, color: "text-amber-400" },
};

const getComponentConfig = (component: string) => {
    return componentConfig[component.toLowerCase()] || {
        label: component.charAt(0).toUpperCase() + component.slice(1),
        icon: Box,
        color: "text-muted-foreground"
    };
};

export default function TracesPage() {
    const { user, loading: authLoading } = useAuth();
    const router = useRouter();
    const [traces, setTraces] = useState<Trace[]>([]);
    const [searchQuery, setSearchQuery] = useState("");
    const [statusFilter, setStatusFilter] = useState<string>("all");
    const [componentFilter, setComponentFilter] = useState<string>("all");
    const [isRefreshing, setIsRefreshing] = useState(false);

    const fetchTraces = useCallback(async () => {
        if (!user) return;
        setIsRefreshing(true);
        try {
            const data = await api.getTraces(
                50,
                0,
                true // root only
            );

            const mappedTraces: Trace[] = data.map(t => ({
                id: t.id,
                traceId: t.trace_id,
                status: (t.status === 'error' ? 'error' : 'success') as TraceStatus,
                component: (t.component?.toLowerCase() || 'llm') as ComponentType,
                latency: t.latency_ms,
                timestamp: t.start_time,
                model: t.meta?.model as string | undefined
            }));

            setTraces(mappedTraces);
        } catch (error) {
            console.error("Failed to fetch traces:", error);
        } finally {
            setIsRefreshing(false);
        }
    }, [user]);

    useEffect(() => {
        if (!authLoading && user) {
            fetchTraces();
        }
    }, [user, authLoading, fetchTraces]);

    const filteredTraces = traces.filter((trace) => {
        const matchesSearch = trace.traceId.toLowerCase().includes(searchQuery.toLowerCase());
        const matchesStatus = statusFilter === "all" || trace.status === statusFilter;
        const matchesComponent = componentFilter === "all" || trace.component === componentFilter;
        return matchesSearch && matchesStatus && matchesComponent;
    });

    const formatTime = (timestamp: string) => {
        const date = new Date(timestamp);
        const now = new Date();
        const diffMs = now.getTime() - date.getTime();
        const diffSecs = Math.floor(diffMs / 1000);

        if (diffSecs < 5) return "Just now";
        if (diffSecs < 60) return `${diffSecs}s ago`;
        if (diffSecs < 3600) return `${Math.floor(diffSecs / 60)}m ago`;
        if (diffSecs < 86400) return `${Math.floor(diffSecs / 3600)}h ago`;
        return date.toLocaleDateString();
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
                    onClick={() => fetchTraces()}
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
                            const componentData = getComponentConfig(trace.component);
                            const statusData = getStatusConfig(trace.status);
                            const ComponentIcon = componentData.icon;
                            return (
                                <div
                                    key={trace.id}
                                    onClick={() => router.push(`/dashboard/traces/detail?id=${trace.traceId}`)}
                                    className="grid md:grid-cols-[100px_1fr_140px_100px_120px_80px] gap-4 px-6 py-4 hover:bg-background/30 transition-colors cursor-pointer group"
                                >
                                    <div className="flex items-center">
                                        <Badge variant="outline" className={cn("text-xs", statusData.className)}>
                                            {statusData.label}
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
                                        <ComponentIcon className={cn("w-4 h-4", componentData.color)} />
                                        <span className="text-sm text-muted-foreground">{componentData.label}</span>
                                    </div>

                                    <div className="flex items-center gap-1.5">
                                        <Clock className="w-3.5 h-3.5 text-muted-foreground" />
                                        <span className={cn(
                                            "text-sm font-mono",
                                            trace.latency > 1000 ? "text-amber-400" : "text-foreground"
                                        )}>
                                            {trace.latency.toFixed(0)}ms
                                        </span>
                                    </div>

                                    <div className="flex items-center">
                                        <span className="text-sm text-muted-foreground">{formatTime(trace.timestamp)}</span>
                                    </div>

                                    <div className="flex items-center justify-end">
                                        <Button
                                            variant="ghost"
                                            size="icon"
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                router.push(`/dashboard/traces/detail?id=${trace.traceId}`);
                                            }}
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
                    <p className="text-2xl font-bold text-foreground">{traces.length}</p>
                </div>
                <div className="p-4 rounded-xl bg-card/50 backdrop-blur-xl border border-border/50">
                    <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">Success Rate</p>
                    <p className="text-2xl font-bold text-emerald-400">
                        {traces.length > 0
                            ? `${Math.round((traces.filter((t) => t.status === "success").length / traces.length) * 100)}%`
                            : "0%"}
                    </p>
                </div>
                <div className="p-4 rounded-xl bg-card/50 backdrop-blur-xl border border-border/50">
                    <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">Avg Latency</p>
                    <p className="text-2xl font-bold text-foreground">
                        {traces.length > 0
                            ? `${Math.round(traces.reduce((acc, t) => acc + t.latency, 0) / traces.length)}ms`
                            : "0ms"}
                    </p>
                </div>
                <div className="p-4 rounded-xl bg-card/50 backdrop-blur-xl border border-border/50">
                    <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">Errors</p>
                    <p className="text-2xl font-bold text-destructive">
                        {traces.filter((t) => t.status === "error").length}
                    </p>
                </div>
            </div>
        </div>
    );
}
