import Link from "next/link";
import Image from "next/image";
import { getBlogPost, getAllBlogSlugs } from "@/lib/blog";
import { ArrowLeft, Calendar, User, Clock } from "lucide-react";
import ReactMarkdown from "react-markdown";
import rehypeHighlight from "rehype-highlight";
import { ShareButtons } from "@/components/blog/ShareButtons";
import Navbar from "@/components/landing/Navbar";
import Footer from "@/components/landing/Footer";
import "highlight.js/styles/github-dark.css";

export async function generateStaticParams() {
    const posts = getAllBlogSlugs();
    return posts.map((post) => ({
        slug: post.slug,
    }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
    const { slug } = await params;
    const post = getBlogPost(slug);

    if (!post) {
        return {
            title: "Post Not Found - Epist.ai",
        };
    }

    const baseUrl = process.env.NEXT_PUBLIC_APP_URL || 'https://epist.ai';
    const postUrl = `${baseUrl}/blog/${slug}`;

    return {
        title: `${post.meta.title} - Epist.ai Blog`,
        description: post.meta.description,
        openGraph: {
            title: post.meta.title,
            description: post.meta.description,
            url: postUrl,
            type: 'article',
            publishedTime: post.meta.date,
            authors: [post.meta.author || 'Epist Team'],
            images: post.meta.coverImage ? [{ url: post.meta.coverImage }] : undefined,
        },
        twitter: {
            card: 'summary_large_image',
            title: post.meta.title,
            description: post.meta.description,
            images: post.meta.coverImage ? [post.meta.coverImage] : undefined,
        },
    };
}

export default async function BlogPostPage({ params }: { params: Promise<{ slug: string }> }) {
    const { slug } = await params;
    const post = getBlogPost(slug);

    if (!post) {
        return (
            <div className="min-h-screen bg-background flex flex-col items-center justify-center">
                <div className="text-center">
                    <h1 className="text-4xl font-bold mb-4">Post Not Found</h1>
                    <Link href="/blog" className="text-primary hover:underline">
                        Return to Blog
                    </Link>
                </div>
            </div>
        );
    }

    const baseUrl = process.env.NEXT_PUBLIC_APP_URL || 'https://epist.ai';
    const postUrl = `${baseUrl}/blog/${slug}`;

    return (
        <div className="min-h-screen bg-background bg-grid relative overflow-x-hidden selection:bg-primary/30 selection:text-foreground">
            <Navbar />

            <main className="pt-32 pb-24 px-6">
                <article className="max-w-4xl mx-auto">
                    <Link href="/blog" className="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground mb-12 transition-colors">
                        <ArrowLeft size={16} /> Back to Blog
                    </Link>

                    <header className="mb-12">
                        <div className="flex flex-wrap items-center gap-4 text-sm text-primary mb-6 font-medium">
                            <span className="px-3 py-1 rounded-full bg-primary/20 text-primary">
                                {post.meta.tags?.[0] || "Blog"}
                            </span>
                            <span className="flex items-center gap-1.5 text-muted-foreground">
                                <Calendar size={14} />
                                {post.meta.date}
                            </span>
                            {post.meta.readTime && (
                                <span className="flex items-center gap-1.5 text-muted-foreground">
                                    <Clock size={14} />
                                    {post.meta.readTime}
                                </span>
                            )}
                        </div>

                        <h1 className="text-4xl md:text-5xl font-bold mb-8 leading-tight tracking-tight">
                            {post.meta.title}
                        </h1>

                        <div className="flex items-center justify-between py-8 border-y border-border/50">
                            <div className="flex items-center gap-4">
                                <div className="w-12 h-12 rounded-full bg-secondary flex items-center justify-center border border-border">
                                    <User size={20} className="text-muted-foreground" />
                                </div>
                                <div>
                                    <p className="text-base font-semibold">{post.meta.author || "Epist Team"}</p>
                                    <p className="text-sm text-muted-foreground font-medium">Author</p>
                                </div>
                            </div>

                            <ShareButtons url={postUrl} title={post.meta.title} />
                        </div>
                    </header>

                    {post.meta.coverImage && (
                        <div className="mb-12 rounded-2xl overflow-hidden border border-border bg-card/50">
                            <Image
                                src={post.meta.coverImage}
                                alt={post.meta.title}
                                width={1200}
                                height={600}
                                className="w-full h-auto"
                                unoptimized
                            />
                        </div>
                    )}

                    <div className="prose prose-zinc prose-invert prose-lg max-w-none 
                        prose-headings:text-foreground prose-headings:font-bold prose-headings:tracking-tight
                        prose-p:text-muted-foreground prose-p:leading-relaxed
                        prose-a:text-primary prose-a:no-underline hover:prose-a:underline
                        prose-strong:text-foreground prose-strong:font-semibold
                        prose-code:text-primary prose-code:bg-primary/10 prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded-md prose-code:font-mono prose-code:before:content-none prose-code:after:content-none
                        prose-pre:bg-card prose-pre:border prose-pre:border-border prose-pre:rounded-xl prose-pre:p-6
                        prose-blockquote:border-l-primary prose-blockquote:bg-primary/5 prose-blockquote:py-2 prose-blockquote:pr-6 prose-blockquote:pl-8 prose-blockquote:rounded-r-xl prose-blockquote:text-lg prose-blockquote:italic prose-blockquote:text-foreground/80">
                        <ReactMarkdown rehypePlugins={[rehypeHighlight]}>
                            {post.content}
                        </ReactMarkdown>
                    </div>

                    <div className="mt-20 pt-10 border-t border-border/50">
                        <h3 className="text-xl font-bold mb-6">Tags</h3>
                        <div className="flex flex-wrap gap-2">
                            {post.meta.tags?.map((tag: string) => (
                                <Link
                                    key={tag}
                                    href={`/blog?tag=${encodeURIComponent(tag)}`}
                                    className="px-4 py-1.5 rounded-lg bg-secondary text-muted-foreground text-sm font-medium hover:text-foreground hover:bg-secondary/80 transition-all border border-border/50"
                                >
                                    #{tag}
                                </Link>
                            )) || (
                                    <span className="text-muted-foreground italic">No tags</span>
                                )}
                        </div>
                    </div>
                </article>
            </main>

            <Footer />
        </div>
    );
}
