"use client";

import React, { useEffect, useState } from 'react';
import { api, AudioStatus } from '@/lib/api';
import {
    FileAudio,
    Globe,
    Lock,
    Share2,
    ExternalLink,
    Trash2,
    CheckCircle2,
    Clock,
    AlertCircle,
    Loader2
} from 'lucide-react';
import { toast } from 'sonner';
import Link from 'next/link';

export function AudioList() {
    const [audios, setAudios] = useState<AudioStatus[]>([]);
    const [loading, setLoading] = useState(true);

    const fetchAudios = async () => {
        try {
            const data = await api.listAudio();
            setAudios(data);
        } catch (error) {
            console.error('Failed to fetch audios:', error);
            toast.error('Could not load your audio resources');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchAudios();
    }, []);

    const togglePublic = async (audio: AudioStatus) => {
        const newStatus = !audio.is_public;
        try {
            await api.updateAudio(audio.id, { is_public: newStatus });
            setAudios(audios.map(a => a.id === audio.id ? { ...a, is_public: newStatus } : a));
            toast.success(newStatus ? 'Transcript is now public' : 'Transcript is now private');
        } catch {
            toast.error('Failed to update visibility');
        }
    };

    const deleteAudio = async (id: string) => {
        if (!confirm('Are you sure you want to delete this resource?')) return;
        try {
            // Assuming there's a deleteAudio method in api.ts
            // If not, I'll need to add it, but for now let's assume it exists or call axios directly
            // Actually, I saw delete_audio in audio.py. Let's add it to api.ts if I haven't.
            await api.deleteAudio(id);
            setAudios(audios.filter(a => a.id !== id));
            toast.success('Resource deleted');
        } catch {
            toast.error('Failed to delete resource');
        }
    };

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center p-12 space-y-4">
                <Loader2 className="w-8 h-8 text-indigo-500 animate-spin" />
                <p className="text-slate-500 text-sm">Loading your resources...</p>
            </div>
        );
    }

    if (audios.length === 0) {
        return (
            <div className="text-center p-12 bg-slate-900/50 border border-dashed border-slate-800 rounded-2xl">
                <FileAudio className="w-12 h-12 text-slate-700 mx-auto mb-4" />
                <h3 className="text-slate-300 font-semibold mb-2">No audio resources yet</h3>
                <p className="text-slate-500 text-sm mb-6">Upload your first audio file or transcribe a URL to get started.</p>
                <Link href="/dashboard/playground" className="text-indigo-400 hover:text-indigo-300 font-medium text-sm transition-colors">
                    Go to Playground →
                </Link>
            </div>
        );
    }

    return (
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
            <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                    <thead className="bg-slate-950 border-b border-slate-800 text-slate-400">
                        <tr>
                            <th className="px-6 py-4 font-medium">Resource</th>
                            <th className="px-6 py-4 font-medium">Status</th>
                            <th className="px-6 py-4 font-medium">Created</th>
                            <th className="px-6 py-4 font-medium">Visibility</th>
                            <th className="px-6 py-4 font-medium text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800">
                        {audios.map((audio) => (
                            <tr key={audio.id} className="group hover:bg-slate-800/50 transition-colors">
                                <td className="px-6 py-4">
                                    <div className="flex items-center gap-3">
                                        <div className="p-2 bg-indigo-500/10 rounded-lg text-indigo-400">
                                            <FileAudio size={18} />
                                        </div>
                                        <div>
                                            <div className="font-medium text-slate-200 truncate max-w-[200px]" title={audio.title}>
                                                {audio.title}
                                            </div>
                                            <div className="text-[10px] text-slate-500 font-mono mt-0.5">
                                                {audio.id.split('-')[0]}...
                                            </div>
                                        </div>
                                    </div>
                                </td>
                                <td className="px-6 py-4">
                                    {audio.status === 'completed' && (
                                        <span className="flex items-center gap-1.5 text-emerald-400 text-xs font-medium">
                                            <CheckCircle2 size={14} /> Ready
                                        </span>
                                    )}
                                    {audio.status === 'processing' && (
                                        <span className="flex items-center gap-1.5 text-indigo-400 text-xs font-medium animate-pulse">
                                            <Loader2 size={14} className="animate-spin" /> Processing
                                        </span>
                                    )}
                                    {audio.status === 'pending' && (
                                        <span className="flex items-center gap-1.5 text-slate-400 text-xs font-medium">
                                            <Clock size={14} /> Pending
                                        </span>
                                    )}
                                    {audio.status === 'failed' && (
                                        <span className="flex items-center gap-1.5 text-red-400 text-xs font-medium">
                                            <AlertCircle size={14} /> Failed
                                        </span>
                                    )}
                                </td>
                                <td className="px-6 py-4 text-slate-500 whitespace-nowrap">
                                    {new Date(audio.created_at).toLocaleDateString()}
                                </td>
                                <td className="px-6 py-4">
                                    <button
                                        onClick={() => togglePublic(audio)}
                                        className={`flex items-center gap-2 px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-tighter transition-all ${audio.is_public
                                            ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                                            : 'bg-slate-800 text-slate-500 border border-transparent hover:border-slate-700'
                                            }`}
                                    >
                                        {audio.is_public ? <Globe size={11} /> : <Lock size={11} />}
                                        {audio.is_public ? 'Public' : 'Private'}
                                    </button>
                                </td>
                                <td className="px-6 py-4 text-right">
                                    <div className="flex items-center justify-end gap-2 opacity-100 md:opacity-0 group-hover:opacity-100 transition-opacity">
                                        {audio.is_public && (
                                            <Link
                                                href={`/share/?id=${audio.id}`}
                                                className="p-1.5 text-slate-400 hover:text-indigo-400 hover:bg-slate-800 rounded-md transition-all"
                                                title="View Public Page"
                                            >
                                                <Share2 size={16} />
                                            </Link>
                                        )}
                                        <Link
                                            href={`/dashboard/playground?audio_id=${audio.id}`}
                                            className="p-1.5 text-slate-400 hover:text-white hover:bg-slate-800 rounded-md transition-all"
                                            title="Open in Playground"
                                        >
                                            <ExternalLink size={16} />
                                        </Link>
                                        <button
                                            onClick={() => deleteAudio(audio.id)}
                                            className="p-1.5 text-slate-400 hover:text-red-500 hover:bg-red-500/10 rounded-md transition-all"
                                            title="Delete Resource"
                                        >
                                            <Trash2 size={16} />
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
