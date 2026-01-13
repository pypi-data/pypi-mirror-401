"use client";

import React, { useEffect, useState } from "react";
import {
    Search,
    Building2,
    Users,
    ExternalLink,
    Filter
} from "lucide-react";
import { api, AdminOrganization as Organization } from "@/lib/api";
import { Button } from "@/components/ui/button";

export default function AdminOrganizations() {
    const [orgs, setOrgs] = useState<Organization[]>([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState("");

    useEffect(() => {
        async function fetchOrgs() {
            try {
                const data = await api.getAdminOrganizations();
                setOrgs(data);
            } catch (error) {
                console.error("Failed to fetch organizations", error);
            } finally {
                setLoading(false);
            }
        }
        fetchOrgs();
    }, []);

    const filteredOrgs = orgs.filter(org =>
        org.name.toLowerCase().includes(search.toLowerCase())
    );

    const handleUpdateTier = async (orgId: string, currentTier: string) => {
        const tiers = ['free', 'pro', 'enterprise'];
        const nextTier = tiers[(tiers.indexOf(currentTier) + 1) % tiers.length];
        if (!confirm(`Upgrade/Change ${nextTier.toUpperCase()}?`)) return;

        try {
            await api.updateAdminOrganization(orgId, { tier: nextTier });
            setOrgs(orgs.map(o => o.id === orgId ? { ...o, tier: nextTier } : o));
        } catch (error) {
            console.error("Failed to update organization", error);
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h2 className="text-2xl font-bold text-white">Organizations</h2>
                    <p className="text-slate-400 text-sm">Manage all teams and subscription tiers.</p>
                </div>

                <div className="flex items-center gap-2">
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={16} />
                        <input
                            type="text"
                            placeholder="Search orgs..."
                            className="bg-slate-900 border border-slate-800 rounded-lg pl-10 pr-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/50 w-64"
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                        />
                    </div>
                    <Button variant="outline" className="border-slate-800 bg-slate-900 hover:bg-slate-800 h-10 w-10 p-0 justify-center">
                        <Filter size={18} />
                    </Button>
                </div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="bg-slate-800/50 text-slate-400 text-xs font-semibold uppercase tracking-wider">
                            <th className="px-6 py-4">Organization</th>
                            <th className="px-6 py-4">Tier</th>
                            <th className="px-6 py-4 text-center">Users</th>
                            <th className="px-6 py-4">Status</th>
                            <th className="px-6 py-4">Joined</th>
                            <th className="px-6 py-4 text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800">
                        {loading ? (
                            [1, 2, 3, 4, 5].map(i => (
                                <tr key={i} className="animate-pulse">
                                    <td colSpan={6} className="px-6 py-4 h-12 bg-slate-900/50" />
                                </tr>
                            ))
                        ) : filteredOrgs.map((org) => (
                            <tr key={org.id} className="hover:bg-slate-800/30 transition-colors group">
                                <td className="px-6 py-4">
                                    <div className="flex items-center gap-3">
                                        <div className="h-10 w-10 bg-indigo-500/10 rounded-lg flex items-center justify-center text-indigo-400">
                                            <Building2 size={20} />
                                        </div>
                                        <div>
                                            <div className="text-sm font-semibold text-white">{org.name}</div>
                                            <div className="text-xs text-slate-500 font-mono">{org.id.split('-')[0]}...</div>
                                        </div>
                                    </div>
                                </td>
                                <td className="px-6 py-4">
                                    <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold uppercase ${org.tier === 'pro' ? 'bg-amber-500/10 text-amber-500 border border-amber-500/20' : org.tier === 'enterprise' ? 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/20' : 'bg-slate-800 text-slate-400'
                                        }`}>
                                        {org.tier}
                                    </span>
                                </td>
                                <td className="px-6 py-4 text-center">
                                    <div className="flex items-center justify-center gap-1.5 text-sm font-medium text-slate-300">
                                        <Users size={14} className="text-slate-500" />
                                        {org.user_count}
                                    </div>
                                </td>
                                <td className="px-6 py-4">
                                    <div className="flex items-center gap-2">
                                        <div className={`h-1.5 w-1.5 rounded-full ${org.subscription_status === 'active' ? 'bg-emerald-500' : 'bg-slate-500'}`} />
                                        <span className="text-sm text-slate-300 capitalize">{org.subscription_status || 'N/A'}</span>
                                    </div>
                                </td>
                                <td className="px-6 py-4 text-sm text-slate-500">
                                    {new Date(org.created_at).toLocaleDateString()}
                                </td>
                                <td className="px-6 py-4 text-right">
                                    <div className="flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                        <Button
                                            variant="outline"
                                            className="h-8 px-2 text-[10px] font-bold uppercase text-slate-400 border-slate-700 hover:text-white"
                                            onClick={() => handleUpdateTier(org.id, org.tier)}
                                        >
                                            Change Tier
                                        </Button>
                                        <Button variant="outline" className="h-8 w-8 p-0 justify-center text-slate-500 hover:text-white">
                                            <ExternalLink size={16} />
                                        </Button>
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>

                {!loading && filteredOrgs.length === 0 && (
                    <div className="py-12 flex flex-col items-center text-slate-500">
                        <Building2 size={40} className="mb-4 opacity-20" />
                        <p>No organizations found matching your search.</p>
                    </div>
                )}
            </div>
        </div>
    );
}
