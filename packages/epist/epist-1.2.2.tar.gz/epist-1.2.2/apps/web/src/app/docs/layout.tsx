import { RootProvider } from 'fumadocs-ui/provider/next';
import type { ReactNode } from 'react';
import { Sidebar } from './Sidebar';
import { source } from '@/lib/source';

export default function Layout({ children }: { children: ReactNode }) {
    return (
        <RootProvider theme={{ defaultTheme: 'dark', forcedTheme: 'dark' }}>
            <div className="flex h-screen bg-background text-foreground overflow-hidden">
                {/* Fixed Sidebar */}
                <Sidebar tree={source.pageTree} />

                {/* Main Content Area */}
                <main className="flex-1 ml-64 h-full overflow-y-auto relative">
                    <div className="min-h-full p-8 md:p-12 max-w-7xl mx-auto">
                        {children}
                    </div>
                </main>
            </div>
        </RootProvider>
    );
}
