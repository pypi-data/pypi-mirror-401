"use client";

import { User, Bell, Shield, Palette, CreditCard, LogOut, Webhook } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Separator } from "@/components/ui/separator";
import { cn } from "@/lib/utils";
import { useAuth } from "@/components/auth/AuthProvider";
import { WebhookSettings } from "@/components/settings/WebhookSettings";

const settingsSections = [
    { id: "profile", label: "Profile", icon: User },
    { id: "notifications", label: "Notifications", icon: Bell },
    { id: "security", label: "Security", icon: Shield },
    { id: "webhooks", label: "Enable Webhooks", icon: Webhook },
    { id: "appearance", label: "Appearance", icon: Palette },
    { id: "billing", label: "Billing", icon: CreditCard },
];

export default function SettingsPage() {
    const { profile } = useAuth();
    const [firstName, lastName] = profile?.full_name?.split(" ") || ["", ""];

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            {/* Page Header */}
            <div className="mb-8">
                <h1 className="text-2xl font-bold tracking-tight text-foreground mb-1">Settings</h1>
                <p className="text-muted-foreground">Manage your account preferences.</p>
            </div>

            <div className="grid lg:grid-cols-4 gap-6">
                {/* Sidebar Navigation */}
                <div className="lg:col-span-1">
                    <nav className="space-y-1 sticky top-24">
                        {settingsSections.map((section) => (
                            <a
                                key={section.id}
                                href={`#${section.id}`}
                                className={cn(
                                    "flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors",
                                    section.id === "profile"
                                        ? "bg-primary/10 text-primary border border-primary/20"
                                        : "text-muted-foreground hover:text-foreground hover:bg-muted/50"
                                )}
                            >
                                <section.icon className="w-4 h-4" />
                                {section.label}
                            </a>
                        ))}
                    </nav>
                </div>

                {/* Settings Content */}
                <div className="lg:col-span-3 space-y-8">
                    {/* Profile Section */}
                    <section id="profile" className="p-6 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50">
                        <h2 className="text-lg font-semibold text-foreground mb-6">Profile</h2>

                        <div className="flex items-center gap-6 mb-6">
                            <div className="w-20 h-20 rounded-full bg-primary/20 border-2 border-primary/30 flex items-center justify-center">
                                <User className="w-8 h-8 text-primary" />
                            </div>
                            <div>
                                <Button variant="outline" size="sm">Change Avatar</Button>
                                <p className="text-xs text-muted-foreground mt-2">JPG, PNG or GIF. Max 2MB.</p>
                            </div>
                        </div>

                        <div className="grid sm:grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <Label htmlFor="firstName">First Name</Label>
                                <Input id="firstName" defaultValue={firstName} className="bg-background/50" />
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="lastName">Last Name</Label>
                                <Input id="lastName" defaultValue={lastName} className="bg-background/50" />
                            </div>
                            <div className="space-y-2 sm:col-span-2">
                                <Label htmlFor="email">Email</Label>
                                <Input id="email" type="email" defaultValue={profile?.email || ""} className="bg-background/50" readOnly />
                                <p className="text-[10px] text-muted-foreground">Email cannot be changed directly.</p>
                            </div>
                        </div>

                        <div className="flex justify-end mt-6">
                            <Button>Save Changes</Button>
                        </div>
                    </section>

                    {/* Notifications Section */}
                    <section id="notifications" className="p-6 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50">
                        <h2 className="text-lg font-semibold text-foreground mb-6">Notifications</h2>

                        <div className="space-y-4">
                            {[
                                { title: "Email notifications", description: "Receive emails about your account activity" },
                                { title: "Processing alerts", description: "Get notified when audio processing completes" },
                                { title: "Weekly digest", description: "Receive a weekly summary of your usage" },
                                { title: "Marketing emails", description: "Receive updates about new features and tips" },
                            ].map((item, index) => (
                                <div key={index} className="flex items-center justify-between py-3">
                                    <div>
                                        <p className="text-sm font-medium text-foreground">{item.title}</p>
                                        <p className="text-xs text-muted-foreground">{item.description}</p>
                                    </div>
                                    <Switch defaultChecked={index < 2} />
                                </div>
                            ))}
                        </div>
                    </section>

                    {/* Webhooks Section */}
                    <section id="webhooks" className="p-6 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50">
                        <WebhookSettings />
                    </section>

                    {/* Security Section */}
                    <section id="security" className="p-6 rounded-2xl bg-card/50 backdrop-blur-xl border border-border/50">
                        <h2 className="text-lg font-semibold text-foreground mb-6">Security</h2>

                        <div className="space-y-6">
                            <div>
                                <Label className="text-sm font-medium">Password</Label>
                                <p className="text-xs text-muted-foreground mb-3">Last changed 30 days ago</p>
                                <Button variant="outline" size="sm">Change Password</Button>
                            </div>

                            <Separator />

                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="text-sm font-medium text-foreground">Two-factor authentication</p>
                                    <p className="text-xs text-muted-foreground">Add an extra layer of security</p>
                                </div>
                                <Button variant="outline" size="sm">Enable 2FA</Button>
                            </div>

                            <Separator />

                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="text-sm font-medium text-foreground">Active sessions</p>
                                    <p className="text-xs text-muted-foreground">Manage your active sessions</p>
                                </div>
                                <Button variant="outline" size="sm">View Sessions</Button>
                            </div>
                        </div>
                    </section>

                    {/* Danger Zone */}
                    <section className="p-6 rounded-2xl bg-destructive/5 border border-destructive/20">
                        <h2 className="text-lg font-semibold text-destructive mb-2">Danger Zone</h2>
                        <p className="text-sm text-muted-foreground mb-6">
                            Permanently delete your account and all associated data.
                        </p>
                        <Button variant="destructive" className="gap-2">
                            <LogOut className="w-4 h-4" />
                            Delete Account
                        </Button>
                    </section>
                </div>
            </div>
        </div>
    );
}
