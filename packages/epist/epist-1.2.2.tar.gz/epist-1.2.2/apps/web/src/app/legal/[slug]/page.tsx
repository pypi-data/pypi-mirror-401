import { getLegalDocument, getAllLegalSlugs } from "@/lib/legal";
import { notFound } from "next/navigation";
import ReactMarkdown from "react-markdown";

export async function generateStaticParams() {
    const slugs = getAllLegalSlugs();
    return slugs;
}

export default async function LegalPage({
    params,
}: {
    params: Promise<{ slug: string }>;
}) {
    const { slug } = await params;
    const document = getLegalDocument(slug);

    if (!document) {
        notFound();
    }

    return (
        <article className="prose prose-invert max-w-none">
            <ReactMarkdown>{document.content}</ReactMarkdown>
        </article>
    );
}
