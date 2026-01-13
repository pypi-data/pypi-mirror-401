"use client";

import React, { useEffect, useState } from "react";
import {
    Users,
    Search,
    Mail,
    Clock,
    MoreVertical,
    ShieldCheck
} from "lucide-react";
import { api, AdminUser as User } from "@/lib/api";
import { Button } from "@/components/ui/button";

export default function AdminUsers() {
    const [users, setUsers] = useState<User[]>([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState("");

    useEffect(() => {
        async function fetchUsers() {
            // For now, we reuse the stats or a list if implemented
            // Let's assume we have a list users endpoint or we might need to add one
            try {
                const data = await api.getAdminUsers();
                setUsers(data);
            } catch (error) {
                console.error("Failed to fetch users", error);
                // Fallback or empty state
            } finally {
                setLoading(false);
            }
        }
        fetchUsers();
    }, []);

    const filteredUsers = users.filter(user =>
        user.email.toLowerCase().includes(search.toLowerCase()) ||
        user.full_name.toLowerCase().includes(search.toLowerCase())
    );

    const handleToggleSuperuser = async (userId: string, currentStatus: boolean) => {
        if (!confirm(`Are you sure you want to ${currentStatus ? 'revoke' : 'grant'} superuser status?`)) return;
        try {
            await api.updateAdminUser(userId, { is_superuser: !currentStatus });
            setUsers(users.map(u => u.id === userId ? { ...u, is_superuser: !currentStatus } : u));
        } catch (error) {
            console.error("Failed to update user", error);
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h2 className="text-2xl font-bold text-white">User Management</h2>
                    <p className="text-slate-400 text-sm">Monitor user activity and system privileges.</p>
                </div>

                <div className="flex items-center gap-2">
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={16} />
                        <input
                            type="text"
                            placeholder="Search users..."
                            className="bg-slate-900 border border-slate-800 rounded-lg pl-10 pr-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/50 w-64"
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                        />
                    </div>
                </div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="bg-slate-800/50 text-slate-400 text-xs font-semibold uppercase tracking-wider">
                            <th className="px-6 py-4">User</th>
                            <th className="px-6 py-4">Role</th>
                            <th className="px-6 py-4">Status</th>
                            <th className="px-6 py-4">Organization ID</th>
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
                        ) : filteredUsers.map((user) => (
                            <tr key={user.id} className="hover:bg-slate-800/30 transition-colors group">
                                <td className="px-6 py-4">
                                    <div className="flex items-center gap-3">
                                        <div className="h-10 w-10 bg-slate-800 rounded-full flex items-center justify-center text-slate-400 border border-slate-700">
                                            {user.full_name?.charAt(0) || user.email.charAt(0)}
                                        </div>
                                        <div>
                                            <div className="text-sm font-semibold text-white flex items-center gap-2">
                                                {user.full_name || 'No Name'}
                                                {user.is_superuser && <ShieldCheck size={14} className="text-indigo-400" />}
                                            </div>
                                            <div className="text-xs text-slate-500 flex items-center gap-1">
                                                <Mail size={12} />
                                                {user.email}
                                            </div>
                                        </div>
                                    </div>
                                </td>
                                <td className="px-6 py-4">
                                    <div className="flex items-center gap-2 text-sm text-slate-300">
                                        {user.is_superuser ? (
                                            <span className="flex items-center gap-1 text-indigo-400 font-bold text-[10px] uppercase tracking-tight px-1.5 py-0.5 bg-indigo-500/10 border border-indigo-500/20 rounded">
                                                Superuser
                                            </span>
                                        ) : (
                                            <span className="capitalize">{user.role}</span>
                                        )}
                                    </div>
                                </td>
                                <td className="px-6 py-4">
                                    <div className="flex items-center gap-2">
                                        <div className={`h-1.5 w-1.5 rounded-full ${user.is_active ? 'bg-emerald-500' : 'bg-rose-500'}`} />
                                        <span className="text-sm text-slate-300">{user.is_active ? 'Active' : 'Deactivated'}</span>
                                    </div>
                                </td>
                                <td className="px-6 py-4 text-xs font-mono text-slate-500">
                                    {user.organization_id?.split('-')[0] || 'N/A'}...
                                </td>
                                <td className="px-6 py-4 text-sm text-slate-500 whitespace-nowrap">
                                    <div className="flex items-center gap-1.5">
                                        <Clock size={14} />
                                        {new Date(user.created_at).toLocaleDateString()}
                                    </div>
                                </td>
                                <td className="px-6 py-4 text-right">
                                    <div className="flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                        <Button
                                            variant="outline"
                                            className={`h-8 px-2 text-[10px] font-bold uppercase ${user.is_superuser ? 'text-rose-400 border-rose-500/20 hover:bg-rose-500/10' : 'text-indigo-400 border-indigo-500/20 hover:bg-indigo-500/10'}`}
                                            onClick={() => handleToggleSuperuser(user.id, user.is_superuser)}
                                        >
                                            {user.is_superuser ? 'Revoke Super' : 'Grant Super'}
                                        </Button>
                                        <Button variant="outline" className="h-8 w-8 p-0 justify-center text-slate-500 hover:text-white">
                                            <MoreVertical size={16} />
                                        </Button>
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>

                {!loading && filteredUsers.length === 0 && (
                    <div className="py-24 flex flex-col items-center text-slate-500">
                        <Users size={40} className="mb-4 opacity-20" />
                        <p>No users found matching your search.</p>
                    </div>
                )}
            </div>
        </div>
    );
}
