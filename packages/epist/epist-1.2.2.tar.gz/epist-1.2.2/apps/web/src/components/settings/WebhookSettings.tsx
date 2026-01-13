"use client";

import { useState, useEffect } from "react";
import { Plus, Trash2, Copy, Check, Info } from "lucide-react";
import { api, Webhook } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
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
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import { Checkbox } from "@/components/ui/checkbox";

const AVAILABLE_EVENTS = [
    { id: "transcription.completed", label: "Transcription Completed" },
    { id: "transcription.failed", label: "Transcription Failed" },
    // Add more as needed
];

export function WebhookSettings() {
    const [webhooks, setWebhooks] = useState<Webhook[]>([]);
    const [loading, setLoading] = useState(true);
    const [isCreateOpen, setIsCreateOpen] = useState(false);

    // Form state
    const [newUrl, setNewUrl] = useState("");
    const [selectedEvents, setSelectedEvents] = useState<string[]>([]);
    const [creating, setCreating] = useState(false);

    // Secret display state
    const [createdWebhook, setCreatedWebhook] = useState<Webhook | null>(null);

    useEffect(() => {
        loadWebhooks();
    }, []);

    const loadWebhooks = async () => {
        try {
            setLoading(true);
            const data = await api.listWebhooks();
            setWebhooks(data);
        } catch (error) {
            toast.error("Failed to load webhooks");
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    const handleCreate = async () => {
        if (!newUrl) return toast.error("URL is required");
        if (selectedEvents.length === 0) return toast.error("Select at least one event");

        try {
            setCreating(true);
            const webhook = await api.createWebhook(newUrl, selectedEvents);
            setCreatedWebhook(webhook);
            setWebhooks([...webhooks, webhook]);
            setNewUrl("");
            setSelectedEvents([]);
            setIsCreateOpen(false); // Close request dialog, show secret dialog
        } catch (error) {
            toast.error("Failed to create webhook");
            console.error(error);
        } finally {
            setCreating(false);
        }
    };

    const handleDelete = async (id: string) => {
        if (!confirm("Are you sure you want to delete this webhook?")) return;
        try {
            await api.deleteWebhook(id);
            setWebhooks(webhooks.filter(w => w.id !== id));
            toast.success("Webhook deleted");
        } catch (error) {
            toast.error("Failed to delete webhook");
            console.error(error);
        }
    };

    const copySecret = () => {
        if (createdWebhook?.secret) {
            navigator.clipboard.writeText(createdWebhook.secret);
            toast.success("Secret copied to clipboard");
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h3 className="text-lg font-medium">Webhooks</h3>
                    <p className="text-sm text-muted-foreground">
                        Register URL endpoints to receive real-time updates about your audio processing.
                    </p>
                </div>
                <Dialog open={isCreateOpen} onOpenChange={setIsCreateOpen}>
                    <DialogTrigger asChild>
                        <Button className="gap-2">
                            <Plus className="w-4 h-4" />
                            Add Webhook
                        </Button>
                    </DialogTrigger>
                    <DialogContent>
                        <DialogHeader>
                            <DialogTitle>Add Webhook Endpoint</DialogTitle>
                            <DialogDescription>
                                Enter the URL where you want to receive webhook events.
                            </DialogDescription>
                        </DialogHeader>
                        <div className="space-y-4 py-4">
                            <div className="space-y-2">
                                <Label htmlFor="url">Endpoint URL</Label>
                                <Input
                                    id="url"
                                    placeholder="https://api.your-app.com/webhooks/epist"
                                    value={newUrl}
                                    onChange={(e) => setNewUrl(e.target.value)}
                                />
                            </div>
                            <div className="space-y-2">
                                <Label>Events</Label>
                                <div className="space-y-2 border rounded-md p-3">
                                    {AVAILABLE_EVENTS.map((event) => (
                                        <div key={event.id} className="flex items-center space-x-2">
                                            <Checkbox
                                                id={event.id}
                                                checked={selectedEvents.includes(event.id)}
                                                onCheckedChange={(checked) => {
                                                    if (checked) {
                                                        setSelectedEvents([...selectedEvents, event.id]);
                                                    } else {
                                                        setSelectedEvents(selectedEvents.filter(e => e !== event.id));
                                                    }
                                                }}
                                            />
                                            <Label htmlFor={event.id} className="font-normal cursor-pointer">
                                                {event.label} <code className="text-xs bg-muted px-1 rounded ml-1">{event.id}</code>
                                            </Label>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                        <DialogFooter>
                            <Button variant="outline" onClick={() => setIsCreateOpen(false)}>Cancel</Button>
                            <Button onClick={handleCreate} disabled={creating}>
                                {creating ? "Creating..." : "Create Webhook"}
                            </Button>
                        </DialogFooter>
                    </DialogContent>
                </Dialog>
            </div>

            {/* Secret Display Dialog */}
            <Dialog open={!!createdWebhook} onOpenChange={(open) => !open && setCreatedWebhook(null)}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Webhook Created Successfully</DialogTitle>
                        <DialogDescription>
                            Please copy your signing secret now. For security reasons, it will not be shown again.
                        </DialogDescription>
                    </DialogHeader>
                    <div className="space-y-4 py-4">
                        <div className="space-y-2">
                            <Label>Signing Secret</Label>
                            <div className="flex items-center gap-2">
                                <code className="flex-1 p-2 bg-muted rounded border font-mono text-sm break-all">
                                    {createdWebhook?.secret}
                                </code>
                                <Button size="icon" variant="outline" onClick={copySecret}>
                                    <Copy className="w-4 h-4" />
                                </Button>
                            </div>
                            <p className="text-xs text-muted-foreground flex items-center gap-1">
                                <Info className="w-3 h-3" />
                                Use this secret to verify the <code>Epist-Signature</code> header.
                            </p>
                        </div>
                    </div>
                    <DialogFooter>
                        <Button onClick={() => setCreatedWebhook(null)}>I have saved the secret</Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>

            <div className="border rounded-lg">
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>URL</TableHead>
                            <TableHead>Events</TableHead>
                            <TableHead>Status</TableHead>
                            <TableHead className="w-[50px]"></TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {loading ? (
                            <TableRow>
                                <TableCell colSpan={4} className="text-center py-8 text-muted-foreground">
                                    Loading...
                                </TableCell>
                            </TableRow>
                        ) : webhooks.length === 0 ? (
                            <TableRow>
                                <TableCell colSpan={4} className="text-center py-8 text-muted-foreground">
                                    No webhooks configured used.
                                </TableCell>
                            </TableRow>
                        ) : (
                            webhooks.map((webhook) => (
                                <TableRow key={webhook.id}>
                                    <TableCell className="font-mono text-sm">{webhook.url}</TableCell>
                                    <TableCell>
                                        <div className="flex flex-wrap gap-1">
                                            {webhook.events.map(e => (
                                                <Badge key={e} variant="secondary" className="text-xs font-normal">
                                                    {e}
                                                </Badge>
                                            ))}
                                        </div>
                                    </TableCell>
                                    <TableCell>
                                        <Badge variant={webhook.is_active ? "default" : "destructive"}>
                                            {webhook.is_active ? "Active" : "Inactive"}
                                        </Badge>
                                    </TableCell>
                                    <TableCell>
                                        <Button
                                            variant="ghost"
                                            size="icon"
                                            className="h-8 w-8 text-muted-foreground hover:text-destructive"
                                            onClick={() => handleDelete(webhook.id)}
                                        >
                                            <Trash2 className="w-4 h-4" />
                                        </Button>
                                    </TableCell>
                                </TableRow>
                            ))
                        )}
                    </TableBody>
                </Table>
            </div>
        </div>
    );
}
