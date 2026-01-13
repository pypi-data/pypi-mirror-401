"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Volume2, Menu, X } from "lucide-react";
import { useState, useEffect } from "react";
import { AuthProvider } from "@/components/auth/AuthProvider";
import { StagingGate } from "@/components/auth/StagingGate";

export function ClientLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <AuthProvider>
            <StagingGate>
                <ClientLayoutContent>{children}</ClientLayoutContent>
            </StagingGate>
        </AuthProvider>
    );
}

function ClientLayoutContent({
    children,
}: {
    children: React.ReactNode;
}) {
    const pathname = usePathname();
    const [scrolled, setScrolled] = useState(false);
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

    useEffect(() => {
        const handleScroll = () => setScrolled(window.scrollY > 20);
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    useEffect(() => {
        if (mobileMenuOpen) {
            // eslint-disable-next-line react-hooks/set-state-in-effect
            setMobileMenuOpen(false);
        }
    }, [pathname, mobileMenuOpen]);

    const isDashboard = pathname?.startsWith('/dashboard');
    const isBlog = pathname?.startsWith('/blog');
    const isHome = pathname === '/';
    const isDocs = pathname?.startsWith('/docs');
    const isLegal = pathname?.startsWith('/legal');
    const isAuth = pathname === '/login' || pathname === '/onboarding';

    // Show landing navigation/footer only on marketing pages (not dashboard, not auth, not docs, not legal)
    // Specifically: NOT on dashboard, NOT on landing itself, NOT on blog, NOT on auth, NOT on docs, NOT on legal
    const showLandingNav = pathname && !isDashboard && !isHome && !isBlog && !isAuth && !isDocs && !isLegal;

    return (
        <div className="flex flex-col min-h-screen">
            {/* Global Navigation - Hide on Dashboard, Landing, and Blog */}
            {showLandingNav && (
                <nav className={`fixed top-0 w-full z-50 transition-all duration-300 ${scrolled || !isHome ? 'bg-slate-950/80 backdrop-blur-lg border-b border-slate-800' : 'bg-transparent'}`}>
                    <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
                        <Link href="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
                            <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center shadow-lg shadow-indigo-500/20">
                                <Volume2 size={18} className="text-white" />
                            </div>
                            <span className="font-bold text-lg tracking-tight">Epist.ai</span>
                        </Link>

                        <div className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-400">
                            <Link href="/#features" className={`${pathname === '/#features' ? 'text-white' : 'hover:text-white'} transition-colors`}>Features</Link>
                            <Link href="/docs" className={`${pathname === '/docs' ? 'text-white' : 'hover:text-white'} transition-colors`}>Documentation</Link>
                            <Link href="/blog" className={`${pathname.startsWith('/blog') ? 'text-white' : 'hover:text-white'} transition-colors`}>Blog</Link>
                            <div className="h-4 w-px bg-slate-800" />
                            <Link
                                href="/dashboard"
                                className={`px-4 py-2 rounded-full transition-all ${pathname.startsWith('/dashboard') ? 'bg-indigo-600 text-white' : 'bg-slate-900 border border-slate-800 hover:bg-slate-800 text-slate-200'}`}
                            >
                                {pathname.startsWith('/dashboard') ? 'Dashboard' : 'Sign In'}
                            </Link>
                        </div>

                        <button className="md:hidden text-slate-400" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
                            {mobileMenuOpen ? <X /> : <Menu />}
                        </button>
                    </div>
                </nav>
            )}

            {/* Mobile Menu */}
            {mobileMenuOpen && showLandingNav && (
                <div className="fixed inset-0 z-40 bg-slate-950 pt-24 px-6 md:hidden space-y-6">
                    <Link href="/#features" className="block w-full text-left text-xl font-bold text-slate-300 py-2 border-b border-slate-800">Features</Link>
                    <Link href="/docs" className="block w-full text-left text-xl font-bold text-slate-300 py-2 border-b border-slate-800">Documentation</Link>
                    <Link href="/blog" className="block w-full text-left text-xl font-bold text-slate-300 py-2 border-b border-slate-800">Blog</Link>
                    <Link href="/dashboard" className="block w-full text-left text-xl font-bold text-indigo-400 py-2">Dashboard / Sign In</Link>
                </div>
            )}

            <main className="flex-1 flex flex-col">
                {children}
            </main>

            {/* Global Footer - Hide on Dashboard, Landing, and Blog */}
            {showLandingNav && (
                <footer className="border-t border-slate-900 bg-slate-950 pt-16 pb-8">
                    <div className="max-w-7xl mx-auto px-6">
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-12">
                            <div className="col-span-2 md:col-span-1">
                                <div className="flex items-center gap-2 mb-4">
                                    <div className="w-6 h-6 bg-indigo-600 rounded flex items-center justify-center">
                                        <Volume2 size={14} className="text-white" />
                                    </div>
                                    <span className="font-bold">Epist.ai</span>
                                </div>
                                <p className="text-slate-500 text-sm">
                                    The developer-first audio intelligence platform.
                                </p>
                            </div>

                            <div>
                                <h4 className="font-semibold text-slate-200 mb-4">Resources</h4>
                                <ul className="space-y-2 text-sm text-slate-400">
                                    <li><Link href="/docs" className="hover:text-indigo-400 transition-colors">Documentation</Link></li>
                                    <li><Link href="/blog" className="hover:text-indigo-400 transition-colors">Blog</Link></li>
                                    <li><a href="#" className="hover:text-indigo-400 transition-colors">GitHub</a></li>
                                    <li><a href="#" className="hover:text-indigo-400 transition-colors">Status</a></li>
                                </ul>
                            </div>

                            <div>
                                <h4 className="font-semibold text-slate-200 mb-4">Legal</h4>
                                <ul className="space-y-2 text-sm text-slate-400">
                                    <li><Link href="/legal/privacy-policy" className="hover:text-indigo-400 transition-colors">Privacy</Link></li>
                                    <li><Link href="/legal/terms-of-service" className="hover:text-indigo-400 transition-colors">Terms</Link></li>
                                </ul>
                            </div>
                        </div>

                        <div className="pt-8 border-t border-slate-900 flex flex-col md:flex-row justify-between items-center gap-4 text-xs text-slate-600">
                            <p>© 2024 Epist.ai. All rights reserved.</p>
                            <div className="flex items-center gap-4">
                                <span>System Operational</span>
                                <div className="w-2 h-2 rounded-full bg-emerald-500"></div>
                            </div>
                        </div>
                    </div>
                </footer>
            )}
        </div>
    );
}
