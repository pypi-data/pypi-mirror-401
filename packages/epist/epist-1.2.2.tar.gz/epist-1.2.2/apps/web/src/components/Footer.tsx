import Link from "next/link";

export function Footer() {
    return (
        <footer className="w-full py-8 border-t border-white/10 text-center text-gray-500 text-sm">
            <div className="flex flex-col items-center gap-4">
                <div className="flex gap-6">
                    <Link href="/legal/privacy-policy" className="hover:text-gray-300 transition-colors">
                        Privacy Policy
                    </Link>
                    <Link href="/legal/terms-of-service" className="hover:text-gray-300 transition-colors">
                        Terms of Service
                    </Link>
                    <a href="mailto:admin@epist.ai" className="hover:text-gray-300 transition-colors">
                        Contact
                    </a>
                </div>
                <p>© 2024 Epist.ai. Open Source.</p>
            </div>
        </footer>
    );
}
