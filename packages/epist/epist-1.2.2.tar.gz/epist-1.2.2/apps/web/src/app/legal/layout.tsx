import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";

export default function LegalLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="min-h-screen flex flex-col bg-black text-white">
            <Header />
            <main className="flex-1 pt-32 pb-20 px-4">
                <div className="max-w-3xl mx-auto prose prose-invert">
                    {children}
                </div>
            </main>
            <Footer />
        </div>
    );
}
