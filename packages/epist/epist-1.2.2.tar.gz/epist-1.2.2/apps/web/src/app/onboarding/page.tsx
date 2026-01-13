"use client";

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/components/auth/AuthProvider';
import { api } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Volume2, Sparkles, Rocket, Shield, ArrowRight, Loader2 } from 'lucide-react';
import { toast } from 'sonner';

export default function OnboardingPage() {
    const { user, loading: authLoading } = useAuth();
    const router = useRouter();
    const [step, setStep] = useState(1);
    const [orgName, setOrgName] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);

    useEffect(() => {
        if (!authLoading && !user) {
            router.push('/login');
        }
    }, [user, authLoading, router]);

    const handleComplete = async () => {
        if (!orgName.trim()) {
            toast.error('Please enter a workspace name');
            return;
        }

        setIsSubmitting(true);
        try {
            // Update organization name and mark onboarding as complete
            // We'll create a dedicated onboarding endpoint for simplicity
            await api.completeOnboarding(orgName);
            toast.success('Welcome to Epist!');
            router.push('/dashboard');
        } catch (error) {
            console.error('Onboarding failed:', error);
            toast.error('Failed to save your settings. Please try again.');
        } finally {
            setIsSubmitting(false);
        }
    };

    if (authLoading) {
        return (
            <div className="min-h-screen bg-slate-950 flex items-center justify-center">
                <Loader2 className="w-8 h-8 text-indigo-500 animate-spin" />
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col items-center justify-center p-6 relative overflow-hidden">
            {/* Background Glows */}
            <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-indigo-500/10 rounded-full blur-[120px] pointer-events-none" />
            <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-purple-500/10 rounded-full blur-[120px] pointer-events-none" />

            <div className="max-w-xl w-full z-10">
                {/* Progress Bar */}
                <div className="flex gap-2 mb-12">
                    {[1, 2, 3].map((s) => (
                        <div
                            key={s}
                            className={`h-1 flex-1 rounded-full transition-all duration-500 ${s <= step ? 'bg-indigo-500 shadow-[0_0_10px_rgba(99,102,241,0.5)]' : 'bg-slate-800'
                                }`}
                        />
                    ))}
                </div>

                {step === 1 && (
                    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
                        <div className="space-y-4">
                            <div className="inline-flex p-3 bg-indigo-500/10 rounded-2xl border border-indigo-500/20 text-indigo-400 mb-2">
                                <Sparkles className="w-6 h-6" />
                            </div>
                            <h1 className="text-4xl font-bold tracking-tight">Welcome to Epist.ai</h1>
                            <p className="text-slate-400 text-lg leading-relaxed">
                                Let&apos;s set up your workspace to get you started with production-ready audio intelligence.
                            </p>
                        </div>

                        <div className="space-y-4">
                            <label className="text-sm font-medium text-slate-300">Workspace name</label>
                            <input
                                autoFocus
                                type="text"
                                value={orgName}
                                onChange={(e) => setOrgName(e.target.value)}
                                placeholder="e.g. Acme Research"
                                className="w-full h-14 bg-slate-900/50 border border-slate-800 rounded-xl px-4 text-lg focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all placeholder:text-slate-600"
                                onKeyDown={(e) => e.key === 'Enter' && setStep(2)}
                            />
                        </div>

                        <Button
                            onClick={() => setStep(2)}
                            disabled={!orgName.trim()}
                            className="w-full h-14 justify-between"
                        >
                            Continue to features
                            <ArrowRight className="w-5 h-5" />
                        </Button>
                    </div>
                )}

                {step === 2 && (
                    <div className="space-y-8 animate-in fade-in slide-in-from-right-4 duration-500">
                        <div className="space-y-4">
                            <div className="inline-flex p-3 bg-purple-500/10 rounded-2xl border border-purple-500/20 text-purple-400 mb-2">
                                <Rocket className="w-6 h-6" />
                            </div>
                            <h1 className="text-4xl font-bold tracking-tight">Powering your RAG</h1>
                            <p className="text-slate-400 text-lg leading-relaxed">
                                Epist transforms audio into searchable knowledge bases. Upload once, query forever.
                            </p>
                        </div>

                        <div className="grid gap-4">
                            {[
                                { icon: Volume2, title: 'Smart Transcription', desc: 'Speaker diarization and timestamps included.' },
                                { icon: Sparkles, title: 'LLM Ready', desc: 'Chunked and embedded for immediate AI retrieval.' },
                                { icon: Shield, title: 'Enterprise Secure', desc: 'Production-grade security and API management.' }
                            ].map((item, idx) => (
                                <div key={idx} className="flex gap-4 p-4 bg-slate-900/40 border border-slate-800/50 rounded-2xl">
                                    <div className="p-2 bg-slate-800 rounded-lg h-fit">
                                        <item.icon className="w-5 h-5 text-indigo-400" />
                                    </div>
                                    <div className="space-y-1">
                                        <h3 className="font-semibold text-slate-200">{item.title}</h3>
                                        <p className="text-sm text-slate-500">{item.desc}</p>
                                    </div>
                                </div>
                            ))}
                        </div>

                        <div className="flex gap-4">
                            <Button variant="secondary" onClick={() => setStep(1)} className="flex-1 h-14">
                                Back
                            </Button>
                            <Button onClick={() => setStep(3)} className="flex-[2] h-14 justify-center">
                                Almost there
                            </Button>
                        </div>
                    </div>
                )}

                {step === 3 && (
                    <div className="space-y-8 animate-in fade-in slide-in-from-right-4 duration-500">
                        <div className="space-y-4">
                            <div className="inline-flex p-3 bg-green-500/10 rounded-2xl border border-green-500/20 text-green-400 mb-2">
                                <Shield className="w-6 h-6" />
                            </div>
                            <h1 className="text-4xl font-bold tracking-tight">You&apos;re all set!</h1>
                            <p className="text-slate-400 text-lg leading-relaxed">
                                Your workspace <span className="text-indigo-400 font-semibold">{orgName}</span> is ready for your first audio file.
                            </p>
                        </div>

                        <div className="p-6 bg-indigo-500/10 border border-indigo-500/20 rounded-3xl space-y-4">
                            <h3 className="text-sm font-bold uppercase tracking-widest text-indigo-400">Quick Start Tip</h3>
                            <p className="text-slate-300 leading-relaxed">
                                Visit the **Playground** to test our RAG capabilities with your own files or a YouTube link.
                            </p>
                        </div>

                        <div className="flex gap-4">
                            <Button variant="secondary" onClick={() => setStep(2)} className="flex-1 h-14">
                                Back
                            </Button>
                            <Button
                                onClick={handleComplete}
                                disabled={isSubmitting}
                                className="flex-[2] h-14 justify-center bg-indigo-500 hover:bg-indigo-400"
                            >
                                {isSubmitting ? (
                                    <>
                                        <Loader2 className="w-5 h-5 animate-spin" />
                                        Setting up...
                                    </>
                                ) : (
                                    'Launch Dashboard'
                                )}
                            </Button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
