import { useState } from "react";
import { Key, Plus, Copy, Check, MoreVertical, Trash2, Pencil, Shield, Clock } from "lucide-react";
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
import { cn } from "@/lib/utils";

interface ApiKey {
  id: string;
  name: string;
  prefix: string;
  createdAt: string;
  lastUsed: string | null;
  permissions: string[];
}

const mockKeys: ApiKey[] = [
  {
    id: "1",
    name: "Production API",
    prefix: "sk-epist-prod-a1b2c3d4",
    createdAt: "Dec 15, 2024",
    lastUsed: "2 hours ago",
    permissions: ["read", "write"],
  },
  {
    id: "2",
    name: "Development",
    prefix: "sk-epist-dev-e5f6g7h8",
    createdAt: "Dec 10, 2024",
    lastUsed: "5 days ago",
    permissions: ["read"],
  },
  {
    id: "3",
    name: "CI/CD Pipeline",
    prefix: "sk-epist-ci-i9j0k1l2",
    createdAt: "Nov 28, 2024",
    lastUsed: "1 day ago",
    permissions: ["read", "write", "delete"],
  },
];

const ApiKeys = () => {
  const [keys, setKeys] = useState<ApiKey[]>(mockKeys);
  const [newKeyName, setNewKeyName] = useState("");
  const [generatedKey, setGeneratedKey] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const [isOpen, setIsOpen] = useState(false);

  const handleCreateKey = () => {
    if (!newKeyName.trim()) return;

    const newKey = `sk-epist-${newKeyName.toLowerCase().replace(/\s+/g, "-")}-${Math.random().toString(36).substring(2, 10)}${Math.random().toString(36).substring(2, 10)}`;
    setGeneratedKey(newKey);

    const apiKey: ApiKey = {
      id: Math.random().toString(36).substring(2),
      name: newKeyName,
      prefix: `sk-epist-${newKeyName.toLowerCase().substring(0, 4)}-****`,
      createdAt: new Date().toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" }),
      lastUsed: null,
      permissions: ["read", "write"],
    };

    setKeys((prev) => [...prev, apiKey]);
  };

  const handleCopyKey = async (key: string) => {
    await navigator.clipboard.writeText(key);
    setCopied(true);
    toast.success("API key copied to clipboard");
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDeleteKey = (id: string) => {
    setKeys((prev) => prev.filter((key) => key.id !== id));
    toast.success("API key revoked successfully");
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
        {keys.length === 0 ? (
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
                      Created {key.createdAt}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {key.lastUsed ? `Last used ${key.lastUsed}` : "Never used"}
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
                      <DropdownMenuItem>
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
    </div>
  );
};

export default ApiKeys;
