import Link from "next/link";
import { ArrowRight, Zap, Terminal, Server } from "lucide-react";

export function GettingStarted() {
    return (
        <div className="mb-12">
            <h2 className="text-xl font-bold mb-6">Getting Started</h2>
            <div className="grid md:grid-cols-3 gap-6">
                {/* Quickstart */}
                <Link href="/docs" className="group relative overflow-hidden rounded-xl bg-gradient-to-br from-indigo-500/10 to-purple-500/10 border border-indigo-500/20 p-6 hover:border-indigo-500/40 transition-all">
                    <div className="absolute top-0 right-0 p-4 opacity-50 group-hover:opacity-100 transition-opacity">
                        <ArrowRight className="text-indigo-400 -rotate-45 group-hover:rotate-0 transition-transform" />
                    </div>
                    <div className="mb-4 p-3 bg-indigo-500/20 rounded-lg w-fit text-indigo-400">
                        <Zap size={24} />
                    </div>
                    <h3 className="text-lg font-semibold mb-2 text-white">Quickstart Guide</h3>
                    <p className="text-sm text-slate-400 mb-4">Learn the basics of the API and start building in minutes.</p>
                    <span className="text-xs font-medium text-indigo-400 group-hover:text-indigo-300">Read Docs →</span>
                </Link>

                {/* Playground */}
                <Link href="/dashboard/playground" className="group relative overflow-hidden rounded-xl bg-gradient-to-br from-cyan-500/10 to-blue-500/10 border border-cyan-500/20 p-6 hover:border-cyan-500/40 transition-all">
                    <div className="absolute top-0 right-0 p-4 opacity-50 group-hover:opacity-100 transition-opacity">
                        <ArrowRight className="text-cyan-400 -rotate-45 group-hover:rotate-0 transition-transform" />
                    </div>
                    <div className="mb-4 p-3 bg-cyan-500/20 rounded-lg w-fit text-cyan-400">
                        <Terminal size={24} />
                    </div>
                    <h3 className="text-lg font-semibold mb-2 text-white">API Playground</h3>
                    <p className="text-sm text-slate-400 mb-4">Test endpoints interactively right from your browser.</p>
                    <span className="text-xs font-medium text-cyan-400 group-hover:text-cyan-300">Try it out →</span>
                </Link>

                {/* MCP Server */}
                {/* MCP Server */}
                <Link href="/docs" className="group relative overflow-hidden rounded-xl bg-gradient-to-br from-emerald-500/10 to-teal-500/10 border border-emerald-500/20 p-6 hover:border-emerald-500/40 transition-all">
                    <div className="absolute top-0 right-0 p-4 opacity-50 group-hover:opacity-100 transition-opacity">
                        <ArrowRight className="text-emerald-400 -rotate-45 group-hover:rotate-0 transition-transform" />
                    </div>
                    <div className="mb-4 p-3 bg-emerald-500/20 rounded-lg w-fit text-emerald-400">
                        <Server size={24} />
                    </div>
                    <h3 className="text-lg font-semibold mb-2 text-white">MCP Server</h3>
                    <p className="text-sm text-slate-400 mb-4">Connect your audio data directly to Claude Desktop.</p>
                    <span className="text-xs font-medium text-emerald-400 group-hover:text-emerald-300">Setup Server →</span>
                </Link>
            </div>
        </div>
    );
}
