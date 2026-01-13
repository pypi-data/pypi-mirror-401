"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Calendar, Clock, ArrowRight, User } from "lucide-react";
import { useSearchParams, useRouter } from "next/navigation";
import { BlogPost } from "@/lib/blog";

interface BlogListProps {
    allPosts: BlogPost[];
}

const categories = ["All", "Product", "Tutorial", "Engineering", "Case Study", "Research"];

export function BlogList({ allPosts }: BlogListProps) {
    const searchParams = useSearchParams();
    const router = useRouter();
    const activeTag = searchParams.get("tag") || "All";

    const posts = activeTag !== "All"
        ? allPosts.filter(p => p.meta.tags?.includes(activeTag))
        : allPosts;

    const featuredPost = activeTag === "All" ? posts[0] : null;
    const regularPosts = activeTag === "All" ? posts.slice(1) : posts;

    const handleCategoryClick = (category: string) => {
        if (category === "All") {
            router.push("/blog");
        } else {
            router.push(`/blog?tag=${category}`);
        }
    };

    return (
        <div className="max-w-6xl mx-auto px-6">
            {/* Header */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="text-center mb-16"
            >
                <h1 className="text-4xl md:text-5xl font-bold tracking-tight mb-4">
                    Blog
                </h1>
                <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                    Insights, tutorials, and updates from the Epist team on audio AI,
                    RAG systems, and developer tools.
                </p>
            </motion.div>

            {/* Categories */}
            <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: 0.1 }}
                className="flex flex-wrap justify-center gap-2 mb-12"
            >
                {categories.map((category) => (
                    <button
                        key={category}
                        onClick={() => handleCategoryClick(category)}
                        className={`px-4 py-2 text-sm font-medium rounded-lg transition-all ${activeTag === category
                                ? "bg-primary text-primary-foreground shadow-glow-sm"
                                : "bg-secondary/50 text-muted-foreground hover:text-foreground hover:bg-secondary"
                            }`}
                    >
                        {category}
                    </button>
                ))}
            </motion.div>

            {/* Featured Post */}
            {featuredPost && (
                <motion.article
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.2 }}
                    className="mb-16"
                >
                    <Link href={`/blog/${featuredPost.slug}`} className="group block">
                        <div className="relative overflow-hidden rounded-2xl border border-border bg-card/50 backdrop-blur-sm p-8 md:p-12 transition-all duration-300 hover:border-primary/50 hover:shadow-glow">
                            <div className="absolute top-0 right-0 w-1/2 h-full bg-gradient-to-l from-primary/5 to-transparent pointer-events-none" />

                            <span className="inline-block px-3 py-1 text-xs font-medium bg-primary/20 text-primary rounded-full mb-4">
                                Featured
                            </span>

                            <h2 className="text-2xl md:text-3xl font-bold mb-4 group-hover:text-primary transition-colors">
                                {featuredPost.meta.title}
                            </h2>

                            <p className="text-muted-foreground text-lg mb-6 max-w-3xl">
                                {featuredPost.meta.description}
                            </p>

                            <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground">
                                <span className="flex items-center gap-1.5">
                                    <User size={14} />
                                    {featuredPost.meta.author || "Epist Team"}
                                </span>
                                <span className="flex items-center gap-1.5">
                                    <Calendar size={14} />
                                    {featuredPost.meta.date}
                                </span>
                                {featuredPost.meta.readTime && (
                                    <span className="flex items-center gap-1.5">
                                        <Clock size={14} />
                                        {featuredPost.meta.readTime}
                                    </span>
                                )}
                                <span className="ml-auto flex items-center gap-1 text-primary font-medium opacity-0 group-hover:opacity-100 transition-opacity">
                                    Read article <ArrowRight size={14} />
                                </span>
                            </div>
                        </div>
                    </Link>
                </motion.article>
            )}

            {/* Posts Grid */}
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {regularPosts.map((post, index) => (
                    <motion.article
                        key={post.slug}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.4, delay: 0.3 + index * 0.05 }}
                    >
                        <Link href={`/blog/${post.slug}`} className="group block h-full">
                            <div className="h-full flex flex-col rounded-xl border border-border bg-card/30 backdrop-blur-sm p-6 transition-all duration-300 hover:border-primary/30 hover:bg-card/50">
                                <span className="inline-block self-start px-2.5 py-1 text-xs font-medium bg-secondary text-muted-foreground rounded-md mb-4">
                                    {post.meta.tags?.[0] || "Blog"}
                                </span>

                                <h3 className="text-lg font-semibold mb-3 group-hover:text-primary transition-colors line-clamp-2">
                                    {post.meta.title}
                                </h3>

                                <p className="text-sm text-muted-foreground mb-4 line-clamp-3 flex-grow">
                                    {post.meta.description}
                                </p>

                                <div className="flex items-center gap-3 text-xs text-muted-foreground pt-4 border-t border-border/50">
                                    <span>{post.meta.author || "Epist Team"}</span>
                                    <span>•</span>
                                    <span>{post.meta.date}</span>
                                    {post.meta.readTime && <span className="ml-auto">{post.meta.readTime}</span>}
                                </div>
                            </div>
                        </Link>
                    </motion.article>
                ))}
            </div>

            {posts.length === 0 && (
                <div className="text-center py-20">
                    <p className="text-muted-foreground">No posts found for this category.</p>
                    <button
                        onClick={() => router.push("/blog")}
                        className="mt-4 text-primary hover:underline"
                    >
                        View all posts
                    </button>
                </div>
            )}

            {/* Newsletter CTA */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.6 }}
                className="mt-20 text-center"
            >
                <div className="inline-block p-8 md:p-12 rounded-2xl border border-border bg-card/30 backdrop-blur-sm">
                    <h3 className="text-2xl font-bold mb-3">Stay Updated</h3>
                    <p className="text-muted-foreground mb-6 max-w-md">
                        Get the latest articles, tutorials, and product updates delivered to your inbox.
                    </p>
                    <form className="flex flex-col sm:flex-row gap-3 max-w-md mx-auto" onSubmit={(e) => e.preventDefault()}>
                        <input
                            type="email"
                            placeholder="you@example.com"
                            className="flex-1 px-4 py-3 bg-background border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary"
                        />
                        <button type="submit" className="btn-primary whitespace-nowrap">
                            Subscribe
                        </button>
                    </form>
                </div>
            </motion.div>
        </div>
    );
}
