"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { X } from "lucide-react";

export function CookieConsent() {
    const [isVisible, setIsVisible] = useState(false);

    useEffect(() => {
        const consent = localStorage.getItem("cookie_consent");
        if (!consent) {
            // Small delay to prevent layout shift flash
            const timer = setTimeout(() => setIsVisible(true), 1000);
            return () => clearTimeout(timer);
        }
    }, []);

    const acceptCookies = () => {
        localStorage.setItem("cookie_consent", "true");
        setIsVisible(false);
    };

    const declineCookies = () => {
        localStorage.setItem("cookie_consent", "false");
        setIsVisible(false);
    };

    if (!isVisible) return null;

    return (
        <div className="fixed bottom-0 left-0 right-0 z-50 p-4 mx-auto max-w-7xl">
            <div className="bg-gray-900/95 backdrop-blur-md border border-gray-800 rounded-lg p-6 shadow-2xl flex flex-col sm:flex-row items-center justify-between gap-4">
                <div className="flex-1">
                    <h3 className="text-lg font-semibold text-white mb-2">We value your privacy</h3>
                    <p className="text-sm text-gray-300">
                        We use cookies to enhance your browsing experience, serve personalized content, and analyze our traffic.
                        By clicking &quot;Accept All&quot;, you consent to our use of cookies.
                        Read our <Link href="/legal/privacy-policy" className="text-indigo-400 hover:text-indigo-300 underline">Privacy Policy</Link> and <Link href="/legal/terms-of-service" className="text-indigo-400 hover:text-indigo-300 underline">Terms of Service</Link>.
                    </p>
                </div>
                <div className="flex items-center gap-3 w-full sm:w-auto">
                    <button
                        onClick={declineCookies}
                        className="flex-1 sm:flex-none px-4 py-2 text-sm font-medium text-gray-300 hover:text-white bg-transparent border border-gray-700 hover:border-gray-600 rounded-md transition-colors"
                    >
                        Decline
                    </button>
                    <button
                        onClick={acceptCookies}
                        className="flex-1 sm:flex-none px-4 py-2 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-500 rounded-md transition-colors shadow-lg shadow-indigo-500/20"
                    >
                        Accept All
                    </button>
                </div>
            </div>
        </div>
    );
}
