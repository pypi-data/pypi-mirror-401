"use client";

import { useAuth } from "@/components/auth/AuthProvider";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Volume2, ShieldCheck, Sparkles, Globe, Zap } from "lucide-react";
import { toast } from "sonner";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
    const { signInWithGoogle, user, loading } = useAuth();
    const router = useRouter();
    const [isHovered, setIsHovered] = useState(false);

    useEffect(() => {
        if (user && !loading) {
            router.push("/dashboard");
        }
    }, [user, loading, router]);

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-[#020617]">
                <div className="flex flex-col items-center gap-6">
                    <div className="relative">
                        <div className="w-16 h-16 bg-indigo-500/20 rounded-2xl animate-spin duration-[3000ms]" />
                        <Volume2 className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-indigo-500 w-8 h-8" />
                    </div>
                    <div className="text-slate-400 font-medium tracking-widest text-xs uppercase animate-pulse">
                        Authenticating
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen flex bg-[#020617] text-slate-100 overflow-hidden relative">
            {/* Ambient Background Elements */}
            <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-indigo-500/10 rounded-full blur-[120px] animate-pulse" />
            <div className="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] bg-purple-500/10 rounded-full blur-[120px] animate-pulse transition-all duration-1000" />

            {/* Left Side - Visual/Marketing (Hidden on mobile) */}
            <div className="hidden lg:flex flex-1 flex-col justify-between p-12 relative z-10 border-r border-slate-800/50 bg-slate-900/20 backdrop-blur-3xl">
                <div className="flex items-center gap-3 group cursor-default">
                    <div className="p-2 bg-indigo-500 rounded-lg group-hover:rotate-12 transition-transform duration-300">
                        <Volume2 className="text-white w-6 h-6" />
                    </div>
                    <span className="text-xl font-bold tracking-tight">Epist.ai</span>
                </div>

                <div className="space-y-8">
                    <div className="space-y-4 max-w-lg">
                        <h1 className="text-6xl font-black leading-tight bg-clip-text text-transparent bg-gradient-to-br from-white via-white to-slate-500">
                            The future of audio is <span className="text-indigo-400">searchable.</span>
                        </h1>
                        <p className="text-xl text-slate-400 leading-relaxed">
                            A production-ready platform for transcribing, indexing, and querying your audio content with AI.
                        </p>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        {[
                            { icon: Zap, label: "High Performance", sub: "Optimized RAG" },
                            { icon: Globe, label: "Multilingual", sub: "Dozens of languages" },
                            { icon: ShieldCheck, label: "Secure by Design", sub: "Privacy Focused" },
                            { icon: Sparkles, label: "AI Native", sub: "Built for LLMs" }
                        ].map((stat, i) => (
                            <div key={i} className="p-4 rounded-2xl bg-white/5 border border-white/10 hover:bg-white/10 transition-colors group">
                                <stat.icon className="w-5 h-5 text-indigo-400 mb-2 group-hover:scale-110 transition-transform" />
                                <div className="font-bold text-sm">{stat.label}</div>
                                <div className="text-[10px] text-slate-500 uppercase tracking-wider">{stat.sub}</div>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="text-xs text-slate-500 flex items-center gap-6">
                    <span>© 2025 Epist</span>
                    <Link href="/docs" className="hover:text-white transition-colors">Documentation</Link>
                    <Link href="/pricing" className="hover:text-white transition-colors">Pricing</Link>
                </div>
            </div>

            {/* Right Side - Login Form */}
            <div className="flex-1 flex flex-col items-center justify-center p-6 relative z-10">
                <div className="w-full max-w-md space-y-12">
                    <div className="text-center space-y-4">
                        <div className="lg:hidden flex items-center justify-center gap-3 mb-8">
                            <div className="p-2 bg-indigo-500 rounded-lg">
                                <Volume2 className="text-white w-6 h-6" />
                            </div>
                            <span className="text-xl font-bold tracking-tight">Epist.ai</span>
                        </div>
                        <h2 className="text-3xl font-bold tracking-tight">Welcome back</h2>
                        <p className="text-slate-400">Sign in to manage your audio knowledge base.</p>
                    </div>

                    <div className="space-y-6">
                        <button
                            onMouseEnter={() => setIsHovered(true)}
                            onMouseLeave={() => setIsHovered(false)}
                            onClick={() => signInWithGoogle().catch(() => toast.error("Failed to sign in"))}
                            className="w-full group relative flex items-center justify-center gap-4 h-16 bg-white hover:bg-slate-100 text-slate-950 rounded-2xl font-bold text-lg transition-all transform hover:scale-[1.02] active:scale-[0.98] shadow-2xl shadow-white/10"
                        >
                            <svg className="w-6 h-6" viewBox="0 0 24 24">
                                <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4" />
                                <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
                                <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05" />
                                <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335" />
                            </svg>
                            Continue with Google
                            <ArrowRight className={`w-5 h-5 transition-all duration-300 ${isHovered ? 'translate-x-1 opacity-100' : 'opacity-0 -translate-x-2'}`} />
                        </button>

                        <div className="flex items-center gap-4 text-xs text-slate-500 uppercase tracking-widest font-bold">
                            <div className="h-px bg-slate-800 flex-1" />
                            <span>Trust Layer Security</span>
                            <div className="h-px bg-slate-800 flex-1" />
                        </div>
                    </div>

                    <p className="text-center text-xs text-slate-500 px-6">
                        By signing in, you agree to our
                        <Link href="/legal/terms-of-service" className="text-slate-300 hover:text-white mx-1 transition-colors underline decoration-slate-700">Terms of Service</Link>
                        and
                        <Link href="/legal/privacy-policy" className="text-slate-300 hover:text-white mx-1 transition-colors underline decoration-slate-700">Privacy Policy</Link>.
                    </p>
                </div>
            </div>
        </div>
    );
}

function ArrowRight({ className }: { className?: string }) {
    return (
        <svg fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor" className={className}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
        </svg>
    )
}
