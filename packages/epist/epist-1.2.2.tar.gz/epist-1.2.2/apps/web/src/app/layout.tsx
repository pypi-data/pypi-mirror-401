import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Toaster } from "sonner";
import { ClientLayout } from "@/components/ClientLayout";
import { CookieConsent } from "@/components/legal/CookieConsent";
import { PostHogProvider } from "@/components/providers/PostHogProvider";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  metadataBase: new URL("https://epist.ai"),
  title: {
    default: "Epist.ai - Audio Intelligence for Developers",
    template: "%s | Epist.ai",
  },
  description: "Production-ready REST API for audio transcription, chunking, and RAG. Built for developers and AI engineers.",
  keywords: ["Audio RAG", "AI Transcription", "Developer API", "Podcast Search", "Knowledge Base", "Audio Analysis"],
  authors: [{ name: "Epist Team" }],
  creator: "Epist.ai",
  openGraph: {
    title: "Epist.ai - Audio Intelligence for Developers",
    description: "Production-ready REST API for audio transcription, chunking, and RAG.",
    url: "https://epist.ai",
    siteName: "Epist.ai",
    type: "website",
    locale: "en_US",
  },
  twitter: {
    card: "summary_large_image",
    title: "Epist.ai - Audio Intelligence for Developers",
    description: "Production-ready REST API for audio transcription, search, and RAG.",
    creator: "@epist_ai",
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  // Note: usePathname is a client hook, so we need to split this component if we want metadata to work properly 
  // in a server component layout. However, since this is the root layout and we need client-side logic for nav,
  // we might need to separate the client logic into a wrapper component.
  // BUT, 'use client' at the top makes the whole layout a client component, which disables Metadata export support in the same file.
  // We must remove 'use client' from this file and move the client logic (Nav, AuthProvider) to a separate component.

  return (
    <html lang="en" suppressHydrationWarning className="dark">
      <body className={`${inter.className} bg-slate-950 text-slate-50 selection:bg-indigo-500/30 font-sans antialiased`}>
        <PostHogProvider>
          <ClientLayout>
            {children}
          </ClientLayout>
        </PostHogProvider>
        <CookieConsent />
        <Toaster position="top-right" theme="dark" />
      </body>
    </html>
  );
}
