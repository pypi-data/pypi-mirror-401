import { source } from '@/lib/source';
import {
    DocsBody,
    DocsDescription,
    DocsTitle,
} from 'fumadocs-ui/page';
import { notFound } from 'next/navigation';
import defaultMdxComponents from 'fumadocs-ui/mdx';

interface PageData {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    body: (props: { components: any }) => React.ReactElement;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    toc: any;
    full: boolean;
    title: string;
    description?: string;
}

export default async function Page(props: {
    params: Promise<{ slug?: string[] }>;
}) {
    const params = await props.params;
    const page = source.getPage(params.slug);
    if (!page) notFound();

    const data = page.data as unknown as PageData;
    const MDX = data.body;

    return (
        <div className="flex flex-col gap-8 pb-20">
            <div className="flex flex-col gap-2">
                <DocsTitle>{data.title}</DocsTitle>
                <DocsDescription>{data.description}</DocsDescription>
            </div>
            <DocsBody>
                <MDX components={{ ...defaultMdxComponents }} />
            </DocsBody>
        </div>
    );
}

export async function generateStaticParams() {
    return source.generateParams();
}

export async function generateMetadata(props: {
    params: Promise<{ slug?: string[] }>;
}) {
    const params = await props.params;
    const page = source.getPage(params.slug);
    if (!page) notFound();

    return {
        title: page.data.title,
        description: page.data.description,
    };
}
export const dynamicParams = false;
