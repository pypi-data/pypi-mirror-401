import { getAllBlogPosts } from "@/lib/blog";
import { BlogList } from "@/components/blog/BlogList";
import { Suspense } from "react";
import Navbar from "@/components/landing/Navbar";
import Footer from "@/components/landing/Footer";

export const metadata = {
    title: "Blog - Epist.ai",
    description: "Insights, tutorials, and updates from the Epist.ai team.",
};

export default function BlogPage() {
    const allPosts = getAllBlogPosts();

    return (
        <div className="min-h-screen bg-background bg-grid relative overflow-x-hidden selection:bg-primary/30 selection:text-foreground">
            <Navbar />
            <main className="pt-32 pb-24">
                <Suspense fallback={
                    <div className="max-w-7xl mx-auto px-6 text-center py-20">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
                    </div>
                }>
                    <BlogList allPosts={allPosts} />
                </Suspense>
            </main>
            <Footer />
        </div>
    );
}
