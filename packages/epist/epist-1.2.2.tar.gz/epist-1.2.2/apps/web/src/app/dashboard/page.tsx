"use client";

import { Music, FileText, Layers, Loader2 } from "lucide-react";
import StatCard from "@/components/dashboard/StatCard";
import OnboardingCard from "@/components/dashboard/OnboardingCard";
import ApiKeyCard from "@/components/dashboard/ApiKeyCard";
import AudioResourcesCard from "@/components/dashboard/AudioResourcesCard";
import SupportCard from "@/components/dashboard/SupportCard";
import { useEffect, useState } from "react";
import { api, SystemStats } from "@/lib/api";

const Dashboard = () => {
    const [stats, setStats] = useState<SystemStats | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const data = await api.getStats();
                setStats(data);
            } catch {
                console.error("Failed to fetch dashboard stats");
            } finally {
                setIsLoading(false);
            }
        };
        fetchStats();
    }, []);

    return (
        <div className="max-w-7xl mx-auto space-y-6">
            {/* Page Header */}
            <div className="mb-8">
                <h1 className="text-2xl font-bold tracking-tight text-foreground mb-1">Dashboard</h1>
                <p className="text-muted-foreground">Welcome back. Here&apos;s an overview of your audio resources.</p>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                {isLoading ? (
                    Array(3).fill(0).map((_, i) => (
                        <div key={i} className="h-32 rounded-2xl bg-card/50 animate-pulse border border-border/50 flex items-center justify-center">
                            <Loader2 className="w-5 h-5 animate-spin text-muted-foreground" />
                        </div>
                    ))
                ) : (
                    <>
                        <StatCard
                            title="Total Audio Files"
                            value={stats?.audio_count || 0}
                            icon={Music}
                        />
                        <StatCard
                            title="Total Transcripts"
                            value={stats?.transcript_count || 0}
                            icon={FileText}
                        />
                        <StatCard
                            title="Total Segments"
                            value={stats?.segment_count?.toLocaleString() || 0}
                            icon={Layers}
                        />
                    </>
                )}
            </div>

            {/* Onboarding */}
            <OnboardingCard />

            {/* Main Grid */}
            <div className="grid lg:grid-cols-2 gap-6">
                <ApiKeyCard />
                <AudioResourcesCard />
            </div>

            {/* Support */}
            <SupportCard />
        </div>
    );
};

export default Dashboard;
