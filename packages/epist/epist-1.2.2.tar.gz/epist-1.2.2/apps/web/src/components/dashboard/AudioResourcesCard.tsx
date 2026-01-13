"use client"

import { Music, Play, Share2, Trash2, MoreVertical, ExternalLink, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import Link from "next/link";
import { toast } from "sonner";
import { api, AudioStatus } from "@/lib/api";
import { useEffect, useState } from "react";

const statusConfig: Record<string, { label: string; className: string }> = {
    ready: {
        label: "Ready",
        className: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
    },
    processing: {
        label: "Processing",
        className: "bg-blue-500/10 text-blue-400 border-blue-500/20 animate-pulse",
    },
    pending: {
        label: "Pending",
        className: "bg-muted text-muted-foreground border-border",
    },
    failed: {
        label: "Failed",
        className: "bg-red-500/10 text-red-400 border-red-500/20",
    },
};

const AudioResourcesCard = () => {
    const [resources, setResources] = useState<AudioStatus[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    const fetchResources = async () => {
        try {
            const data = await api.listAudio(5); // Only show latest 5
            setResources(data);
        } catch (error) {
            console.error("Failed to fetch audio resources:", error);
            toast.error("Failed to load audio resources");
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchResources();
    }, []);

    const handleShare = (id: string) => {
        // Use staging URL for demo purposes or window.location.origin
        const url = `${window.location.origin}/share/${id}`;
        navigator.clipboard.writeText(url);
        toast.success("Share link copied to clipboard");
    };

    const handleToggleVisibility = async (id: string, currentPublic: boolean | undefined) => {
        const nextPublic = !currentPublic;
        try {
            await api.updateAudio(id, { is_public: nextPublic });
            setResources(prev => prev.map(r => r.id === id ? { ...r, is_public: nextPublic } : r));
            toast.success(`Resource is now ${nextPublic ? 'public' : 'private'}`);
        } catch {
            toast.error("Failed to update visibility");
        }
    };

    const handleDelete = async (id: string) => {
        if (!confirm("Are you sure you want to delete this resource?")) return;
        try {
            await api.deleteAudio(id);
            setResources(prev => prev.filter(r => r.id !== id));
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

    return (
        <div className="p-6 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50">
            <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                    <div className="p-2 rounded-lg bg-primary/10 border border-primary/20">
                        <Music className="w-4 h-4 text-primary" />
                    </div>
                    <div>
                        <h3 className="text-base font-semibold text-foreground">Recent Audio</h3>
                        <p className="text-xs text-muted-foreground">Your latest uploads</p>
                    </div>
                </div>

                <Link href="/dashboard/audio">
                    <Button variant="ghost" size="sm" className="gap-2 text-muted-foreground">
                        View All
                        <ExternalLink className="w-3 h-3" />
                    </Button>
                </Link>
            </div>

            <div className="space-y-3">
                {isLoading ? (
                    <div className="flex justify-center py-8">
                        <Loader2 className="w-6 h-6 animate-spin text-primary/50" />
                    </div>
                ) : resources.length === 0 ? (
                    <div className="text-center py-8 text-muted-foreground text-sm">
                        No audio resources yet.
                    </div>
                ) : (
                    resources.map((audio) => (
                        <div
                            key={audio.id}
                            className="group flex items-center justify-between p-4 rounded-xl bg-background/50 border border-border/50 hover:border-border transition-all duration-200"
                        >
                            <div className="flex items-center gap-4 min-w-0 flex-1">
                                <div className="p-2 rounded-lg bg-muted/50 group-hover:bg-primary/10 transition-colors">
                                    <Music className="w-4 h-4 text-muted-foreground group-hover:text-primary transition-colors" />
                                </div>
                                <div className="min-w-0 flex-1">
                                    <p className="text-sm font-medium text-foreground truncate">{audio.title}</p>
                                    <p className="text-xs text-muted-foreground">
                                        {formatDuration(audio.meta_data?.duration as string)} • {new Date(audio.created_at).toLocaleDateString()}
                                    </p>
                                </div>
                            </div>

                            <div className="flex items-center gap-3">
                                <Badge
                                    variant="outline"
                                    className={cn("text-[10px] font-medium", statusConfig[audio.status]?.className || statusConfig.pending.className)}
                                >
                                    {statusConfig[audio.status]?.label || "Processing"}
                                </Badge>

                                <div className="hidden sm:flex items-center gap-2">
                                    <Switch
                                        checked={audio.is_public}
                                        onCheckedChange={() => handleToggleVisibility(audio.id, audio.is_public)}
                                        className="scale-75"
                                        aria-label="Toggle visibility"
                                    />
                                    <span className="text-xs text-muted-foreground w-12">
                                        {audio.is_public ? "Public" : "Private"}
                                    </span>
                                </div>

                                <DropdownMenu>
                                    <DropdownMenuTrigger asChild>
                                        <Button variant="ghost" size="icon" className="h-8 w-8 opacity-0 group-hover:opacity-100 transition-opacity">
                                            <MoreVertical className="w-4 h-4" />
                                        </Button>
                                    </DropdownMenuTrigger>
                                    <DropdownMenuContent align="end">
                                        <DropdownMenuItem asChild>
                                            <Link href={`/dashboard/playground?audio=${audio.id}`}>
                                                <Play className="w-4 h-4 mr-2" />
                                                Open in Playground
                                            </Link>
                                        </DropdownMenuItem>
                                        {audio.is_public && (
                                            <DropdownMenuItem onClick={() => handleShare(audio.id)}>
                                                <Share2 className="w-4 h-4 mr-2" />
                                                Share Public Link
                                            </DropdownMenuItem>
                                        )}
                                        <DropdownMenuItem className="text-destructive" onClick={() => handleDelete(audio.id)}>
                                            <Trash2 className="w-4 h-4 mr-2" />
                                            Delete
                                        </DropdownMenuItem>
                                    </DropdownMenuContent>
                                </DropdownMenu>
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default AudioResourcesCard;
