"use client";

import { useState, useEffect } from "react";
import {
    Music,
    Upload,
    Search,
    Grid,
    List,
    MoreVertical,
    Play,
    Share2,
    Trash2,
    Filter,
    Clock,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Switch } from "@/components/ui/switch";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { cn } from "@/lib/utils";
import Link from "next/link";
import { toast } from "sonner";

import { api, AudioStatus } from "@/lib/api";

export default function AudioPage() {
    const [audioFiles, setAudioFiles] = useState<AudioStatus[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [viewMode, setViewMode] = useState<"grid" | "list">("list");
    const [searchQuery, setSearchQuery] = useState("");
    const [statusFilter, setStatusFilter] = useState<string>("all");

    const fetchAudio = async () => {
        try {
            const data = await api.listAudio(100);
            setAudioFiles(data);
        } catch {
            console.error("Failed to fetch audio files");
            toast.error("Failed to load audio library");
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchAudio();
    }, []);

    const filteredFiles = audioFiles.filter((file) => {
        const matchesSearch = file.title.toLowerCase().includes(searchQuery.toLowerCase());
        const matchesStatus = statusFilter === "all" || file.status === statusFilter;
        return matchesSearch && matchesStatus;
    });

    const handleShare = (id: string) => {
        navigator.clipboard.writeText(`${window.location.origin}/share/${id}`);
        toast.success("Share link copied to clipboard");
    };

    const handleToggleVisibility = async (id: string, currentPublic: boolean | undefined) => {
        const nextPublic = !currentPublic;
        try {
            await api.updateAudio(id, { is_public: nextPublic });
            setAudioFiles(prev => prev.map(r => r.id === id ? { ...r, is_public: nextPublic } : r));
            toast.success(`Resource is now ${nextPublic ? 'public' : 'private'}`);
        } catch {
            toast.error("Failed to update visibility");
        }
    };

    const handleDelete = async (id: string) => {
        if (!confirm("Are you sure you want to delete this resource?")) return;
        try {
            await api.deleteAudio(id);
            setAudioFiles(prev => prev.filter(r => r.id !== id));
            toast.success("Resource deleted");
        } catch {
            toast.error("Failed to delete resource");
        }
    };

    const formatDuration = (seconds?: number | string) => {
        if (!seconds) return "0:00";
        const totalSeconds = Number(seconds);
        const mins = Math.floor(totalSeconds / 60);
        const secs = Math.floor(totalSeconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    const statusConfig: Record<string, { label: string; className: string }> = {
        completed: { label: "Completed", className: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" },
        processing: { label: "Processing", className: "bg-blue-500/10 text-blue-400 border-blue-500/20 animate-pulse" },
        pending: { label: "Pending", className: "bg-muted text-muted-foreground border-border" },
        failed: { label: "Failed", className: "bg-red-500/10 text-red-400 border-red-500/20" },
    };

    return (
        <div className="max-w-7xl mx-auto space-y-6">
            {/* Page Header */}
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
                <div>
                    <h1 className="text-2xl font-bold tracking-tight text-foreground mb-1">Audio Library</h1>
                    <p className="text-muted-foreground">Manage and organize your audio files.</p>
                </div>
                <Button className="gap-2">
                    <Upload className="w-4 h-4" />
                    Upload Audio
                </Button>
            </div>

            {/* Filters */}
            <div className="flex flex-col sm:flex-row gap-4">
                <div className="relative flex-1">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                    <Input
                        placeholder="Search audio files..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="pl-10 bg-card/50 border-border/50"
                    />
                </div>
                <div className="flex gap-2">
                    <Select value={statusFilter} onValueChange={setStatusFilter}>
                        <SelectTrigger className="w-[140px] bg-card/50 border-border/50">
                            <Filter className="w-4 h-4 mr-2" />
                            <SelectValue placeholder="Status" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="all">All Status</SelectItem>
                            <SelectItem value="completed">Completed</SelectItem>
                            <SelectItem value="processing">Processing</SelectItem>
                            <SelectItem value="pending">Pending</SelectItem>
                            <SelectItem value="failed">Failed</SelectItem>
                        </SelectContent>
                    </Select>

                    <div className="flex rounded-lg border border-border/50 bg-card/50 p-1">
                        <Button
                            variant={viewMode === "list" ? "secondary" : "ghost"}
                            size="icon"
                            className="h-8 w-8"
                            onClick={() => setViewMode("list")}
                        >
                            <List className="w-4 h-4" />
                        </Button>
                        <Button
                            variant={viewMode === "grid" ? "secondary" : "ghost"}
                            size="icon"
                            className="h-8 w-8"
                            onClick={() => setViewMode("grid")}
                        >
                            <Grid className="w-4 h-4" />
                        </Button>
                    </div>
                </div>
            </div>

            {/* File List/Grid */}
            {viewMode === "list" ? (
                <div className="rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50 overflow-hidden">
                    <div className="grid grid-cols-12 gap-4 px-6 py-3 border-b border-border/50 text-xs font-medium text-muted-foreground uppercase tracking-wide">
                        <div className="col-span-5">Name</div>
                        <div className="col-span-2">Status</div>
                        <div className="col-span-2 hidden sm:block">Duration</div>
                        <div className="col-span-2 hidden sm:block">Created</div>
                        <div className="col-span-1"></div>
                    </div>

                    <div className="divide-y divide-border/50">
                        {isLoading ? (
                            Array(5).fill(0).map((_, i) => (
                                <div key={i} className="h-16 bg-muted/20 animate-pulse" />
                            ))
                        ) : filteredFiles.map((file) => (
                            <div
                                key={file.id}
                                className="grid grid-cols-12 gap-4 px-6 py-4 items-center hover:bg-muted/30 transition-colors group"
                            >
                                <div className="col-span-5 flex items-center gap-3 min-w-0">
                                    <div className="p-2 rounded-lg bg-muted/50 group-hover:bg-primary/10 transition-colors">
                                        <Music className="w-4 h-4 text-muted-foreground group-hover:text-primary transition-colors" />
                                    </div>
                                    <div className="min-w-0">
                                        <p className="text-sm font-medium text-foreground truncate">{file.title}</p>
                                        <p className="text-xs text-muted-foreground sm:hidden">{formatDuration(file.meta_data?.duration as string)}</p>
                                    </div>
                                </div>

                                <div className="col-span-2">
                                    <Badge variant="outline" className={cn("text-[10px]", statusConfig[file.status]?.className || statusConfig.pending.className)}>
                                        {statusConfig[file.status]?.label || "Processing"}
                                    </Badge>
                                </div>

                                <div className="col-span-2 hidden sm:flex items-center gap-1 text-sm text-muted-foreground">
                                    <Clock className="w-3 h-3" />
                                    {formatDuration(file.meta_data?.duration as string)}
                                </div>

                                <div className="col-span-2 hidden sm:block text-sm text-muted-foreground">
                                    {new Date(file.created_at).toLocaleDateString()}
                                </div>

                                <div className="col-span-1 flex items-center justify-end gap-2">
                                    <Switch
                                        checked={file.is_public}
                                        onCheckedChange={() => handleToggleVisibility(file.id, file.is_public)}
                                        className="scale-75"
                                    />
                                    <DropdownMenu>
                                        <DropdownMenuTrigger asChild>
                                            <Button variant="ghost" size="icon" className="h-8 w-8 opacity-0 group-hover:opacity-100 transition-opacity">
                                                <MoreVertical className="w-4 h-4" />
                                            </Button>
                                        </DropdownMenuTrigger>
                                        <DropdownMenuContent align="end">
                                            <DropdownMenuItem asChild>
                                                <Link href={`/dashboard/playground?audio=${file.id}`}>
                                                    <Play className="w-4 h-4 mr-2" />
                                                    Open in Playground
                                                </Link>
                                            </DropdownMenuItem>
                                            {file.is_public && (
                                                <DropdownMenuItem onClick={() => handleShare(file.id)}>
                                                    <Share2 className="w-4 h-4 mr-2" />
                                                    Share Link
                                                </DropdownMenuItem>
                                            )}
                                            <DropdownMenuItem className="text-destructive" onClick={() => handleDelete(file.id)}>
                                                <Trash2 className="w-4 h-4 mr-2" />
                                                Delete
                                            </DropdownMenuItem>
                                        </DropdownMenuContent>
                                    </DropdownMenu>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                    {isLoading ? (
                        Array(8).fill(0).map((_, i) => (
                            <div key={i} className="h-48 rounded-2xl bg-card/50 animate-pulse border border-border/50" />
                        ))
                    ) : filteredFiles.map((file) => (
                        <div
                            key={file.id}
                            className="group p-4 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50 hover:border-border transition-all"
                        >
                            <div className="flex items-start justify-between mb-4">
                                <div className="p-3 rounded-xl bg-muted/50 group-hover:bg-primary/10 transition-colors">
                                    <Music className="w-6 h-6 text-muted-foreground group-hover:text-primary transition-colors" />
                                </div>
                                <DropdownMenu>
                                    <DropdownMenuTrigger asChild>
                                        <Button variant="ghost" size="icon" className="h-8 w-8">
                                            <MoreVertical className="w-4 h-4" />
                                        </Button>
                                    </DropdownMenuTrigger>
                                    <DropdownMenuContent align="end">
                                        <DropdownMenuItem asChild>
                                            <Link href={`/dashboard/playground?audio=${file.id}`}>
                                                <Play className="w-4 h-4 mr-2" />
                                                Open in Playground
                                            </Link>
                                        </DropdownMenuItem>
                                        {file.is_public && (
                                            <DropdownMenuItem onClick={() => handleShare(file.id)}>
                                                <Share2 className="w-4 h-4 mr-2" />
                                                Share Link
                                            </DropdownMenuItem>
                                        )}
                                        <DropdownMenuItem className="text-destructive" onClick={() => handleDelete(file.id)}>
                                            <Trash2 className="w-4 h-4 mr-2" />
                                            Delete
                                        </DropdownMenuItem>
                                    </DropdownMenuContent>
                                </DropdownMenu>
                            </div>

                            <h3 className="text-sm font-medium text-foreground mb-2 line-clamp-2">{file.title}</h3>

                            <div className="flex items-center gap-2 mb-3">
                                <Badge variant="outline" className={cn("text-[10px]", statusConfig[file.status]?.className || statusConfig.pending.className)}>
                                    {statusConfig[file.status]?.label || "Processing"}
                                </Badge>
                                <Switch
                                    checked={file.is_public}
                                    onCheckedChange={() => handleToggleVisibility(file.id, file.is_public)}
                                    className="scale-75 ml-auto"
                                />
                            </div>

                            <div className="flex items-center justify-between text-xs text-muted-foreground">
                                <div className="flex items-center gap-1">
                                    <Clock className="w-3 h-3" />
                                    {formatDuration(file.meta_data?.duration as string)}
                                </div>
                                <span>{new Date(file.created_at).toLocaleDateString()}</span>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {filteredFiles.length === 0 && (
                <div className="text-center py-16">
                    <Music className="w-12 h-12 text-muted-foreground/50 mx-auto mb-4" />
                    <p className="text-muted-foreground">No audio files found.</p>
                </div>
            )}
        </div>
    );
}
