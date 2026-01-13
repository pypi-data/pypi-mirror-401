import { Music, FileText, Layers } from "lucide-react";
import StatCard from "@/components/dashboard/StatCard";
import OnboardingCard from "@/components/dashboard/OnboardingCard";
import ApiKeyCard from "@/components/dashboard/ApiKeyCard";
import AudioResourcesCard from "@/components/dashboard/AudioResourcesCard";
import SupportCard from "@/components/dashboard/SupportCard";

const Dashboard = () => {
  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold tracking-tight text-foreground mb-1">Dashboard</h1>
        <p className="text-muted-foreground">Welcome back. Here's an overview of your audio resources.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <StatCard
          title="Total Audio Files"
          value={24}
          icon={Music}
          trend={{ value: 12, positive: true }}
        />
        <StatCard
          title="Total Transcripts"
          value={18}
          icon={FileText}
          trend={{ value: 8, positive: true }}
        />
        <StatCard
          title="Total Segments"
          value="1,284"
          icon={Layers}
          trend={{ value: 24, positive: true }}
        />
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
