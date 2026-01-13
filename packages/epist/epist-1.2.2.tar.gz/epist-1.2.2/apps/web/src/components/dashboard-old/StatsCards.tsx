import { BarChart3, Mic, Search, CreditCard } from "lucide-react";
import { SystemStats } from "@/lib/api";

interface StatsCardsProps {
    stats: SystemStats;
}

export function StatsCards({ stats }: StatsCardsProps) {
    return (
        <div>
            <h2 className="text-xl font-bold mb-6 flex items-center gap-2"><BarChart3 size={20} /> System Status</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-8 mb-8">
                <div className="p-6 rounded-xl bg-slate-900 border border-slate-800">
                    <div className="flex justify-between items-start mb-4">
                        <div className="p-2 bg-indigo-500/10 rounded-lg text-indigo-400"><Mic size={20} /></div>
                        <span className="text-xs font-medium text-green-400 bg-green-500/10 px-2 py-1 rounded">Live</span>
                    </div>
                    <div className="text-3xl font-bold mb-1">{stats.audio_count}</div>
                    <div className="text-sm text-slate-500">Audio Files Processed</div>
                </div>

                <div className="p-6 rounded-xl bg-slate-900 border border-slate-800">
                    <div className="flex justify-between items-start mb-4">
                        <div className="p-2 bg-cyan-500/10 rounded-lg text-cyan-400"><Search size={20} /></div>
                        <span className="text-xs font-medium text-green-400 bg-green-500/10 px-2 py-1 rounded">Live</span>
                    </div>
                    <div className="text-3xl font-bold mb-1">{stats.segment_count}</div>
                    <div className="text-sm text-slate-500">Indexed Segments</div>
                </div>

                <div className="p-6 rounded-xl bg-slate-900 border border-slate-800">
                    <div className="flex justify-between items-start mb-4">
                        <div className="p-2 bg-purple-500/10 rounded-lg text-purple-400"><CreditCard size={20} /></div>
                        <span className="text-xs font-medium text-slate-400 bg-slate-800 px-2 py-1 rounded">Pro Plan</span>
                    </div>
                    <div className="text-3xl font-bold mb-1">$0.00</div>
                    <div className="text-sm text-slate-500">Current usage</div>
                </div>
            </div>

            {/* Usage Chart (Visual Only) */}
            <div className="h-48 bg-slate-900 border border-slate-800 rounded-xl p-6 flex items-end justify-between gap-2">
                {[30, 45, 25, 60, 75, 40, 50, 70, 55, 80, 65, 90, 40, 55].map((h, i) => (
                    <div key={i} className="w-full bg-indigo-500/20 hover:bg-indigo-500/40 transition-colors rounded-t-md relative group" style={{ height: `${h}%` }}>
                        <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-slate-800 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
                            {h}reqs
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
