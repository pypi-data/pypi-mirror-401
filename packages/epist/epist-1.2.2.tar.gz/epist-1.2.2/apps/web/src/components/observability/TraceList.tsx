'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { api, TraceEvent } from '@/lib/api';
import { formatDistanceToNow } from 'date-fns';

export default function TraceList() {
    const [traces, setTraces] = useState<TraceEvent[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchTraces = async () => {
            try {
                // Fetch root traces only
                const data = await api.getTraces(50, 0, true);
                setTraces(data);
            } catch (error) {
                console.error('Failed to fetch traces:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchTraces();
    }, []);

    if (loading) {
        return (
            <div className="animate-pulse space-y-4">
                {[...Array(5)].map((_, i) => (
                    <div key={i} className="h-16 bg-white/5 rounded-lg border border-white/10" />
                ))}
            </div>
        );
    }

    if (traces.length === 0) {
        return (
            <div className="text-center py-12 text-white/40 bg-white/5 rounded-lg border border-white/10">
                <p>No traces found. Run some RAG workflows to generate data.</p>
            </div>
        );
    }

    return (
        <div className="w-full overflow-hidden rounded-xl border border-white/10 bg-white/5 backdrop-blur-sm">
            <table className="w-full text-sm text-left">
                <thead className="text-xs uppercase bg-white/5 text-white/60">
                    <tr>
                        <th className="px-6 py-4 font-medium">Status</th>
                        <th className="px-6 py-4 font-medium">Trace ID</th>
                        <th className="px-6 py-4 font-medium">Component</th>
                        <th className="px-6 py-4 font-medium">Name</th>
                        <th className="px-6 py-4 font-medium">Latency</th>
                        <th className="px-6 py-4 font-medium">Time</th>
                        <th className="px-6 py-4 font-medium text-right">Action</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                    {traces.map((trace) => (
                        <tr key={trace.id} className="hover:bg-white/5 transition-colors group">
                            <td className="px-6 py-4">
                                <StatusBadge status={trace.status} />
                            </td>
                            <td className="px-6 py-4 font-mono text-white/70 truncate max-w-[120px]" title={trace.trace_id}>
                                {trace.trace_id.slice(0, 8)}...
                            </td>
                            <td className="px-6 py-4 text-white/80">{trace.component}</td>
                            <td className="px-6 py-4 text-white font-medium">{trace.name}</td>
                            <td className="px-6 py-4 text-white/70">
                                {trace.latency_ms > 0 ? `${trace.latency_ms.toFixed(0)}ms` : '<1ms'}
                            </td>
                            <td className="px-6 py-4 text-white/60">
                                {formatDistanceToNow(new Date(trace.start_time), { addSuffix: true })}
                            </td>
                            <td className="px-6 py-4 text-right">
                                <Link
                                    href={`/dashboard/traces/detail?id=${trace.trace_id}`}
                                    className="text-primary hover:text-primary-light font-medium transition-colors"
                                >
                                    View Details &rarr;
                                </Link>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

function StatusBadge({ status }: { status: string }) {
    const isError = status === 'error';
    return (
        <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ring-1 ring-inset ${isError
            ? 'bg-red-400/10 text-red-400 ring-red-400/20'
            : 'bg-green-400/10 text-green-400 ring-green-400/20'
            }`}>
            {isError ? 'Error' : 'Success'}
        </span>
    );
}
