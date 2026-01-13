import { LucideIcon } from "lucide-react";

interface MetricCardProps {
    label: string;
    value: string | number;
    icon: LucideIcon;
    change?: string;
    trend?: "up" | "down" | "neutral";
    unit?: string;
}

export function MetricCard({ label, value, icon: Icon, change, trend = "neutral", unit }: MetricCardProps) {
    const trendColors = {
        up: "text-green-400",
        down: "text-red-400",
        neutral: "text-zinc-400",
    };

    return (
        <div className="metric-card">
            <div className="flex items-start justify-between mb-4">
                <div className="p-2 bg-zinc-800 rounded-lg">
                    <Icon className="w-5 h-5 text-zinc-400" />
                </div>
                {change && (
                    <span className={`text-xs font-mono ${trendColors[trend]}`}>
                        {change}
                    </span>
                )}
            </div>
            <div>
                <p className="text-xs text-zinc-500 uppercase tracking-wide mb-1">{label}</p>
                <p className="text-2xl font-bold text-zinc-100 font-mono">
                    {value}
                    {unit && <span className="text-sm text-zinc-400 ml-1">{unit}</span>}
                </p>
            </div>
        </div>
    );
}
