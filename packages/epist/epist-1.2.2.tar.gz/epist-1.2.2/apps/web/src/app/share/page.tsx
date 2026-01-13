"use client";

import React, { useEffect, useState, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { api, AudioStatus, Transcript } from '@/lib/api';
import { TranscriptViewer } from '@/components/playground/TranscriptViewer';
import { WaveformBackground } from '@/components/WaveformBackground';
import { Loader2, ExternalLink, ShieldCheck, Zap } from 'lucide-react';
import { Header } from '@/components/Header';
import { Footer } from '@/components/Footer';

function ShareContent() {
    const searchParams = useSearchParams();
    const audio_id = searchParams.get('id');
    const [audio, setAudio] = useState<AudioStatus | null>(null);
    const [transcript, setTranscript] = useState<Transcript | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            if (!audio_id) {
                setError('No transcript ID provided.');
                setLoading(false);
                return;
            }

            try {
                // Fetch public audio status
                const audioData = await api.getAudioStatus(audio_id);
                setAudio(audioData);

                // Fetch public transcript
                const transcriptData = await api.getTranscript(audio_id);
                setTranscript(transcriptData);
            } catch (err: unknown) {
                console.error('Error fetching public resource:', err);
                const axiosError = err as { response?: { status?: number } };
                setError(axiosError.response?.status === 403
                    ? 'This transcript is private. Ask the owner to share it with you.'
                    : 'Transcript not found or has been deleted.');
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [audio_id]);

    if (loading) {
        return (
            <div className="min-h-screen bg-slate-950 flex items-center justify-center">
                <div className="flex flex-col items-center gap-4">
                    <Loader2 className="w-8 h-8 text-indigo-500 animate-spin" />
                    <p className="text-slate-400 font-medium">Fetching transcript...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
                <div className="max-w-md w-full bg-slate-900 border border-slate-800 rounded-2xl p-8 text-center space-y-6">
                    <div className="w-16 h-16 bg-red-500/10 rounded-full flex items-center justify-center mx-auto text-red-500">
                        <ShieldCheck className="w-8 h-8" />
                    </div>
                    <div className="space-y-2">
                        <h1 className="text-xl font-bold text-slate-100">Access Restricted</h1>
                        <p className="text-slate-400 text-sm leading-relaxed">{error}</p>
                    </div>
                    <Link
                        href="/"
                        className="inline-block px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-colors font-medium text-sm"
                    >
                        Go to Home
                    </Link>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-slate-950 flex flex-col relative overflow-hidden">
            <WaveformBackground />

            <Header />

            <main className="flex-1 container mx-auto px-4 py-12 relative z-10 max-w-4xl">
                <div className="mb-8 space-y-4">
                    <div className="flex flex-wrap items-center gap-3">
                        <span className="px-2.5 py-1 rounded-full bg-indigo-500/10 text-indigo-400 text-[10px] font-bold uppercase tracking-wider border border-indigo-500/20">
                            Public Transcript
                        </span>
                        <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400 truncate max-w-full">
                            {audio?.title}
                        </h1>
                    </div>
                    <p className="text-slate-400 text-sm leading-relaxed">
                        Transcribed on {new Date(audio?.created_at || '').toLocaleDateString('en-US', {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric'
                        })}
                    </p>
                </div>

                <div className="grid grid-cols-1 gap-6">
                    <div className="h-[600px] border border-slate-800 rounded-2xl overflow-hidden shadow-2xl shadow-indigo-500/5">
                        {transcript && <TranscriptViewer transcript={transcript} onSeek={() => { }} />}
                    </div>

                    {/* Viral Loop Banner */}
                    <div className="bg-gradient-to-r from-indigo-900/20 to-purple-900/20 border border-indigo-500/20 rounded-2xl p-6 flex flex-col md:flex-row items-center justify-between gap-6 backdrop-blur-md">
                        <div className="space-y-2 text-center md:text-left">
                            <h3 className="text-lg font-bold text-white flex items-center justify-center md:justify-start gap-2">
                                <Zap className="w-5 h-5 text-yellow-400 fill-yellow-400" />
                                Build your own Audio Knowledge Base
                            </h3>
                            <p className="text-slate-400 text-sm max-w-md">
                                Transform any audio into a searchable RAG knowledge base. Join 1,000+ developers building with Epist.ai.
                            </p>
                        </div>
                        <Link
                            href="/login"
                            className="w-full md:w-auto px-8 py-3 bg-white text-slate-950 font-bold rounded-xl hover:bg-slate-200 transition-all transform hover:scale-105 shadow-xl shadow-white/10 flex items-center justify-center gap-2"
                        >
                            Get Started for Free
                            <ExternalLink className="w-4 h-4" />
                        </Link>
                    </div>
                </div>
            </main>

            <Footer />

            {/* Attribution - Sticky Bottom */}
            <div className="fixed bottom-0 left-0 right-0 py-2 text-center bg-slate-950/80 backdrop-blur-sm border-t border-slate-800 pointer-events-none">
                <p className="text-[10px] text-slate-500 pointer-events-auto">
                    Powered by <Link href="/" className="hover:text-indigo-400 transition-colors font-semibold">Epist.ai</Link> - Production-ready Audio Intelligence for Developers
                </p>
            </div>
        </div>
    );
}

export default function SharePage() {
    return (
        <Suspense fallback={
            <div className="min-h-screen bg-slate-950 flex items-center justify-center">
                <Loader2 className="w-8 h-8 text-indigo-500 animate-spin" />
            </div>
        }>
            <ShareContent />
        </Suspense>
    );
}
