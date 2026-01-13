"use client";

import { useMemo, useState, useCallback } from "react";
import { TraceEvent } from "@/lib/api";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronRight, ChevronDown, Info, AlertCircle, CheckCircle2, Cpu, Box, Activity, Clock } from "lucide-react";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";

interface TraceWaterfallProps {
    events: TraceEvent[];
}

interface TreeNode extends TraceEvent {
    children: TreeNode[];
    depth: number;
}

export default function TraceWaterfall({ events }: TraceWaterfallProps) {
    const [selectedSpan, setSelectedSpan] = useState<TraceEvent | null>(null);
    const [collapsedSpans, setCollapsedSpans] = useState<Set<string>>(new Set());

    // 1. Build the tree structure and calculate timeline metadata
    const { tree, startTime, totalDuration } = useMemo(() => {
        if (!events.length) return { tree: [], startTime: 0, totalDuration: 0 };

        const sorted = [...events].sort((a, b) => new Date(a.start_time).getTime() - new Date(b.start_time).getTime());
        const start = new Date(sorted[0].start_time).getTime();
        const end = Math.max(...sorted.map(e => new Date(e.end_time).getTime()));

        const nodeMap = new Map<string, TreeNode>();

        // Initialize nodes
        events.forEach(e => {
            nodeMap.set(e.span_id, { ...e, children: [], depth: 0 });
        });

        const rootNodes: TreeNode[] = [];

        // Build tree
        events.forEach(e => {
            const node = nodeMap.get(e.span_id)!;
            if (e.parent_span_id && nodeMap.has(e.parent_span_id)) {
                const parent = nodeMap.get(e.parent_span_id)!;
                parent.children.push(node);
            } else {
                rootNodes.push(node);
            }
        });

        // Calculate depths recursively
        const calcDepth = (nodes: TreeNode[], depth: number) => {
            nodes.sort((a, b) => new Date(a.start_time).getTime() - new Date(b.start_time).getTime());
            nodes.forEach(node => {
                node.depth = depth;
                calcDepth(node.children, depth + 1);
            });
        };
        calcDepth(rootNodes, 0);

        return { tree: rootNodes, startTime: start, totalDuration: end - start };
    }, [events]);

    const toggleExpand = useCallback((spanId: string) => {
        setCollapsedSpans(prev => {
            const next = new Set(prev);
            if (next.has(spanId)) next.delete(spanId);
            else next.add(spanId);
            return next;
        });
    }, []);

    // 2. Flatten the tree based on which nodes are collapsed
    const flatNodes = useMemo(() => {
        const flattenTree = (nodes: TreeNode[]): TreeNode[] => {
            let result: TreeNode[] = [];
            nodes.forEach(node => {
                result.push(node);
                if (!collapsedSpans.has(node.span_id)) {
                    result = result.concat(flattenTree(node.children));
                }
            });
            return result;
        };
        return flattenTree(tree);
    }, [tree, collapsedSpans]);

    if (!events.length) {
        return (
            <div className="flex h-full items-center justify-center text-muted-foreground p-12">
                <div className="text-center">
                    <Activity className="w-12 h-12 mx-auto opacity-20 mb-4" />
                    <p>No trace events found.</p>
                </div>
            </div>
        );
    }

    return (
        <div className="flex h-[75vh] min-h-[600px] overflow-hidden">
            <div className="flex-1 flex flex-col min-w-0 bg-background/30 overflow-hidden border-r border-border/50">
                <div className="flex-1 overflow-auto custom-scrollbar">
                    <div className="min-w-[1000px] h-full flex flex-col">
                        {/* Header Scale */}
                        <div className="sticky top-0 z-30 flex pl-[300px] bg-background/95 backdrop-blur-md border-b border-border/50 h-10 items-center text-[10px] font-medium text-muted-foreground uppercase tracking-widest">
                            <div className="flex-1 relative h-full flex items-center">
                                <span className="absolute left-0">0ms</span>
                                <div className="absolute left-1/4 h-3 border-l border-border/30" />
                                <span className="absolute left-1/4 -translate-x-1/2">{(totalDuration * 0.25).toFixed(0)}ms</span>
                                <div className="absolute left-1/2 h-4 border-l border-border/50" />
                                <span className="absolute left-1/2 -translate-x-1/2">{(totalDuration * 0.5).toFixed(0)}ms</span>
                                <div className="absolute left-3/4 h-3 border-l border-border/30" />
                                <span className="absolute left-3/4 -translate-x-1/2">{(totalDuration * 0.75).toFixed(0)}ms</span>
                                <span className="absolute right-4 text-primary/80">{totalDuration.toFixed(1)}ms</span>
                            </div>
                        </div>

                        <div className="p-2 pt-0 space-y-0.5">
                            {flatNodes.map((node, index) => {
                                const nodeStart = new Date(node.start_time).getTime();
                                const nodeDuration = node.latency_ms;

                                const offsetPct = ((nodeStart - startTime) / totalDuration) * 100;
                                const widthPct = Math.max((nodeDuration / totalDuration) * 100, 0.2);

                                const isSelected = selectedSpan?.span_id === node.span_id;
                                const hasChildren = node.children.length > 0;
                                const isExpanded = !collapsedSpans.has(node.span_id);

                                return (
                                    <motion.div
                                        key={node.span_id}
                                        initial={{ opacity: 0, y: 5 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ delay: index * 0.01 }}
                                        className={cn(
                                            "flex items-center group cursor-pointer rounded-lg transition-all duration-200 h-9",
                                            isSelected ? "bg-primary/10 ring-1 ring-primary/20 shadow-lg shadow-primary/5" : "hover:bg-accent/40"
                                        )}
                                        onClick={() => setSelectedSpan(node)}
                                    >
                                        {/* Name Column */}
                                        <div
                                            className="w-[300px] shrink-0 flex items-center gap-2 py-1.5 px-3 border-r border-border/20 h-full overflow-hidden bg-background/20 sticky left-0 z-10 backdrop-blur-sm"
                                            style={{ paddingLeft: `${node.depth * 16 + 12}px` }}
                                        >
                                            {hasChildren ? (
                                                <button
                                                    onClick={(e) => { e.stopPropagation(); toggleExpand(node.span_id); }}
                                                    className="w-5 h-5 flex items-center justify-center rounded-md hover:bg-white/10 text-muted-foreground transition-colors"
                                                >
                                                    {isExpanded ? <ChevronDown className="w-3.5 h-3.5" /> : <ChevronRight className="w-3.5 h-3.5" />}
                                                </button>
                                            ) : (
                                                <div className="w-5" />
                                            )}

                                            <div className="flex items-center gap-2 flex-1 min-w-0">
                                                <div className={cn(
                                                    "w-1.5 h-1.5 rounded-full shrink-0 shadow-[0_0_8px_rgba(var(--primary),0.5)]",
                                                    node.status === "error" ? "bg-destructive shadow-destructive/50" : "bg-primary"
                                                )} />
                                                <span className="text-[10px] font-mono text-muted-foreground/60 uppercase tracking-tighter shrink-0">
                                                    {node.component}
                                                </span>
                                                <span className="truncate text-xs font-medium text-foreground/90" title={node.name}>
                                                    {node.name}
                                                </span>
                                            </div>
                                        </div>

                                        {/* Timeline Column */}
                                        <div className="flex-1 relative h-full px-2 flex items-center group/timeline">
                                            {/* Grid line markers */}
                                            <div className="absolute left-[25%] top-0 bottom-0 border-l border-border/10 pointer-events-none" />
                                            <div className="absolute left-[50%] top-0 bottom-0 border-l border-border/10 pointer-events-none" />
                                            <div className="absolute left-[75%] top-0 bottom-0 border-l border-border/10 pointer-events-none" />

                                            <motion.div
                                                layoutId={`bar-${node.span_id}`}
                                                className={cn(
                                                    "absolute h-2.5 rounded-full shadow-sm relative",
                                                    node.status === "error"
                                                        ? "bg-gradient-to-r from-destructive/60 to-destructive shadow-destructive/20"
                                                        : "bg-gradient-to-r from-primary/60 to-primary shadow-primary/20",
                                                    isSelected && "ring-2 ring-white/20"
                                                )}
                                                style={{
                                                    left: `${offsetPct}%`,
                                                    width: `${widthPct}%`
                                                }}
                                            >
                                                {/* Tooltip on bar hover */}
                                                <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 hidden group-hover/timeline:block pointer-events-none z-50">
                                                    <div className="bg-popover text-popover-foreground px-2 py-1 rounded-md border border-border/60 text-[10px] whitespace-nowrap shadow-xl">
                                                        {node.latency_ms.toFixed(2)}ms
                                                    </div>
                                                </div>
                                            </motion.div>

                                            {/* Latency text shown when wider or on group hover */}
                                            {widthPct < 5 && (
                                                <span
                                                    className="absolute text-[9px] text-muted-foreground/40 font-mono transition-opacity group-hover:opacity-100 opacity-0 whitespace-nowrap"
                                                    style={{ left: `${offsetPct + widthPct + 0.5}%` }}
                                                >
                                                    {node.latency_ms.toFixed(1)}ms
                                                </span>
                                            )}
                                        </div>
                                    </motion.div>
                                );
                            })}
                        </div>
                    </div>
                </div>
            </div>

            {/* Sidebar Details */}
            <AnimatePresence mode="wait">
                {selectedSpan ? (
                    <motion.div
                        key="sidebar"
                        initial={{ x: 300, opacity: 0 }}
                        animate={{ x: 0, opacity: 1 }}
                        exit={{ x: 400, opacity: 0 }}
                        className="w-[400px] shrink-0 bg-background/80 backdrop-blur-xl flex flex-col overflow-hidden border-l border-border/50 shadow-2xl z-40"
                    >
                        <div className="p-5 border-b border-border/50 bg-accent/10">
                            <div className="flex items-start justify-between mb-2">
                                <h3 className="font-bold text-foreground leading-tight text-lg">{selectedSpan.name}</h3>
                                <button
                                    onClick={() => setSelectedSpan(null)}
                                    className="p-1 hover:bg-white/10 rounded-md text-muted-foreground"
                                >
                                    <ChevronRight className="w-5 h-5 rotate-180" />
                                </button>
                            </div>
                            <div className="flex items-center gap-2">
                                <code className="text-[10px] text-muted-foreground font-mono bg-muted/40 px-1.5 py-0.5 rounded">
                                    {selectedSpan.span_id}
                                </code>
                                <Badge variant={selectedSpan.status === "error" ? "destructive" : "outline"} className="text-[10px] h-4">
                                    {selectedSpan.status}
                                </Badge>
                            </div>
                        </div>

                        <div className="flex-1 overflow-y-auto p-5 space-y-8 custom-scrollbar">
                            <div className="grid grid-cols-2 gap-3">
                                <div className="bg-accent/10 p-3 rounded-xl border border-border/30">
                                    <div className="text-[10px] font-bold text-muted-foreground uppercase mb-1 flex items-center gap-1.5">
                                        <Cpu className="w-3 h-3" /> Component
                                    </div>
                                    <div className="text-sm font-semibold capitalize">{selectedSpan.component}</div>
                                </div>
                                <div className="bg-accent/10 p-3 rounded-xl border border-border/30">
                                    <div className="text-[10px] font-bold text-muted-foreground uppercase mb-1 flex items-center gap-1.5">
                                        <Clock className="w-3 h-3" /> Latency
                                    </div>
                                    <div className="text-sm font-semibold">{selectedSpan.latency_ms.toFixed(2)}ms</div>
                                </div>
                            </div>

                            {selectedSpan.error_message && (
                                <div className="space-y-2">
                                    <div className="text-[10px] font-bold text-destructive uppercase flex items-center gap-1.5">
                                        <AlertCircle className="w-3 h-3" /> Error Details
                                    </div>
                                    <div className="bg-destructive/10 border border-destructive/20 p-4 rounded-xl text-destructive-foreground text-xs font-mono break-all leading-relaxed">
                                        {selectedSpan.error_message}
                                    </div>
                                </div>
                            )}

                            {[
                                { title: "Inputs", data: selectedSpan.inputs, icon: Info },
                                { title: "Outputs", data: selectedSpan.outputs, icon: CheckCircle2 },
                                { title: "Metadata", data: selectedSpan.meta, icon: Box }
                            ].map((section) => (
                                section.data && Object.keys(section.data).length > 0 && (
                                    <div key={section.title} className="space-y-3">
                                        <div className="text-[10px] font-bold text-muted-foreground uppercase flex items-center gap-1.5">
                                            <section.icon className="w-3 h-3 text-primary" /> {section.title}
                                        </div>
                                        <div className="relative group">
                                            <pre className="bg-muted/30 p-4 rounded-2xl text-[11px] text-foreground/80 font-mono overflow-x-auto border border-border/20 max-h-[300px] leading-relaxed select-all custom-scrollbar">
                                                {JSON.stringify(section.data, null, 2)}
                                            </pre>
                                            <button
                                                className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity bg-primary/20 hover:bg-primary/40 text-[10px] px-2 py-1 rounded text-primary-foreground font-medium"
                                                onClick={() => navigator.clipboard.writeText(JSON.stringify(section.data, null, 2))}
                                            >
                                                copy
                                            </button>
                                        </div>
                                    </div>
                                )
                            ))}
                        </div>
                    </motion.div>
                ) : (
                    <motion.div
                        key="placeholder"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="w-[450px] shrink-0 flex flex-col items-center justify-center p-8 text-center text-muted-foreground border-l border-border/50"
                    >
                        <div className="w-16 h-16 bg-muted/30 rounded-full flex items-center justify-center mb-4">
                            <Activity className="w-8 h-8 opacity-20" />
                        </div>
                        <h4 className="font-semibold text-foreground/80 mb-2">No Span Selected</h4>
                        <p className="text-sm">Click on any segment in the waterfall to view detailed parameters and outputs.</p>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
