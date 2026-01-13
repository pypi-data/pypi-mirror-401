"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import {
    LayoutDashboard,
    Users,
    Building2,
    Activity,
    ChevronLeft,
    ChevronRight,
    AppWindow,
    ShieldCheck
} from "lucide-react";
import { useAuth } from "@/components/auth/AuthProvider";
import { Button } from "@/components/ui/button";

interface AdminLayoutProps {
    children: React.ReactNode;
}

export default function AdminLayout({ children }: AdminLayoutProps) {
    const { user, profile, loading } = useAuth();
    const router = useRouter();
    const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);

    useEffect(() => {
        if (!loading && (!user || !profile?.is_superuser)) {
            // Redirection logic for non-admins
            // Small delay to prevent flash
            router.push("/dashboard");
        }
    }, [user, profile, loading, router]);

    if (loading) {
        return (
            <div className="flex h-screen items-center justify-center bg-slate-950 text-slate-400">
                <div className="flex flex-col items-center gap-4">
                    <ShieldCheck className="h-10 w-10 animate-pulse text-indigo-500" />
                    <p className="text-sm font-medium">Verifying authorization...</p>
                </div>
            </div>
        );
    }

    if (!profile?.is_superuser) {
        return null; // Will redirect via useEffect
    }

    const navItems = [
        { label: "Overview", href: "/admin", icon: LayoutDashboard },
        { label: "Organizations", href: "/admin/organizations", icon: Building2 },
        { label: "Users", href: "/admin/users", icon: Users },
        { label: "Health & Logs", href: "/admin/logs", icon: Activity },
    ];

    return (
        <div className="flex h-screen bg-slate-950 font-sans text-slate-200">
            {/* Sidebar */}
            <aside
                className={`relative flex flex-col border-r border-slate-800 bg-slate-900/50 transition-all duration-300 ${isSidebarCollapsed ? "w-20" : "w-64"
                    }`}
            >
                <div className="flex h-16 items-center justify-between px-6 border-b border-slate-800">
                    {!isSidebarCollapsed && (
                        <Link href="/" className="flex items-center gap-2 font-bold text-xl tracking-tight">
                            <span className="text-indigo-500">Epist</span>
                            <span className="text-slate-400 text-sm font-medium px-2 py-0.5 bg-slate-800 rounded">Admin</span>
                        </Link>
                    )}
                    <Button
                        variant="secondary"
                        onClick={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
                        className="text-slate-400 hover:text-white hover:bg-slate-800 h-10 w-10 p-0 items-center justify-center rounded-lg"
                    >
                        {isSidebarCollapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
                    </Button>
                </div>

                <nav className="flex-1 space-y-2 p-4">
                    {navItems.map((item) => (
                        <Link
                            key={item.label}
                            href={item.href}
                            className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-slate-400 transition-colors hover:bg-slate-800 hover:text-white"
                        >
                            <item.icon size={20} className="shrink-0" />
                            {!isSidebarCollapsed && <span>{item.label}</span>}
                        </Link>
                    ))}
                </nav>

                <div className="p-4 border-t border-slate-800">
                    <Link
                        href="/dashboard"
                        className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-indigo-400 transition-colors hover:bg-indigo-500/10 hover:text-indigo-300"
                    >
                        <AppWindow size={20} className="shrink-0" />
                        {!isSidebarCollapsed && <span>Back to App</span>}
                    </Link>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 overflow-y-auto overflow-x-hidden">
                <header className="flex h-16 items-center border-b border-slate-800 bg-slate-900/50 px-8 backdrop-blur-sm">
                    <h1 className="text-lg font-semibold">Admin Panel</h1>
                    <div className="ml-auto flex items-center gap-4">
                        <div className="flex items-center gap-3 px-3 py-1.5 bg-slate-800/50 rounded-full border border-slate-700">
                            <div className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
                            <span className="text-xs font-medium text-slate-300 capitalize">{profile?.email}</span>
                        </div>
                    </div>
                </header>

                <div className="p-8 max-w-7xl mx-auto">
                    {children}
                </div>
            </main>
        </div>
    );
}
