"use client";

import { useState, useEffect } from "react";
import { Key, Plus, Copy, Check, MoreVertical, Trash2, Pencil, Shield, Clock, Loader2 } from "lucide-react";
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
import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
    AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { api, ApiKey } from "@/lib/api";


export default function ApiKeysPage() {
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
            console.error("Failed to fetch keys:", error);
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
            const data = await api.createApiKey(newKeyName);
            setGeneratedKey(data.key || null);
            setKeys(prev => [data, ...prev]);
            toast.success("API key created successfully");
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
            toast.success("API key revoked successfully");
        } catch {
            toast.error("Failed to revoke API key");
        }
    };

    const handleRenameKey = async () => {
        if (!renamingKey) return;
        try {
            const updated = await api.renameApiKey(renamingKey.id, renamingKey.name);
            setKeys(prev => prev.map(k => k.id === updated.id ? updated : k));
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
        <div className="max-w-4xl mx-auto space-y-6">
            {/* Page Header */}
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
                <div>
                    <h1 className="text-2xl font-bold tracking-tight text-foreground mb-1">API Keys</h1>
                    <p className="text-muted-foreground">Manage your API credentials for integration.</p>
                </div>

                <Dialog open={isOpen} onOpenChange={setIsOpen}>
                    <DialogTrigger asChild>
                        <Button className="gap-2">
                            <Plus className="w-4 h-4" />
                            Create New Key
                        </Button>
                    </DialogTrigger>
                    <DialogContent>
                        <DialogHeader>
                            <DialogTitle>{generatedKey ? "Your New API Key" : "Create API Key"}</DialogTitle>
                            <DialogDescription>
                                {generatedKey
                                    ? "Make sure to copy your API key now. You won't be able to see it again!"
                                    : "Give your API key a descriptive name to identify it later."}
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
                                        placeholder="e.g., Production API, CI/CD"
                                        value={newKeyName}
                                        onChange={(e) => setNewKeyName(e.target.value)}
                                    />
                                </div>
                            </div>
                        )}

                        <DialogFooter>
                            {generatedKey ? (
                                <Button onClick={handleCloseDialog}>Done</Button>
                            ) : (
                                <>
                                    <Button variant="outline" onClick={handleCloseDialog}>Cancel</Button>
                                    <Button onClick={handleCreateKey} disabled={!newKeyName.trim()}>Generate Key</Button>
                                </>
                            )}
                        </DialogFooter>
                    </DialogContent>
                </Dialog>
            </div>

            {/* Security Notice */}
            <div className="flex items-start gap-4 p-4 rounded-2xl bg-amber-500/10 border border-amber-500/20">
                <Shield className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
                <div>
                    <p className="text-sm font-medium text-amber-400 mb-1">Keep your keys secure</p>
                    <p className="text-xs text-amber-400/80">
                        Never share your API keys in public repositories, client-side code, or with unauthorized users.
                        Rotate keys regularly and revoke any that may have been compromised.
                    </p>
                </div>
            </div>

            {/* Keys List */}
            <div className="rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50 overflow-hidden">
                {isLoading ? (
                    <div className="flex items-center justify-center py-16">
                        <Loader2 className="w-8 h-8 animate-spin text-primary/50" />
                    </div>
                ) : keys.length === 0 ? (
                    <div className="text-center py-16">
                        <Key className="w-12 h-12 text-muted-foreground/50 mx-auto mb-4" />
                        <p className="text-muted-foreground mb-4">No API keys yet</p>
                        <Button onClick={() => setIsOpen(true)} className="gap-2">
                            <Plus className="w-4 h-4" />
                            Create Your First Key
                        </Button>
                    </div>
                ) : (
                    <div className="divide-y divide-border/50">
                        {keys.map((key) => (
                            <div
                                key={key.id}
                                className="flex items-center justify-between p-6 hover:bg-muted/30 transition-colors group"
                            >
                                <div className="flex items-center gap-4">
                                    <div className="p-3 rounded-xl bg-primary/10 border border-primary/20 group-hover:bg-primary/20 transition-colors">
                                        <Key className="w-5 h-5 text-primary" />
                                    </div>
                                    <div>
                                        <p className="text-sm font-medium text-foreground mb-1">{key.name}</p>
                                        <p className="text-xs font-mono text-muted-foreground">{key.prefix}</p>
                                    </div>
                                </div>

                                <div className="flex items-center gap-6">
                                    <div className="hidden md:block text-right">
                                        <p className="text-xs text-muted-foreground flex items-center gap-1 justify-end mb-1">
                                            <Clock className="w-3 h-3" />
                                            Created {new Date(key.created_at).toLocaleDateString()}
                                        </p>
                                        <p className="text-xs text-muted-foreground">
                                            {key.last_used_at ? `Last used ${new Date(key.last_used_at).toLocaleDateString()}` : "Never used"}
                                        </p>
                                    </div>

                                    <DropdownMenu>
                                        <DropdownMenuTrigger asChild>
                                            <Button variant="ghost" size="icon" className="h-9 w-9">
                                                <MoreVertical className="w-4 h-4" />
                                            </Button>
                                        </DropdownMenuTrigger>
                                        <DropdownMenuContent align="end">
                                            <DropdownMenuItem onClick={() => handleCopyKey(key.prefix)}>
                                                <Copy className="w-4 h-4 mr-2" />
                                                Copy Prefix
                                            </DropdownMenuItem>
                                            <DropdownMenuItem onClick={() => setRenamingKey({ id: key.id, name: key.name })}>
                                                <Pencil className="w-4 h-4 mr-2" />
                                                Rename
                                            </DropdownMenuItem>
                                            <AlertDialog>
                                                <AlertDialogTrigger asChild>
                                                    <DropdownMenuItem
                                                        className="text-destructive"
                                                        onSelect={(e) => e.preventDefault()}
                                                    >
                                                        <Trash2 className="w-4 h-4 mr-2" />
                                                        Revoke Key
                                                    </DropdownMenuItem>
                                                </AlertDialogTrigger>
                                                <AlertDialogContent>
                                                    <AlertDialogHeader>
                                                        <AlertDialogTitle>Revoke API Key?</AlertDialogTitle>
                                                        <AlertDialogDescription>
                                                            This action cannot be undone. Any applications using this key will
                                                            immediately lose access.
                                                        </AlertDialogDescription>
                                                    </AlertDialogHeader>
                                                    <AlertDialogFooter>
                                                        <AlertDialogCancel>Cancel</AlertDialogCancel>
                                                        <AlertDialogAction
                                                            onClick={() => handleDeleteKey(key.id)}
                                                            className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
                                                        >
                                                            Revoke Key
                                                        </AlertDialogAction>
                                                    </AlertDialogFooter>
                                                </AlertDialogContent>
                                            </AlertDialog>
                                        </DropdownMenuContent>
                                    </DropdownMenu>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {/* Rename Dialog */}
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
}
