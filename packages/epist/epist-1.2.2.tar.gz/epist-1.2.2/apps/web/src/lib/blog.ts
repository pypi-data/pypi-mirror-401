import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

const blogDirectory = path.join(process.cwd(), 'content/blog');

export interface BlogPost {
    slug: string;
    meta: {
        title: string;
        date: string;
        description: string;
        author?: string;
        coverImage?: string;
        tags?: string[];
        readTime?: string;
        [key: string]: unknown;
    };
    content: string;
}

export function getBlogPost(slug: string): BlogPost | null {
    const fullPath = path.join(blogDirectory, `${slug}.md`);

    if (!fs.existsSync(fullPath)) {
        return null;
    }

    const fileContents = fs.readFileSync(fullPath, 'utf8');
    const { data, content } = matter(fileContents);

    return {
        slug,
        meta: data as BlogPost['meta'],
        content,
    };
}

export function getAllBlogSlugs(): { slug: string }[] {
    if (!fs.existsSync(blogDirectory)) {
        return [];
    }
    const fileNames = fs.readdirSync(blogDirectory);
    return fileNames
        .filter((fileName) => fileName.endsWith('.md'))
        .map((fileName) => {
            return {
                slug: fileName.replace(/\.md$/, ''),
            };
        });
}

export function getAllBlogPosts(): BlogPost[] {
    const slugs = getAllBlogSlugs();
    const posts = slugs
        .map((slug) => getBlogPost(slug.slug))
        .filter((post): post is BlogPost => post !== null)
        .sort((a, b) => {
            if (a.meta.date && b.meta.date) {
                return new Date(b.meta.date).getTime() - new Date(a.meta.date).getTime();
            }
            return 0;
        });
    return posts;
}
