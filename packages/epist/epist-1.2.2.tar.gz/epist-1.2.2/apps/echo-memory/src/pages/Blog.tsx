import { motion } from "framer-motion";
import { Calendar, Clock, ArrowRight, User } from "lucide-react";
import { Link } from "react-router-dom";
import Navbar from "@/components/landing/Navbar";
import Footer from "@/components/landing/Footer";

interface BlogPost {
  id: string;
  title: string;
  excerpt: string;
  author: string;
  date: string;
  readTime: string;
  category: string;
  featured?: boolean;
  image?: string;
}

const blogPosts: BlogPost[] = [
  {
    id: "introducing-audio-rag",
    title: "Introducing Audio RAG: The Future of Voice-First Search",
    excerpt: "Learn how Retrieval-Augmented Generation is transforming the way we interact with audio content, enabling semantic search across hours of recordings.",
    author: "Alex Chen",
    date: "Dec 18, 2024",
    readTime: "8 min read",
    category: "Product",
    featured: true,
  },
  {
    id: "building-voice-assistants",
    title: "Building Voice Assistants with Epist SDK",
    excerpt: "A comprehensive guide to creating intelligent voice assistants that can understand context and provide accurate responses from your audio library.",
    author: "Sarah Kim",
    date: "Dec 15, 2024",
    readTime: "12 min read",
    category: "Tutorial",
  },
  {
    id: "audio-chunking-strategies",
    title: "Audio Chunking Strategies for Optimal RAG Performance",
    excerpt: "Explore different approaches to segmenting audio content for maximum retrieval accuracy and response quality.",
    author: "Marcus Johnson",
    date: "Dec 10, 2024",
    readTime: "6 min read",
    category: "Engineering",
  },
  {
    id: "podcast-search-case-study",
    title: "Case Study: Semantic Search for 10,000+ Podcast Episodes",
    excerpt: "How a major podcast network implemented Epist to make their entire archive searchable with natural language queries.",
    author: "Emily Zhang",
    date: "Dec 5, 2024",
    readTime: "10 min read",
    category: "Case Study",
  },
  {
    id: "transcription-accuracy",
    title: "Achieving 99% Transcription Accuracy: Our Approach",
    excerpt: "Deep dive into the techniques and models we use to ensure industry-leading transcription quality across languages and accents.",
    author: "David Park",
    date: "Nov 28, 2024",
    readTime: "7 min read",
    category: "Engineering",
  },
  {
    id: "audio-rag-vs-text",
    title: "Audio RAG vs. Text RAG: Key Differences and Considerations",
    excerpt: "Understanding the unique challenges and opportunities when applying RAG techniques to audio content versus traditional text documents.",
    author: "Alex Chen",
    date: "Nov 20, 2024",
    readTime: "9 min read",
    category: "Research",
  },
];

const categories = ["All", "Product", "Tutorial", "Engineering", "Case Study", "Research"];

const Blog = () => {
  const featuredPost = blogPosts.find((post) => post.featured);
  const regularPosts = blogPosts.filter((post) => !post.featured);

  return (
    <div className="min-h-screen bg-background text-foreground">
      <Navbar />

      <main className="pt-32 pb-24 px-6">
        <div className="max-w-6xl mx-auto">
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
                className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
                  category === "All"
                    ? "bg-primary text-primary-foreground"
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
              <Link to={`/blog/${featuredPost.id}`} className="group block">
                <div className="relative overflow-hidden rounded-2xl border border-border bg-card/50 backdrop-blur-sm p-8 md:p-12 transition-all duration-300 hover:border-primary/50 hover:shadow-glow">
                  <div className="absolute top-0 right-0 w-1/2 h-full bg-gradient-to-l from-primary/5 to-transparent pointer-events-none" />
                  
                  <span className="inline-block px-3 py-1 text-xs font-medium bg-primary/20 text-primary rounded-full mb-4">
                    Featured
                  </span>
                  
                  <h2 className="text-2xl md:text-3xl font-bold mb-4 group-hover:text-primary transition-colors">
                    {featuredPost.title}
                  </h2>
                  
                  <p className="text-muted-foreground text-lg mb-6 max-w-3xl">
                    {featuredPost.excerpt}
                  </p>
                  
                  <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground">
                    <span className="flex items-center gap-1.5">
                      <User size={14} />
                      {featuredPost.author}
                    </span>
                    <span className="flex items-center gap-1.5">
                      <Calendar size={14} />
                      {featuredPost.date}
                    </span>
                    <span className="flex items-center gap-1.5">
                      <Clock size={14} />
                      {featuredPost.readTime}
                    </span>
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
                key={post.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: 0.3 + index * 0.05 }}
              >
                <Link to={`/blog/${post.id}`} className="group block h-full">
                  <div className="h-full flex flex-col rounded-xl border border-border bg-card/30 backdrop-blur-sm p-6 transition-all duration-300 hover:border-primary/30 hover:bg-card/50">
                    <span className="inline-block self-start px-2.5 py-1 text-xs font-medium bg-secondary text-muted-foreground rounded-md mb-4">
                      {post.category}
                    </span>
                    
                    <h3 className="text-lg font-semibold mb-3 group-hover:text-primary transition-colors line-clamp-2">
                      {post.title}
                    </h3>
                    
                    <p className="text-sm text-muted-foreground mb-4 line-clamp-3 flex-grow">
                      {post.excerpt}
                    </p>
                    
                    <div className="flex items-center gap-3 text-xs text-muted-foreground pt-4 border-t border-border/50">
                      <span>{post.author}</span>
                      <span>•</span>
                      <span>{post.date}</span>
                      <span className="ml-auto">{post.readTime}</span>
                    </div>
                  </div>
                </Link>
              </motion.article>
            ))}
          </div>

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
              <form className="flex flex-col sm:flex-row gap-3 max-w-md mx-auto">
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
      </main>

      <Footer />
    </div>
  );
};

export default Blog;
