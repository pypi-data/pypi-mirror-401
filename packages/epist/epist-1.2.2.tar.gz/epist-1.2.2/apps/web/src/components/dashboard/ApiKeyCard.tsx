"use client"

import { useState, useEffect } from "react";
import { Key, Plus, Copy, Check, MoreVertical, Trash2, Pencil, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { api, ApiKey } from "@/lib/api";

const ApiKeyCard = () => {
    const [keys, setKeys] = useState<ApiKey[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [newKeyName, setNewKeyName] = useState("");
    const [generatedKey, setGeneratedKey] = useState<string | null>(null);
    const [copied, setCopied] = useState(false);
    const [isOpen, setIsOpen] = useState(false);
    const [renamingKey, setRenamingKey] = useState<{ id: string, name: string } | null>(null);

    const fetchKeys = async () => {
        try {
            const data = await api.getApiKeys();
            setKeys(data);
        } catch (error) {
            console.error("Failed to fetch API keys:", error);
            toast.error("Failed to load API keys");
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchKeys();
    }, []);

    const handleCreateKey = async () => {
        if (!newKeyName.trim()) return;

        try {
            const result = await api.createApiKey(newKeyName);
            setGeneratedKey(result.key || null);
            fetchKeys(); // Refresh list
            toast.success("API key created");
        } catch {
            toast.error("Failed to create API key");
        }
    };

    const handleCopyKey = async (key: string) => {
        await navigator.clipboard.writeText(key);
        setCopied(true);
        toast.success("API key copied to clipboard");
        setTimeout(() => setCopied(false), 2000);
    };

    const handleDeleteKey = async (id: string) => {
        try {
            await api.revokeApiKey(id);
            setKeys((prev) => prev.filter((key) => key.id !== id));
            toast.success("API key revoked");
        } catch {
            toast.error("Failed to revoke API key");
        }
    };

    const handleRenameKey = async () => {
        if (!renamingKey) return;
        try {
            await api.renameApiKey(renamingKey.id, renamingKey.name);
            fetchKeys();
            setRenamingKey(null);
            toast.success("API key renamed");
        } catch {
            toast.error("Failed to rename API key");
        }
    };

    const handleCloseDialog = () => {
        setIsOpen(false);
        setNewKeyName("");
        setGeneratedKey(null);
    };

    return (
        <div className="p-6 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50">
            <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                    <div className="p-2 rounded-lg bg-primary/10 border border-primary/20">
                        <Key className="w-4 h-4 text-primary" />
                    </div>
                    <div>
                        <h3 className="text-base font-semibold text-foreground">API Keys</h3>
                        <p className="text-xs text-muted-foreground">Manage your credentials</p>
                    </div>
                </div>

                <Dialog open={isOpen} onOpenChange={setIsOpen}>
                    <DialogTrigger asChild>
                        <Button size="sm" className="gap-2">
                            <Plus className="w-4 h-4" />
                            Create Key
                        </Button>
                    </DialogTrigger>
                    <DialogContent>
                        <DialogHeader>
                            <DialogTitle>{generatedKey ? "Your API Key" : "Create New API Key"}</DialogTitle>
                            <DialogDescription>
                                {generatedKey
                                    ? "Copy this key now. You won't be able to see it again."
                                    : "Give your API key a name to help you identify it later."}
                            </DialogDescription>
                        </DialogHeader>

                        {generatedKey ? (
                            <div className="space-y-4">
                                <div className="p-4 rounded-xl bg-card border border-border font-mono text-sm break-all">
                                    {generatedKey}
                                </div>
                                <Button
                                    className="w-full gap-2"
                                    variant="outline"
                                    onClick={() => handleCopyKey(generatedKey)}
                                >
                                    {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                                    {copied ? "Copied!" : "Copy to Clipboard"}
                                </Button>
                            </div>
                        ) : (
                            <div className="space-y-4">
                                <div className="space-y-2">
                                    <Label htmlFor="keyName">Key Name</Label>
                                    <Input
                                        id="keyName"
                                        placeholder="e.g., Production API"
                                        value={newKeyName}
                                        onChange={(e: React.ChangeEvent<HTMLInputElement>) => setNewKeyName(e.target.value)}
                                    />
                                </div>
                            </div>
                        )}

                        <DialogFooter>
                            {generatedKey ? (
                                <Button onClick={handleCloseDialog}>Done</Button>
                            ) : (
                                <>
                                    <Button variant="outline" onClick={handleCloseDialog}>
                                        Cancel
                                    </Button>
                                    <Button onClick={handleCreateKey} disabled={!newKeyName.trim()}>
                                        Generate Key
                                    </Button>
                                </>
                            )}
                        </DialogFooter>
                    </DialogContent>
                </Dialog>
            </div>

            {/* Keys List */}
            <div className="space-y-3">
                {isLoading ? (
                    <div className="flex justify-center py-8">
                        <Loader2 className="w-6 h-6 animate-spin text-primary/50" />
                    </div>
                ) : keys.length === 0 ? (
                    <div className="text-center py-8 text-muted-foreground text-sm">
                        No API keys yet. Create one to get started.
                    </div>
                ) : (
                    keys.map((key) => (
                        <div
                            key={key.id}
                            className="flex items-center justify-between p-4 rounded-xl bg-background/50 border border-border/50 hover:border-border transition-colors"
                        >
                            <div className="flex items-center gap-4">
                                <div className="p-2 rounded-lg bg-muted/50">
                                    <Key className="w-4 h-4 text-muted-foreground" />
                                </div>
                                <div className="min-w-0">
                                    <p className="text-sm font-medium text-foreground truncate">{key.name}</p>
                                    <p className="text-xs font-mono text-muted-foreground">{key.prefix}***</p>
                                </div>
                            </div>

                            <div className="flex items-center gap-4">
                                <div className="hidden sm:block text-right">
                                    <p className="text-xs text-muted-foreground">
                                        Created {key.created_at ? new Date(key.created_at).toLocaleDateString() : "Unknown"}
                                    </p>
                                    <p className="text-xs text-muted-foreground">
                                        {key.last_used_at ? `Last used ${new Date(key.last_used_at).toLocaleDateString()}` : "Never used"}
                                    </p>
                                </div>

                                <DropdownMenu>
                                    <DropdownMenuTrigger asChild>
                                        <Button variant="ghost" size="icon" className="h-8 w-8">
                                            <MoreVertical className="w-4 h-4" />
                                        </Button>
                                    </DropdownMenuTrigger>
                                    <DropdownMenuContent align="end">
                                        <DropdownMenuItem onClick={() => setRenamingKey({ id: key.id, name: key.name })}>
                                            <Pencil className="w-4 h-4 mr-2" />
                                            Rename
                                        </DropdownMenuItem>
                                        <DropdownMenuItem
                                            className="text-destructive"
                                            onClick={() => handleDeleteKey(key.id)}
                                        >
                                            <Trash2 className="w-4 h-4 mr-2" />
                                            Revoke
                                        </DropdownMenuItem>
                                    </DropdownMenuContent>
                                </DropdownMenu>
                            </div>
                        </div>
                    ))
                )}
            </div>

            <Dialog open={!!renamingKey} onOpenChange={(open) => !open && setRenamingKey(null)}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Rename API Key</DialogTitle>
                        <DialogDescription>
                            Enter a new name for this API key.
                        </DialogDescription>
                    </DialogHeader>
                    <div className="space-y-4 py-4">
                        <div className="space-y-2">
                            <Label htmlFor="renameKey">New Name</Label>
                            <Input
                                id="renameKey"
                                value={renamingKey?.name || ""}
                                onChange={(e) => setRenamingKey(prev => prev ? { ...prev, name: e.target.value } : null)}
                                autoFocus
                            />
                        </div>
                    </div>
                    <DialogFooter>
                        <Button variant="outline" onClick={() => setRenamingKey(null)}>Cancel</Button>
                        <Button onClick={handleRenameKey}>Save Changes</Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </div>
    );
};

export default ApiKeyCard;
