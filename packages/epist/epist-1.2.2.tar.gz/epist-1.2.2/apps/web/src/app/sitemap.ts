import { MetadataRoute } from 'next';

export const dynamic = 'force-static';

export default function sitemap(): MetadataRoute.Sitemap {
    const baseUrl = 'https://epist.ai';

    // Static routes
    const routes = [
        '',
        '/pricing',
        '/docs',
        '/blog',
        '/login',
    ].map((route) => ({
        url: `${baseUrl}${route}`,
        lastModified: new Date(),
        changeFrequency: 'weekly' as const,
        priority: route === '' ? 1 : 0.8,
    }));

    // In a real app, we would fetch dynamic routes from the API here
    // e.g., blog slugs, public share pages

    return [...routes];
}
