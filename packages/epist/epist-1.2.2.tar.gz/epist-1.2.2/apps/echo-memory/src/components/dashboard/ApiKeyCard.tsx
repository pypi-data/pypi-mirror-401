import { useState } from "react";
import { Key, Plus, Copy, Check, MoreVertical, Trash2, Pencil } from "lucide-react";
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
import { cn } from "@/lib/utils";

interface ApiKey {
  id: string;
  name: string;
  prefix: string;
  createdAt: string;
  lastUsed: string | null;
}

const mockKeys: ApiKey[] = [
  {
    id: "1",
    name: "Production API",
    prefix: "sk-epist-prod-****",
    createdAt: "Dec 15, 2024",
    lastUsed: "2 hours ago",
  },
  {
    id: "2",
    name: "Development",
    prefix: "sk-epist-dev-****",
    createdAt: "Dec 10, 2024",
    lastUsed: "5 days ago",
  },
];

const ApiKeyCard = () => {
  const [keys, setKeys] = useState<ApiKey[]>(mockKeys);
  const [newKeyName, setNewKeyName] = useState("");
  const [generatedKey, setGeneratedKey] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const [isOpen, setIsOpen] = useState(false);

  const handleCreateKey = () => {
    if (!newKeyName.trim()) return;

    const newKey = `sk-epist-${newKeyName.toLowerCase().replace(/\s+/g, "-")}-${Math.random().toString(36).substring(2, 10)}`;
    setGeneratedKey(newKey);

    const apiKey: ApiKey = {
      id: Math.random().toString(36).substring(2),
      name: newKeyName,
      prefix: `sk-epist-${newKeyName.toLowerCase().substring(0, 4)}-****`,
      createdAt: new Date().toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" }),
      lastUsed: null,
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
    toast.success("API key revoked");
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
        {keys.length === 0 ? (
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
                <div>
                  <p className="text-sm font-medium text-foreground">{key.name}</p>
                  <p className="text-xs font-mono text-muted-foreground">{key.prefix}</p>
                </div>
              </div>

              <div className="flex items-center gap-4">
                <div className="hidden sm:block text-right">
                  <p className="text-xs text-muted-foreground">Created {key.createdAt}</p>
                  <p className="text-xs text-muted-foreground">
                    {key.lastUsed ? `Last used ${key.lastUsed}` : "Never used"}
                  </p>
                </div>

                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="icon" className="h-8 w-8">
                      <MoreVertical className="w-4 h-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem>
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
    </div>
  );
};

export default ApiKeyCard;
