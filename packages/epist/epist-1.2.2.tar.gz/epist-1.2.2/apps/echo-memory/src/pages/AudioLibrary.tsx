import { useState } from "react";
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
import { Link } from "react-router-dom";
import { toast } from "sonner";

type AudioStatus = "ready" | "processing" | "pending" | "failed";

interface AudioFile {
  id: string;
  title: string;
  status: AudioStatus;
  isPublic: boolean;
  createdAt: string;
  duration: string;
  size: string;
}

const mockAudioFiles: AudioFile[] = [
  { id: "1", title: "Q4 Product Strategy Meeting", status: "ready", isPublic: false, createdAt: "Dec 20, 2024", duration: "45:32", size: "42.3 MB" },
  { id: "2", title: "Customer Interview - Enterprise", status: "processing", isPublic: false, createdAt: "Dec 19, 2024", duration: "28:15", size: "26.1 MB" },
  { id: "3", title: "Team Standup Recording", status: "ready", isPublic: true, createdAt: "Dec 18, 2024", duration: "12:08", size: "11.2 MB" },
  { id: "4", title: "Podcast Episode Draft", status: "pending", isPublic: false, createdAt: "Dec 17, 2024", duration: "52:41", size: "48.7 MB" },
  { id: "5", title: "Sales Call - Acme Corp", status: "ready", isPublic: false, createdAt: "Dec 16, 2024", duration: "34:22", size: "31.8 MB" },
  { id: "6", title: "Product Demo Recording", status: "ready", isPublic: true, createdAt: "Dec 15, 2024", duration: "18:45", size: "17.3 MB" },
  { id: "7", title: "Weekly Planning Session", status: "failed", isPublic: false, createdAt: "Dec 14, 2024", duration: "41:18", size: "38.2 MB" },
  { id: "8", title: "User Research Interview #5", status: "ready", isPublic: false, createdAt: "Dec 13, 2024", duration: "55:02", size: "50.9 MB" },
];

const statusConfig: Record<AudioStatus, { label: string; className: string }> = {
  ready: { label: "Ready", className: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" },
  processing: { label: "Processing", className: "bg-blue-500/10 text-blue-400 border-blue-500/20 animate-pulse" },
  pending: { label: "Pending", className: "bg-muted text-muted-foreground border-border" },
  failed: { label: "Failed", className: "bg-red-500/10 text-red-400 border-red-500/20" },
};

const AudioLibrary = () => {
  const [viewMode, setViewMode] = useState<"grid" | "list">("list");
  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState<string>("all");

  const filteredFiles = mockAudioFiles.filter((file) => {
    const matchesSearch = file.title.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus = statusFilter === "all" || file.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const handleShare = (id: string) => {
    navigator.clipboard.writeText(`https://epist.ai/share/${id}`);
    toast.success("Share link copied to clipboard");
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
              <SelectItem value="ready">Ready</SelectItem>
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
            {filteredFiles.map((file) => (
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
                    <p className="text-xs text-muted-foreground sm:hidden">{file.duration}</p>
                  </div>
                </div>

                <div className="col-span-2">
                  <Badge variant="outline" className={cn("text-[10px]", statusConfig[file.status].className)}>
                    {statusConfig[file.status].label}
                  </Badge>
                </div>

                <div className="col-span-2 hidden sm:flex items-center gap-1 text-sm text-muted-foreground">
                  <Clock className="w-3 h-3" />
                  {file.duration}
                </div>

                <div className="col-span-2 hidden sm:block text-sm text-muted-foreground">
                  {file.createdAt}
                </div>

                <div className="col-span-1 flex items-center justify-end gap-2">
                  <Switch checked={file.isPublic} className="scale-75" />
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" size="icon" className="h-8 w-8 opacity-0 group-hover:opacity-100 transition-opacity">
                        <MoreVertical className="w-4 h-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem asChild>
                        <Link to={`/dashboard/playground?audio=${file.id}`}>
                          <Play className="w-4 h-4 mr-2" />
                          Open in Playground
                        </Link>
                      </DropdownMenuItem>
                      {file.isPublic && (
                        <DropdownMenuItem onClick={() => handleShare(file.id)}>
                          <Share2 className="w-4 h-4 mr-2" />
                          Share Link
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
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filteredFiles.map((file) => (
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
                      <Link to={`/dashboard/playground?audio=${file.id}`}>
                        <Play className="w-4 h-4 mr-2" />
                        Open in Playground
                      </Link>
                    </DropdownMenuItem>
                    <DropdownMenuItem className="text-destructive">
                      <Trash2 className="w-4 h-4 mr-2" />
                      Delete
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>

              <h3 className="text-sm font-medium text-foreground mb-2 line-clamp-2">{file.title}</h3>
              
              <div className="flex items-center gap-2 mb-3">
                <Badge variant="outline" className={cn("text-[10px]", statusConfig[file.status].className)}>
                  {statusConfig[file.status].label}
                </Badge>
              </div>

              <div className="flex items-center justify-between text-xs text-muted-foreground">
                <span>{file.duration}</span>
                <span>{file.size}</span>
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
};

export default AudioLibrary;
