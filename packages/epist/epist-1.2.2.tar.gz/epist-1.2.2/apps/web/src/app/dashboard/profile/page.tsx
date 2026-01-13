"use client";

import { useState, useEffect } from "react";
import { Copy, Check, Mail, Building2, Users, Crown, CreditCard, UserPlus, Trash2, Shield, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { useToast } from "@/hooks/use-toast";
import { cn } from "@/lib/utils";
import { useAuth } from "@/components/auth/AuthProvider";
import { api, AdminUser } from "@/lib/api";

const roleColors: Record<string, string> = {
    owner: "bg-amber-500/10 text-amber-400 border-amber-500/20",
    admin: "bg-primary/10 text-primary border-primary/20",
    member: "bg-muted text-muted-foreground border-border",
};

export default function ProfilePage() {
    const { profile, loading } = useAuth();
    const [copied, setCopied] = useState<string | null>(null);
    const [inviteEmail, setInviteEmail] = useState("");
    const [members, setMembers] = useState<AdminUser[]>([]);
    const [loadingMembers, setLoadingMembers] = useState(true);
    const [managingBilling, setManagingBilling] = useState(false);
    const { toast } = useToast();

    useEffect(() => {
        const fetchMembers = async () => {
            try {
                const data = await api.getMembers();
                setMembers(data);
            } catch (error) {
                console.error("Failed to fetch members:", error);
            } finally {
                setLoadingMembers(false);
            }
        };

        if (profile) {
            fetchMembers();
        }
    }, [profile]);

    const handleCopy = (text: string, label: string) => {
        navigator.clipboard.writeText(text);
        setCopied(label);
        toast({ title: "Copied!", description: `${label} copied to clipboard.` });
        setTimeout(() => setCopied(null), 2000);
    };

    const handleInvite = async () => {
        if (!inviteEmail.trim() || !inviteEmail.includes("@")) {
            toast({ title: "Invalid email", description: "Please enter a valid email address.", variant: "destructive" });
            return;
        }
        try {
            await api.inviteMember(inviteEmail);
            toast({ title: "Invitation sent", description: `Invite sent to ${inviteEmail}` });
            setInviteEmail("");
        } catch (error) {
            toast({ title: "Invite failed", description: "Failed to send invitation. Check permissions.", variant: "destructive" });
        }
    };

    const handleRevoke = async (id: string) => {
        try {
            await api.removeMember(id);
            setMembers(members.filter((m) => m.id !== id));
            toast({ title: "Member removed", description: "Team member access has been revoked." });
        } catch (error) {
            toast({ title: "Removal failed", description: "Failed to remove member.", variant: "destructive" });
        }
    };

    const handleManageBilling = async () => {
        setManagingBilling(true);
        try {
            const { url } = await api.createPortalSession();
            window.location.href = url;
        } catch (error) {
            console.error("Billing portal error:", error);
            toast({
                title: "Internal Error",
                description: "Billing isn't configured for this environment yet.",
                variant: "destructive"
            });
        } finally {
            setManagingBilling(false);
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-[400px]">
                <Loader2 className="w-8 h-8 animate-spin text-primary" />
            </div>
        );
    }

    if (!profile) {
        return (
            <div className="flex flex-col items-center justify-center min-h-[400px] gap-4">
                <Shield className="w-12 h-12 text-muted-foreground" />
                <h2 className="text-xl font-semibold">Authentication Required</h2>
                <p className="text-muted-foreground">Please sign in to view your profile.</p>
                <Button onClick={() => window.location.href = "/login"}>Sign In</Button>
            </div>
        );
    }

    const userId = profile.id;
    const userEmail = profile.email;
    const orgName = profile.organization?.name || "Personal Workspace";
    const tier = profile.organization?.tier || "free";
    const status = profile.organization?.subscription_status || "active";

    return (
        <div className="max-w-4xl mx-auto space-y-8">
            {/* Hero Header */}
            <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-primary/20 via-card to-card border border-border/50">
                <div className="absolute inset-0 bg-grid opacity-20" />
                <div className="absolute top-0 right-0 w-64 h-64 bg-primary/20 rounded-full blur-3xl" />

                <div className="relative p-8 flex items-center gap-6">
                    <div className="w-20 h-20 rounded-2xl bg-primary/20 border border-primary/30 flex items-center justify-center">
                        <span className="text-3xl font-bold text-primary">
                            {profile.full_name ? profile.full_name.split(' ').map((n: string) => n[0]).join('') : '??'}
                        </span>
                    </div>
                    <div>
                        <h1 className="text-2xl font-bold text-foreground mb-1">{profile.full_name || 'User'}</h1>
                        <p className="text-muted-foreground">{userEmail}</p>
                        <div className="flex items-center gap-2 mt-2">
                            <Badge variant="outline" className="bg-primary/10 text-primary border-primary/20 capitalize">
                                <Crown className="w-3 h-3 mr-1" />
                                {tier} Plan
                            </Badge>
                            <Badge variant="outline" className="bg-emerald-500/10 text-emerald-400 border-emerald-500/20 capitalize">
                                {status}
                            </Badge>
                        </div>
                    </div>
                </div>
            </div>

            {/* Info Cards Grid */}
            <div className="grid gap-6 md:grid-cols-2">
                {/* Identity Card */}
                <div className="p-6 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50">
                    <div className="flex items-center gap-3 mb-6">
                        <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
                            <Shield className="w-5 h-5 text-primary" />
                        </div>
                        <h2 className="text-lg font-semibold text-foreground">Identity</h2>
                    </div>

                    <div className="space-y-4">
                        <div>
                            <label className="text-xs font-medium text-muted-foreground uppercase tracking-wide">User ID</label>
                            <div className="mt-1.5 flex items-center gap-2">
                                <code className="flex-1 px-3 py-2 rounded-lg bg-background/50 border border-border/50 text-sm font-mono text-foreground">
                                    {userId}
                                </code>
                                <Button
                                    variant="ghost"
                                    size="icon"
                                    className="h-9 w-9"
                                    onClick={() => handleCopy(userId, "User ID")}
                                >
                                    {copied === "User ID" ? (
                                        <Check className="w-4 h-4 text-emerald-500" />
                                    ) : (
                                        <Copy className="w-4 h-4" />
                                    )}
                                </Button>
                            </div>
                        </div>

                        <div>
                            <label className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Email</label>
                            <div className="mt-1.5 flex items-center gap-3 px-3 py-2 rounded-lg bg-background/50 border border-border/50">
                                <Mail className="w-4 h-4 text-muted-foreground" />
                                <span className="text-sm text-foreground">{userEmail}</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Organization Card */}
                <div className="p-6 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50">
                    <div className="flex items-center gap-3 mb-6">
                        <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
                            <Building2 className="w-5 h-5 text-primary" />
                        </div>
                        <h2 className="text-lg font-semibold text-foreground">Organization</h2>
                    </div>

                    <div className="space-y-4">
                        <div>
                            <label className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Org Name</label>
                            <div className="mt-1.5 flex items-center gap-3 px-3 py-2 rounded-lg bg-background/50 border border-border/50">
                                <Building2 className="w-4 h-4 text-muted-foreground" />
                                <span className="text-sm text-foreground">{orgName}</span>
                            </div>
                        </div>

                        <div>
                            <label className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Members</label>
                            <div className="mt-1.5 flex items-center gap-3 px-3 py-2 rounded-lg bg-background/50 border border-border/50">
                                <Users className="w-4 h-4 text-muted-foreground" />
                                <span className="text-sm text-foreground">{members.length} team members</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Subscription Card */}
            <div className="p-6 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50">
                <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
                            <CreditCard className="w-5 h-5 text-primary" />
                        </div>
                        <h2 className="text-lg font-semibold text-foreground">Subscription</h2>
                    </div>
                    <div className="flex items-center gap-3">
                        {tier !== "pro" && (
                            <Button
                                className="gap-2 bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 text-white border-0"
                                onClick={() => window.location.href = "/pricing"}
                            >
                                <Crown className="w-4 h-4" />
                                Upgrade
                            </Button>
                        )}
                        {profile.organization?.stripe_customer_id && (
                            <Button
                                variant="outline"
                                className="gap-2"
                                onClick={handleManageBilling}
                                disabled={managingBilling}
                            >
                                {managingBilling ? <Loader2 className="w-4 h-4 animate-spin" /> : "Manage Billing"}
                            </Button>
                        )}
                    </div>
                </div>

                <div className="grid gap-6 md:grid-cols-3">
                    <div className="p-4 rounded-xl bg-background/50 border border-border/50">
                        <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-2">Current Plan</p>
                        <div className="flex items-center gap-2">
                            <Crown className="w-5 h-5 text-amber-500" />
                            <span className="text-lg font-semibold text-foreground capitalize">{tier}</span>
                        </div>
                    </div>

                    <div className="p-4 rounded-xl bg-background/50 border border-border/50">
                        <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-2">Status</p>
                        <Badge variant="outline" className="bg-emerald-500/10 text-emerald-400 border-emerald-500/20 capitalize">
                            {status}
                        </Badge>
                    </div>

                    <div className="p-4 rounded-xl bg-background/50 border border-border/50">
                        <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-2">Next Billing</p>
                        <span className="text-lg font-semibold text-foreground">
                            {profile.organization?.current_period_end ? new Date(profile.organization.current_period_end).toLocaleDateString() : 'N/A'}
                        </span>
                    </div>
                </div>
            </div>

            {/* Usage Stats Card */}
            <div className="p-6 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50">
                <div className="flex items-center gap-3 mb-6">
                    <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
                        <Loader2 className="w-5 h-5 text-primary" />
                    </div>
                    <h2 className="text-lg font-semibold text-foreground">Usage</h2>
                </div>

                <div className="space-y-6">
                    <div>
                        <div className="flex justify-between text-sm mb-2">
                            <span className="text-muted-foreground">Transcription Minutes</span>
                            <span className="font-medium">
                                Used: {((profile.organization?.monthly_audio_seconds || 0) / 60).toFixed(1)} / Limit: {
                                    (tier === "pro" ? 6000 : tier === "starter" ? 1200 : 300)
                                } mins
                                <span className="text-muted-foreground ml-2 font-normal">
                                    (Remaining: {(
                                        ((tier === "pro" ? 6000 : tier === "starter" ? 1200 : 300) * 60 - (profile.organization?.monthly_audio_seconds || 0)) / 60
                                    ).toFixed(1)} mins)
                                </span>
                            </span>
                        </div>
                        {/* Progress Bar */}
                        <div className="h-2 w-full bg-secondary rounded-full overflow-hidden">
                            <div
                                className="h-full bg-primary transition-all duration-500"
                                style={{
                                    width: `${Math.min(100, ((profile.organization?.monthly_audio_seconds || 0) / (
                                        (tier === "pro" ? 100 * 3600 : tier === "starter" ? 20 * 3600 : 5 * 3600)
                                    )) * 100)}%`
                                }}
                            />
                        </div>
                        <p className="text-xs text-muted-foreground mt-2">
                            Resets on {profile.organization?.usage_reset_at ? new Date(profile.organization.usage_reset_at).toLocaleDateString() : 'next billing cycle'}.
                        </p>
                    </div>
                </div>
            </div>

            {/* Team Management */}
            <div className="p-6 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50">
                <div className="flex items-center gap-3 mb-6">
                    <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
                        <Users className="w-5 h-5 text-primary" />
                    </div>
                    <h2 className="text-lg font-semibold text-foreground">Team Management</h2>
                </div>

                {/* Invite Form */}
                <div className="flex gap-3 mb-6">
                    <div className="relative flex-1">
                        <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                        <Input
                            type="email"
                            placeholder="Enter email to invite..."
                            value={inviteEmail}
                            onChange={(e) => setInviteEmail(e.target.value)}
                            className="pl-10 bg-background/50 border-border/50"
                            onKeyDown={(e) => e.key === "Enter" && handleInvite()}
                        />
                    </div>
                    <Button onClick={handleInvite} className="gap-2">
                        <UserPlus className="w-4 h-4" />
                        Send Invite
                    </Button>
                </div>

                <Separator className="mb-6" />

                {/* Members List */}
                <div className="space-y-3">
                    {loadingMembers ? (
                        <div className="flex items-center justify-center py-8">
                            <Loader2 className="w-6 h-6 animate-spin text-primary" />
                        </div>
                    ) : members.length === 0 ? (
                        <p className="text-sm text-muted-foreground text-center py-8">No other members in this organization.</p>
                    ) : members.map((member) => (
                        <div
                            key={member.id}
                            className="flex items-center justify-between p-4 rounded-xl bg-background/50 border border-border/50 hover:border-border transition-colors"
                        >
                            <div className="flex items-center gap-4">
                                <div className="w-10 h-10 rounded-full bg-primary/20 border border-primary/30 flex items-center justify-center">
                                    <span className="text-sm font-medium text-primary">
                                        {member.full_name ? member.full_name.split(" ").map((n: string) => n[0]).join("") : "?"}
                                    </span>
                                </div>
                                <div>
                                    <p className="text-sm font-medium text-foreground">{member.full_name}</p>
                                    <p className="text-xs text-muted-foreground">{member.email}</p>
                                </div>
                            </div>

                            <div className="flex items-center gap-3">
                                <Badge variant="outline" className={cn("capitalize", roleColors[member.role] || roleColors.member)}>
                                    {member.role}
                                </Badge>
                                {member.id !== profile.id && member.role !== "owner" && (
                                    <Button
                                        variant="ghost"
                                        size="icon"
                                        className="h-8 w-8 text-destructive hover:bg-destructive/10"
                                        onClick={() => handleRevoke(member.id)}
                                    >
                                        <Trash2 className="w-4 h-4" />
                                    </Button>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
