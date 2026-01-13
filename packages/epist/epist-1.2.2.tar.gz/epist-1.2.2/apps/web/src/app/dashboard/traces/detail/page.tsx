"use client";

import { useEffect, useState, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { ArrowLeft, Clock, Activity, AlertCircle, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { api, TraceEvent } from "@/lib/api";
import TraceWaterfall from "@/components/observability/TraceWaterfall";
import { useAuth } from "@/components/auth/AuthProvider";

function TraceDetailContent() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const id = searchParams.get("id");
    const { user, loading: authLoading } = useAuth();
    const [events, setEvents] = useState<TraceEvent[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchTraceDetails = async () => {
            if (!user || !id) return;
            setIsLoading(true);
            try {
                const data = await api.getTraceDetails(id);
                setEvents(data);
            } catch (err: unknown) {
                console.error("Failed to fetch trace details:", err);
                const apiError = err as { response?: { data?: { detail?: string } } };
                const message = apiError.response?.data?.detail || (err instanceof Error ? err.message : "Failed to load trace details");
                setError(message);
            } finally {
                setIsLoading(false);
            }
        };

        if (!authLoading && user && id) {
            fetchTraceDetails();
        }
    }, [id, user, authLoading]);

    if (!id) {
        return (
            <div className="max-w-2xl mx-auto mt-12 p-8 rounded-2xl bg-muted/30 border border-border/50 text-center">
                <AlertCircle className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
                <h2 className="text-xl font-semibold text-foreground mb-2">Missing Trace ID</h2>
                <p className="text-muted-foreground mb-6">No trace ID was provided in the URL.</p>
                <Button onClick={() => router.push("/dashboard/traces")} variant="outline">
                    <ArrowLeft className="w-4 h-4 mr-2" />
                    Back to Traces
                </Button>
            </div>
        );
    }

    if (isLoading) {
        return (
            <div className="flex flex-col items-center justify-center min-h-[400px] space-y-4">
                <Loader2 className="w-8 h-8 text-primary animate-spin" />
                <p className="text-muted-foreground animate-pulse">Loading trace sequence...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="max-w-2xl mx-auto mt-12 p-8 rounded-2xl bg-destructive/5 border border-destructive/20 text-center">
                <AlertCircle className="w-12 h-12 text-destructive mx-auto mb-4" />
                <h2 className="text-xl font-semibold text-foreground mb-2">Error Loading Trace</h2>
                <p className="text-muted-foreground mb-6">{error}</p>
                <Button onClick={() => router.back()} variant="outline">
                    <ArrowLeft className="w-4 h-4 mr-2" />
                    Go Back
                </Button>
            </div>
        );
    }

    const totalDuration = events.length > 0
        ? Math.max(...events.map(e => new Date(e.end_time).getTime())) -
        Math.min(...events.map(e => new Date(e.start_time).getTime()))
        : 0;

    const hasError = events.some(e => e.status === "error");

    return (
        <div className="max-w-[1600px] mx-auto space-y-6">
            {/* Header */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div className="flex items-center gap-4">
                    <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => router.back()}
                        className="rounded-full"
                    >
                        <ArrowLeft className="w-5 h-5" />
                    </Button>
                    <div>
                        <div className="flex items-center gap-3 mb-1">
                            <h1 className="text-2xl font-bold tracking-tight text-foreground">
                                Trace Details
                            </h1>
                            <Badge variant="outline" className="font-mono bg-muted/50">
                                {id.slice(0, 12)}...
                            </Badge>
                            {hasError && (
                                <Badge variant="destructive" className="gap-1">
                                    <AlertCircle className="w-3 h-3" />
                                    Error
                                </Badge>
                            )}
                        </div>
                        <div className="flex items-center gap-4 text-sm text-muted-foreground">
                            <div className="flex items-center gap-1.5">
                                <Clock className="w-4 h-4" />
                                {totalDuration.toFixed(2)}ms total
                            </div>
                            <div className="flex items-center gap-1.5">
                                <Activity className="w-4 h-4" />
                                {events.length} spans
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Waterfall View */}
            <div className="rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50 overflow-hidden shadow-2xl">
                <TraceWaterfall events={events} />
            </div>
        </div>
    );
}

export default function TraceDetailPage() {
    return (
        <Suspense fallback={
            <div className="flex flex-col items-center justify-center min-h-[400px] space-y-4">
                <Loader2 className="w-8 h-8 text-primary animate-spin" />
                <p className="text-muted-foreground animate-pulse">Initializing...</p>
            </div>
        }>
            <TraceDetailContent />
        </Suspense>
    );
}
