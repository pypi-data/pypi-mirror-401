import { LucideIcon } from "lucide-react";
import { cn } from "@/lib/utils";

interface StatCardProps {
    title: string;
    value: string | number;
    icon: LucideIcon;
    trend?: {
        value: number;
        positive: boolean;
    };
    className?: string;
}

const StatCard = ({ title, value, icon: Icon, trend, className }: StatCardProps) => {
    return (
        <div
            className={cn(
                "group relative p-6 rounded-2xl",
                "bg-card/50 backdrop-blur-xl border border-border/50",
                "hover:border-primary/30 hover:bg-card/70 transition-all duration-300",
                className
            )}
        >
            {/* Glow effect on hover */}
            <div className="absolute inset-0 rounded-2xl bg-primary/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

            <div className="relative flex items-start justify-between">
                <div className="space-y-3">
                    <p className="text-sm font-medium text-muted-foreground">{title}</p>
                    <p className="text-3xl font-bold tracking-tight text-foreground">{value}</p>
                    {trend && (
                        <div className="flex items-center gap-1">
                            <span
                                className={cn(
                                    "text-xs font-medium",
                                    trend.positive ? "text-emerald-400" : "text-red-400"
                                )}
                            >
                                {trend.positive ? "+" : ""}{trend.value}%
                            </span>
                            <span className="text-xs text-muted-foreground">vs last month</span>
                        </div>
                    )}
                </div>

                <div className="p-3 rounded-xl bg-primary/10 border border-primary/20 group-hover:bg-primary/20 transition-colors duration-300">
                    <Icon className="w-5 h-5 text-primary" />
                </div>
            </div>
        </div>
    );
};

export default StatCard;
