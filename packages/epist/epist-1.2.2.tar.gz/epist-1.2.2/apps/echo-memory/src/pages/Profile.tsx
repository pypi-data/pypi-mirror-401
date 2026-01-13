import { useState } from "react";
import { Copy, Check, Mail, Building2, Users, Crown, CreditCard, UserPlus, Trash2, Shield } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { useToast } from "@/hooks/use-toast";
import { cn } from "@/lib/utils";

interface TeamMember {
  id: string;
  email: string;
  name: string;
  role: "owner" | "admin" | "member";
  joinedAt: string;
}

const mockMembers: TeamMember[] = [
  { id: "1", email: "john@example.com", name: "John Doe", role: "owner", joinedAt: "2024-01-15" },
  { id: "2", email: "sarah@example.com", name: "Sarah Wilson", role: "admin", joinedAt: "2024-02-20" },
  { id: "3", email: "mike@example.com", name: "Mike Chen", role: "member", joinedAt: "2024-03-10" },
];

const roleColors = {
  owner: "bg-amber-500/10 text-amber-400 border-amber-500/20",
  admin: "bg-primary/10 text-primary border-primary/20",
  member: "bg-muted text-muted-foreground border-border",
};

const Profile = () => {
  const [copied, setCopied] = useState<string | null>(null);
  const [inviteEmail, setInviteEmail] = useState("");
  const [members, setMembers] = useState<TeamMember[]>(mockMembers);
  const { toast } = useToast();

  const userId = "usr_8x7k2m9n4p5q1r3s";
  const userEmail = "developer@example.com";
  const orgName = "Acme Corp";

  const handleCopy = (text: string, label: string) => {
    navigator.clipboard.writeText(text);
    setCopied(label);
    toast({ title: "Copied!", description: `${label} copied to clipboard.` });
    setTimeout(() => setCopied(null), 2000);
  };

  const handleInvite = () => {
    if (!inviteEmail.trim() || !inviteEmail.includes("@")) {
      toast({ title: "Invalid email", description: "Please enter a valid email address.", variant: "destructive" });
      return;
    }
    toast({ title: "Invitation sent", description: `Invite sent to ${inviteEmail}` });
    setInviteEmail("");
  };

  const handleRevoke = (id: string) => {
    setMembers(members.filter((m) => m.id !== id));
    toast({ title: "Member removed", description: "Team member access has been revoked." });
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Hero Header */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-primary/20 via-card to-card border border-border/50">
        <div className="absolute inset-0 bg-grid opacity-20" />
        <div className="absolute top-0 right-0 w-64 h-64 bg-primary/20 rounded-full blur-3xl" />
        
        <div className="relative p-8 flex items-center gap-6">
          <div className="w-20 h-20 rounded-2xl bg-primary/20 border border-primary/30 flex items-center justify-center">
            <span className="text-3xl font-bold text-primary">JD</span>
          </div>
          <div>
            <h1 className="text-2xl font-bold text-foreground mb-1">John Doe</h1>
            <p className="text-muted-foreground">{userEmail}</p>
            <div className="flex items-center gap-2 mt-2">
              <Badge variant="outline" className="bg-primary/10 text-primary border-primary/20">
                <Crown className="w-3 h-3 mr-1" />
                Pro Plan
              </Badge>
              <Badge variant="outline" className="bg-emerald-500/10 text-emerald-400 border-emerald-500/20">
                Active
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
          <Button variant="outline" className="gap-2">
            Manage Billing
          </Button>
        </div>

        <div className="grid gap-6 md:grid-cols-3">
          <div className="p-4 rounded-xl bg-background/50 border border-border/50">
            <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-2">Current Plan</p>
            <div className="flex items-center gap-2">
              <Crown className="w-5 h-5 text-amber-500" />
              <span className="text-lg font-semibold text-foreground">Pro</span>
            </div>
          </div>

          <div className="p-4 rounded-xl bg-background/50 border border-border/50">
            <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-2">Status</p>
            <Badge variant="outline" className="bg-emerald-500/10 text-emerald-400 border-emerald-500/20">
              Active
            </Badge>
          </div>

          <div className="p-4 rounded-xl bg-background/50 border border-border/50">
            <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-2">Next Billing</p>
            <span className="text-lg font-semibold text-foreground">Jan 15, 2025</span>
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
          {members.map((member) => (
            <div
              key={member.id}
              className="flex items-center justify-between p-4 rounded-xl bg-background/50 border border-border/50 hover:border-border transition-colors"
            >
              <div className="flex items-center gap-4">
                <div className="w-10 h-10 rounded-full bg-primary/20 border border-primary/30 flex items-center justify-center">
                  <span className="text-sm font-medium text-primary">
                    {member.name.split(" ").map((n) => n[0]).join("")}
                  </span>
                </div>
                <div>
                  <p className="text-sm font-medium text-foreground">{member.name}</p>
                  <p className="text-xs text-muted-foreground">{member.email}</p>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <Badge variant="outline" className={cn("capitalize", roleColors[member.role])}>
                  {member.role}
                </Badge>
                {member.role !== "owner" && (
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
};

export default Profile;
