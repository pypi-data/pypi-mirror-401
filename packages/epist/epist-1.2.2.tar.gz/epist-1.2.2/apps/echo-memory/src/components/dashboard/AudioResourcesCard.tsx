import { Music, Play, Share2, Trash2, MoreVertical, ExternalLink } from "lucide-react";
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
import { Link } from "react-router-dom";
import { toast } from "sonner";

type AudioStatus = "ready" | "processing" | "pending" | "failed";

interface AudioResource {
  id: string;
  title: string;
  status: AudioStatus;
  isPublic: boolean;
  createdAt: string;
  duration: string;
}

const mockAudioResources: AudioResource[] = [
  {
    id: "1",
    title: "Q4 Product Strategy Meeting",
    status: "ready",
    isPublic: false,
    createdAt: "Dec 20, 2024",
    duration: "45:32",
  },
  {
    id: "2",
    title: "Customer Interview - Enterprise",
    status: "processing",
    isPublic: false,
    createdAt: "Dec 19, 2024",
    duration: "28:15",
  },
  {
    id: "3",
    title: "Team Standup Recording",
    status: "ready",
    isPublic: true,
    createdAt: "Dec 18, 2024",
    duration: "12:08",
  },
  {
    id: "4",
    title: "Podcast Episode Draft",
    status: "pending",
    isPublic: false,
    createdAt: "Dec 17, 2024",
    duration: "52:41",
  },
];

const statusConfig: Record<AudioStatus, { label: string; className: string }> = {
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
  const handleShare = (id: string) => {
    navigator.clipboard.writeText(`https://epist.ai/share/${id}`);
    toast.success("Share link copied to clipboard");
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

        <Link to="/dashboard/audio">
          <Button variant="ghost" size="sm" className="gap-2 text-muted-foreground">
            View All
            <ExternalLink className="w-3 h-3" />
          </Button>
        </Link>
      </div>

      {/* Audio List */}
      <div className="space-y-3">
        {mockAudioResources.map((audio) => (
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
                  {audio.duration} • {audio.createdAt}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <Badge
                variant="outline"
                className={cn("text-[10px] font-medium", statusConfig[audio.status].className)}
              >
                {statusConfig[audio.status].label}
              </Badge>

              <div className="hidden sm:flex items-center gap-2">
                <Switch
                  checked={audio.isPublic}
                  className="scale-75"
                  aria-label="Toggle visibility"
                />
                <span className="text-xs text-muted-foreground w-12">
                  {audio.isPublic ? "Public" : "Private"}
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
                    <Link to={`/dashboard/playground?audio=${audio.id}`}>
                      <Play className="w-4 h-4 mr-2" />
                      Open in Playground
                    </Link>
                  </DropdownMenuItem>
                  {audio.isPublic && (
                    <DropdownMenuItem onClick={() => handleShare(audio.id)}>
                      <Share2 className="w-4 h-4 mr-2" />
                      Share Public Link
                    </DropdownMenuItem>
                  )}
                  <DropdownMenuItem className="text-destructive">
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
  );
};

export default AudioResourcesCard;
