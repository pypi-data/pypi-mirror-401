import Link from "next/link";
import { Mic, Github } from "lucide-react";

export function Header() {
    return (
        <header className="w-full py-6 px-8 flex justify-between items-center border-b border-white/10 bg-black/20 backdrop-blur-sm fixed top-0 z-50">
            <div className="flex items-center gap-2">
                <Link href="/" className="flex items-center gap-2">
                    <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
                        <Mic className="w-5 h-5 text-white" />
                    </div>
                    <span className="text-xl font-bold tracking-tight text-white">Epist.ai</span>
                </Link>
            </div>
            <nav className="flex gap-6 text-sm font-medium text-gray-400">
                <Link href="/#features" className="hover:text-white transition-colors">Features</Link>
                <Link href="/docs" className="hover:text-white transition-colors">Documentation</Link>
                <Link href="/#blog" className="hover:text-white transition-colors">Blog</Link>
            </nav>
            <div className="flex gap-4">
                <Link
                    href="https://github.com"
                    className="p-2 hover:bg-white/10 rounded-full transition-colors text-white"
                >
                    <Github className="w-5 h-5" />
                </Link>
                <Link
                    href="/dashboard"
                    className="px-4 py-2 bg-white text-black rounded-full text-sm font-bold hover:bg-gray-200 transition-colors"
                >
                    Get Started
                </Link>
            </div>
        </header>
    );
}
