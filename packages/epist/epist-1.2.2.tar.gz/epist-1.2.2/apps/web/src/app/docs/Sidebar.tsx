"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Zap, Search, BookOpen, ChevronLeft, LogIn, Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";
import type { Node as PageTreeNode, Root as PageTreeRoot } from "fumadocs-core/page-tree";
import { useAuth } from "@/components/auth/AuthProvider";

export function Sidebar({ tree }: { tree: PageTreeRoot }) {
    const { user, loading } = useAuth();

    return (
        <aside className="w-64 fixed inset-y-0 left-0 border-r border-border/50 bg-card/50 backdrop-blur-xl flex flex-col z-50">
            {/* Header / Logo */}
            <div className="h-16 flex items-center px-6 border-b border-border/50">
                <Link href="/docs" className="flex items-center gap-2 font-bold text-foreground">
                    <div className="p-1.5 rounded-lg bg-primary/10">
                        <Zap className="w-4 h-4 text-primary" />
                    </div>
                    <span>Epist Docs</span>
                </Link>
            </div>

            {/* Content */}
            <div className="flex-1 overflow-y-auto py-6 px-4 space-y-6">

                {/* Auth / Bridge Navigation */}
                {!loading && (
                    <div className="pb-2">
                        {user ? (
                            <Link
                                href="/dashboard"
                                className="flex items-center gap-2 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors px-1"
                            >
                                <ChevronLeft className="w-4 h-4" />
                                Back to Dashboard
                            </Link>
                        ) : (
                            <div className="grid grid-cols-2 gap-2">
                                <Link
                                    href="/login"
                                    className="flex items-center justify-center gap-2 px-3 py-1.5 rounded-md text-sm font-medium border border-border bg-background hover:bg-accent hover:text-accent-foreground transition-colors"
                                >
                                    <LogIn className="w-3.5 h-3.5" />
                                    Sign In
                                </Link>
                                <Link
                                    href="/"
                                    className="flex items-center justify-center gap-2 px-3 py-1.5 rounded-md text-sm font-medium bg-primary text-primary-foreground hover:bg-primary/90 transition-colors shadow-sm"
                                >
                                    Get Started
                                </Link>
                            </div>
                        )}
                    </div>
                )}

                {/* Search Trigger */}
                <div>
                    <button
                        type="button"
                        className="w-full flex items-center gap-2 px-3 py-2 rounded-lg bg-muted/30 border border-white/10 hover:bg-muted/50 transition-colors group text-sm text-muted-foreground"
                    >
                        <Search className="w-4 h-4 group-hover:text-foreground transition-colors" />
                        <span className="flex-1 text-left">Search</span>
                        <kbd className="hidden sm:inline-flex h-5 items-center gap-1 rounded border border-border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground opacity-100">
                            <span className="text-xs">⌘</span>K
                        </kbd>
                    </button>
                </div>

                {/* Navigation Tree */}
                <div className="space-y-6">
                    <div className="px-2 text-[10px] font-bold text-muted-foreground uppercase tracking-widest flex items-center gap-2">
                        <BookOpen className="w-3 h-3" />
                        Developer Hub
                    </div>

                    <nav className="space-y-1">
                        {tree.children.map((node: PageTreeNode, i: number) => (
                            <TreeNode key={i} node={node} />
                        ))}
                    </nav>
                </div>
            </div>
        </aside>
    );
}

function TreeNode({ node }: { node: PageTreeNode }) {
    const pathname = usePathname();

    if (node.type === "separator") {
        return (
            <div className="px-2 py-4">
                <h3 className="text-xs font-semibold text-foreground">{node.name}</h3>
            </div>
        );
    }

    if (node.type === "folder") {
        return (
            <div className="space-y-1 pt-2">
                <div className="px-2 py-1.5 text-sm font-medium text-foreground/80 flex items-center justify-between group cursor-default">
                    {node.name}
                </div>
                <div className="pl-4 space-y-1 border-l border-border/40 ml-2">
                    {node.children.map((child: PageTreeNode, i: number) => (
                        <TreeNode key={i} node={child} />
                    ))}
                </div>
            </div>
        );
    }

    if (node.type === "page") {
        const isActive = pathname === node.url;
        return (
            <Link
                href={node.url}
                className={cn(
                    "flex items-center gap-2 px-2 py-1.5 rounded-md text-sm transition-colors",
                    isActive
                        ? "bg-primary/10 text-primary font-medium"
                        : "text-muted-foreground hover:text-foreground hover:bg-accent/50"
                )}
            >
                {node.name}
            </Link>
        );
    }

    return null;
}
