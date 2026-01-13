"use client";

import React, { useEffect, useState } from "react";
import {
    Users,
    Building2,
    Mic2,
    Activity,
    ArrowUpRight,
    Clock,
    TrendingUp
} from "lucide-react";
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    AreaChart,
    Area
} from 'recharts';
import { api, AdminStats as Stats, AdminUsageMetric as UsageMetric } from "@/lib/api";

export default function AdminDashboard() {
    const [stats, setStats] = useState<Stats | null>(null);
    const [usage, setUsage] = useState<UsageMetric[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchData() {
            try {
                const [statsData, usageData] = await Promise.all([
                    api.getAdminStats(),
                    api.getAdminUsage(14)
                ]);
                setStats(statsData);
                setUsage(usageData);
            } catch (error) {
                console.error("Failed to fetch admin data", error);
            } finally {
                setLoading(false);
            }
        }
        fetchData();
    }, []);

    if (loading) {
        return (
            <div className="space-y-8 animate-pulse">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {[1, 2, 3, 4].map(i => (
                        <div key={i} className="h-32 bg-slate-900 rounded-xl border border-slate-800" />
                    ))}
                </div>
                <div className="h-96 bg-slate-900 rounded-xl border border-slate-800" />
            </div>
        );
    }

    const statCards = [
        { label: "Total Users", value: stats?.users || 0, icon: Users, color: "text-blue-400", bg: "bg-blue-400/10" },
        { label: "Active (24h)", value: stats?.active_users_24h || 0, icon: Activity, color: "text-emerald-400", bg: "bg-emerald-400/10" },
        { label: "Organizations", value: stats?.organizations || 0, icon: Building2, color: "text-purple-400", bg: "bg-purple-400/10" },
        { label: "Audio Resources", value: stats?.audio_resources || 0, icon: Mic2, color: "text-orange-400", bg: "bg-orange-400/10" },
    ];

    return (
        <div className="space-y-8">
            {/* Header Section */}
            <div>
                <h2 className="text-3xl font-bold tracking-tight text-white transition-all hover:text-indigo-400">System Overview</h2>
                <p className="text-slate-400 mt-1">Real-time health and usage metrics for the Epist platform.</p>
            </div>

            {/* Stat Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {statCards.map((card) => (
                    <div
                        key={card.label}
                        className="group relative overflow-hidden bg-slate-900 rounded-2xl border border-slate-800 p-6 transition-all hover:border-indigo-500/50 hover:shadow-2xl hover:shadow-indigo-500/10"
                    >
                        <div className="flex justify-between items-start">
                            <div className={`p-3 rounded-xl ${card.bg} ${card.color}`}>
                                <card.icon size={24} />
                            </div>
                            <TrendingUp className="text-slate-600 group-hover:text-indigo-400 transition-colors" size={20} />
                        </div>
                        <div className="mt-4">
                            <p className="text-slate-500 text-sm font-medium">{card.label}</p>
                            <h3 className="text-3xl font-bold text-slate-100 mt-1">
                                {card.value.toLocaleString()}
                            </h3>
                        </div>
                        {/* Subtle interactive background glow */}
                        <div className="absolute -right-4 -bottom-4 h-24 w-24 bg-indigo-500/5 blur-[60px] group-hover:bg-indigo-500/10 transition-all rounded-full" />
                    </div>
                ))}
            </div>

            {/* Main Charts Row */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Request Volume Chart */}
                <div className="bg-slate-900 p-8 rounded-2xl border border-slate-800 shadow-sm transition-all hover:border-slate-700">
                    <div className="flex items-center justify-between mb-8">
                        <div>
                            <h3 className="text-xl font-bold flex items-center gap-2">
                                <Activity className="text-indigo-400" size={20} />
                                Request Volume
                            </h3>
                            <p className="text-slate-500 text-sm">Last 14 days activity</p>
                        </div>
                        <div className="px-3 py-1 bg-emerald-500/10 text-emerald-400 rounded-full text-xs font-semibold flex items-center gap-1">
                            <ArrowUpRight size={14} /> +12%
                        </div>
                    </div>

                    <div className="h-[300px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={usage}>
                                <defs>
                                    <linearGradient id="colorRequests" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                                        <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#1e293b" />
                                <XAxis
                                    dataKey="date"
                                    tickFormatter={(str: string) => new Date(str).toLocaleDateString([], { month: 'short', day: 'numeric' })}
                                    stroke="#64748b"
                                    fontSize={12}
                                    tickLine={false}
                                    axisLine={false}
                                />
                                <YAxis
                                    stroke="#64748b"
                                    fontSize={12}
                                    tickLine={false}
                                    axisLine={false}
                                />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }}
                                    itemStyle={{ color: '#818cf8' }}
                                />
                                <Area
                                    type="monotone"
                                    dataKey="requests"
                                    stroke="#818cf8"
                                    strokeWidth={3}
                                    fillOpacity={1}
                                    fill="url(#colorRequests)"
                                />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Latency Chart */}
                <div className="bg-slate-900 p-8 rounded-2xl border border-slate-800 shadow-sm transition-all hover:border-slate-700">
                    <div className="flex items-center justify-between mb-8">
                        <div>
                            <h3 className="text-xl font-bold flex items-center gap-2">
                                <Clock className="text-orange-400" size={20} />
                                Average Latency
                            </h3>
                            <p className="text-slate-500 text-sm">API performance monitoring</p>
                        </div>
                        <div className="px-3 py-1 bg-slate-800 text-slate-400 rounded-full text-xs font-semibold">
                            ms
                        </div>
                    </div>

                    <div className="h-[300px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={usage}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#1e293b" />
                                <XAxis
                                    dataKey="date"
                                    tickFormatter={(str: string) => new Date(str).toLocaleDateString([], { month: 'short', day: 'numeric' })}
                                    stroke="#64748b"
                                    fontSize={12}
                                    tickLine={false}
                                    axisLine={false}
                                />
                                <YAxis
                                    stroke="#64748b"
                                    fontSize={12}
                                    tickLine={false}
                                    axisLine={false}
                                />
                                <Tooltip
                                    cursor={{ fill: '#1e293b' }}
                                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }}
                                />
                                <Bar
                                    dataKey="avg_latency_ms"
                                    fill="#facc15"
                                    radius={[4, 4, 0, 0]}
                                    barSize={30}
                                />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>
        </div>
    );
}
