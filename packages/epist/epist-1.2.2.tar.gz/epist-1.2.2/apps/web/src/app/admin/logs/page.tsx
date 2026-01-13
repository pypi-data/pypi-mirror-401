"use client";

import React, { useEffect, useState } from "react";
import {
    CheckCircle2,
    Clock,
    Terminal,
    RefreshCw
} from "lucide-react";
import { api, AdminRequestLog as RequestLog } from "@/lib/api";
import { Button } from "@/components/ui/button";

export default function AdminLogs() {
    const [logs, setLogs] = useState<RequestLog[]>([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState<number | null>(null);

    async function fetchLogs() {
        setLoading(true);
        try {
            const data = await api.getAdminLogs(filter || undefined);
            setLogs(data);
        } catch (error) {
            console.error("Failed to fetch logs", error);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        fetchLogs();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [filter]);

    const getStatusColor = (code: number) => {
        if (code >= 200 && code < 300) return "text-emerald-400 bg-emerald-400/10 border-emerald-400/20";
        if (code >= 400 && code < 500) return "text-amber-400 bg-amber-400/10 border-amber-400/20";
        return "text-rose-400 bg-rose-400/10 border-rose-400/20";
    };

    return (
        <div className="space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h2 className="text-2xl font-bold text-white">System Logs</h2>
                    <p className="text-slate-400 text-sm">Real-time API request monitoring and error tracking.</p>
                </div>

                <div className="flex items-center gap-2">
                    <select
                        className="bg-slate-900 border border-slate-800 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/50 text-slate-300"
                        onChange={(e) => setFilter(e.target.value ? parseInt(e.target.value) : null)}
                    >
                        <option value="">All Status Codes</option>
                        <option value="200">200 OK</option>
                        <option value="201">201 Created</option>
                        <option value="400">400 Bad Request</option>
                        <option value="401">401 Unauthorized</option>
                        <option value="403">403 Forbidden</option>
                        <option value="404">404 Not Found</option>
                        <option value="500">500 Server Error</option>
                    </select>
                    <Button
                        variant="outline"
                        onClick={fetchLogs}
                        disabled={loading}
                        className="border-slate-800 bg-slate-900 hover:bg-slate-800 gap-2"
                    >
                        <RefreshCw size={16} className={loading ? "animate-spin" : ""} />
                        Refresh
                    </Button>
                </div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="bg-slate-800/50 text-slate-400 text-xs font-semibold uppercase tracking-wider">
                                <th className="px-6 py-4">Status</th>
                                <th className="px-6 py-4">Method</th>
                                <th className="px-6 py-4">Path</th>
                                <th className="px-6 py-4">Latency</th>
                                <th className="px-6 py-4">User</th>
                                <th className="px-6 py-4">Time</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-800 font-mono text-xs">
                            {logs.map((log) => (
                                <tr key={log.id} className="hover:bg-slate-800/30 transition-colors group">
                                    <td className="px-6 py-4">
                                        <span className={`px-2 py-0.5 rounded border text-[10px] font-bold ${getStatusColor(log.status_code)}`}>
                                            {log.status_code}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 font-bold text-slate-300">
                                        {log.method}
                                    </td>
                                    <td className="px-6 py-4">
                                        <span className="text-slate-400 group-hover:text-white transition-colors">
                                            {log.path}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4">
                                        <div className="flex items-center gap-1.5">
                                            <Clock size={12} className={log.latency_ms > 500 ? "text-amber-500" : "text-slate-500"} />
                                            <span className={log.latency_ms > 500 ? "text-amber-400" : "text-slate-400"}>
                                                {Math.round(log.latency_ms)}ms
                                            </span>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 text-slate-500">
                                        {log.user_id ? log.user_id.split('-')[0] : 'anonymous'}
                                    </td>
                                    <td className="px-6 py-4 text-slate-500 whitespace-nowrap">
                                        {new Date(log.created_at).toLocaleTimeString()}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                {loading && logs.length === 0 && (
                    <div className="py-24 flex flex-col items-center text-slate-500">
                        <Terminal size={40} className="mb-4 animate-pulse opacity-20" />
                        <p>Decoding system stream...</p>
                    </div>
                )}

                {!loading && logs.length === 0 && (
                    <div className="py-24 flex flex-col items-center text-slate-500">
                        <CheckCircle2 size={40} className="mb-4 text-emerald-500/20" />
                        <p>No logs found for the selected filter.</p>
                    </div>
                )}
            </div>
        </div>
    );
}
