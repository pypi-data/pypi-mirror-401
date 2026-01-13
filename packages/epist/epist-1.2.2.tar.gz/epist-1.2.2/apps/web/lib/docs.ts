import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

const docsDirectory = path.join(process.cwd(), 'content/docs');

export function getDocSlugs() {
    return fs.readdirSync(docsDirectory);
}

export function getDocBySlug(slug: string) {
    const realSlug = slug.replace(/\.md$/, '');
    const fullPath = path.join(docsDirectory, `${realSlug}.md`);
    const fileContents = fs.readFileSync(fullPath, 'utf8');
    const { data, content } = matter(fileContents);

    return { slug: realSlug, meta: data, content };
}

export function getAllDocs() {
    const slugs = getDocSlugs();
    const docs = slugs.map((slug) => getDocBySlug(slug));
    return docs;
}
