import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

const legalDirectory = path.join(process.cwd(), 'content/legal');

export function getLegalDocument(slug: string) {
    const fullPath = path.join(legalDirectory, `${slug}.md`);

    if (!fs.existsSync(fullPath)) {
        return null;
    }

    const fileContents = fs.readFileSync(fullPath, 'utf8');
    const { data, content } = matter(fileContents);

    return {
        slug,
        meta: data,
        content,
    };
}

export function getAllLegalSlugs() {
    if (!fs.existsSync(legalDirectory)) {
        return [];
    }
    const fileNames = fs.readdirSync(legalDirectory);
    return fileNames.map((fileName) => {
        return {
            slug: fileName.replace(/\.md$/, ''),
        };
    });
}
