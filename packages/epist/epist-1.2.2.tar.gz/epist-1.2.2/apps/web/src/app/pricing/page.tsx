'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Check, X, Shield, Zap, Headphones, Globe } from 'lucide-react';
import { api } from '@/lib/api';
import { auth } from '@/lib/firebase';

const tiers = [
    {
        name: 'Sandbox',
        id: 'free',
        price: 0,
        description: 'For experimentation and personal projects.',
        features: [
            '5 hours transcription / month',
            'Basic Vector Search',
            'Community Support',
            'Standard Processing',
            '1 Team Member'
        ],
        notIncluded: [
            'API Access',
            'Hybrid Search (Reranking)',
            'Priority Support'
        ],
        cta: 'Get Started',
        mostPopular: false,
    },
    {
        name: 'Starter',
        id: 'starter',
        price: 19,
        description: 'For individuals building serious applications.',
        features: [
            '20 hours transcription / month',
            'API Access',
            'Basic Vector Search',
            'Email Support',
            'Standard Processing',
            'Up to 3 Team Members'
        ],
        notIncluded: [
            'Hybrid Search (Reranking)',
            'Priority Queue'
        ],
        cta: 'Start Free Trial',
        mostPopular: false,
    },
    {
        name: 'Pro',
        id: 'pro',
        price: 49,
        description: 'For teams and production-grade applications.',
        features: [
            '100 hours transcription / month',
            'API Access (Higher Limits)',
            'Hybrid Search + Reranking',
            'Priority Queue',
            'Priority Email & Chat Support',
            'Unlimited Team Members'
        ],
        notIncluded: [],
        cta: 'Upgrade to Pro',
        mostPopular: true,
    },
];

const faqs = [
    {
        question: "Can I cancel at any time?",
        answer: "Yes, you can cancel your subscription at any time. You will continue to have access to the features you paid for until the end of your billing cycle."
    },
    {
        question: "How does the transcription limit work?",
        answer: "Limits are reset every month. If you exceed your limit, you can upgrade to a higher tier or wait for the next billing cycle."
    },
    {
        question: "What happens to my data if I downgrade?",
        answer: "Your data is kept safe. However, you may lose access to premium features like advanced search indices or historical logs dependent on the higher tier."
    },
    {
        question: "Do you offer enterprise plans?",
        answer: "Yes! Contact us for custom limits, dedicated support, and on-premise deployment options."
    }
];

export default function PricingPage() {
    const router = useRouter();
    const [loading, setLoading] = useState<string | null>(null);
    const [billingInterval, setBillingInterval] = useState<'month' | 'year'>('month');

    const handleUpgrade = async (tierId: string) => {
        if (!auth.currentUser) {
            router.push('/login?redirect=/pricing');
            return;
        }

        if (tierId === 'free') {
            // Logic to downgrade or just redirect to dashboard
            router.push('/dashboard');
            return;
        }

        try {
            setLoading(tierId);
            const { url } = await api.createCheckoutSession(tierId);
            window.location.href = url;
        } catch (error) {
            console.error('Failed to start checkout:', error);
            // Using a simple alert for now, but a toast would be better
            alert('Failed to start checkout. Please try again or contact support.');
        } finally {
            setLoading(null);
        }
    };

    return (
        <div className="bg-slate-950 min-h-screen font-sans selection:bg-indigo-500/30">
            {/* Header / Hero */}
            <div className="relative pt-24 pb-12 sm:pt-32 sm:pb-16 overflow-hidden">
                <div className="absolute top-0 left-1/2 w-full -translate-x-1/2 -translate-y-1/2 pointer-events-none">
                    <div className="w-[800px] h-[800px] bg-indigo-500/20 rounded-full blur-[120px] opacity-30"></div>
                </div>

                <div className="mx-auto max-w-7xl px-6 lg:px-8 relative z-10">
                    <div className="mx-auto max-w-4xl text-center">
                        <h2 className="text-base font-semibold leading-7 text-indigo-400 uppercase tracking-widest">Pricing</h2>
                        <p className="mt-4 text-5xl font-bold tracking-tight text-white sm:text-6xl">
                            Scalable plans for every stage
                        </p>
                        <p className="mt-6 text-xl leading-8 text-slate-400">
                            Unlock the full potential of your audio data with our flexible pricing tiers.
                        </p>
                    </div>

                    {/* Toggle */}
                    <div className="mt-10 flex justify-center">
                        <div className="bg-slate-900/50 p-1 rounded-xl border border-white/5 flex items-center relative">
                            <button
                                onClick={() => setBillingInterval('month')}
                                className={`px-6 py-2 rounded-lg text-sm font-medium transition-all ${billingInterval === 'month' ? 'bg-indigo-600 text-white shadow-lg' : 'text-slate-400 hover:text-white'}`}
                            >
                                Monthly
                            </button>
                            <button
                                onClick={() => setBillingInterval('year')}
                                className={`px-6 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2 ${billingInterval === 'year' ? 'bg-indigo-600 text-white shadow-lg' : 'text-slate-400 hover:text-white'}`}
                            >
                                Yearly <span className="text-[10px] bg-emerald-500/20 text-emerald-400 px-1.5 py-0.5 rounded-full border border-emerald-500/30">-20%</span>
                            </button>
                        </div>
                    </div>


                </div>
            </div>

            {/* Pricing Cards */}
            <div className="mx-auto max-w-7xl px-6 lg:px-8 pb-24">
                <div className="isolate mx-auto grid max-w-md grid-cols-1 gap-8 lg:mx-0 lg:max-w-none lg:grid-cols-2">
                    {tiers.map((tier) => (
                        <div
                            key={tier.id}
                            className={`relative flex flex-col justify-between rounded-3xl p-8 xl:p-10 transition-all duration-300 ${tier.mostPopular
                                ? 'bg-slate-900/80 ring-2 ring-indigo-500 shadow-2xl shadow-indigo-500/10 scale-105 z-10'
                                : 'bg-white/5 ring-1 ring-white/10 hover:bg-white/10'
                                }`}
                        >
                            {tier.mostPopular && (
                                <div className="absolute top-0 right-0 -translate-y-1/2 translate-x-1/4 sm:translate-x-0 sm:right-8">
                                    <span className="inline-flex items-center rounded-full bg-indigo-500 px-4 py-1 text-sm font-semibold text-white shadow-lg">
                                        Most Popular
                                    </span>
                                </div>
                            )}

                            <div>
                                <div className="flex items-center justify-between gap-x-4">
                                    <h3 id={tier.id} className="text-xl font-bold leading-8 text-white">
                                        {tier.name}
                                    </h3>
                                </div>
                                <p className="mt-4 text-sm leading-6 text-slate-400">{tier.description}</p>
                                <p className="mt-6 flex items-baseline gap-x-1">
                                    <span className="text-5xl font-bold tracking-tight text-white">
                                        {typeof tier.price === 'number'
                                            ? `$${billingInterval === 'year' ? Math.floor(tier.price * 0.8) : tier.price}`
                                            : tier.price}
                                    </span>
                                    {typeof tier.price === 'number' && (
                                        <span className="text-sm font-semibold leading-6 text-slate-400">/{billingInterval === 'year' ? 'month, billed yearly' : 'month'}</span>
                                    )}
                                </p>
                                <ul role="list" className="mt-8 space-y-3 text-sm leading-6 text-slate-300">
                                    {tier.features.map((feature) => (
                                        <li key={feature} className="flex gap-x-3">
                                            <Check className="h-6 w-5 flex-none text-indigo-400" aria-hidden="true" />
                                            {feature}
                                        </li>
                                    ))}
                                    {tier.notIncluded?.map((feature) => (
                                        <li key={feature} className="flex gap-x-3 text-slate-600">
                                            <X className="h-6 w-5 flex-none" aria-hidden="true" />
                                            {feature}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                            <button
                                onClick={() => {
                                    if (tier.id === 'enterprise') {
                                        window.location.href = 'mailto:sales@epist.ai';
                                        return;
                                    }
                                    handleUpgrade(tier.id);
                                }}
                                disabled={loading !== null || (tier.id === 'free' && false)}
                                aria-describedby={tier.id}
                                className={`mt-8 block w-full rounded-xl px-3 py-3 text-center text-sm font-bold leading-6 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 transition-all ${tier.mostPopular
                                    ? 'bg-indigo-600 text-white hover:bg-indigo-500 shadow-lg shadow-indigo-500/25'
                                    : 'bg-white/10 text-white hover:bg-white/20'
                                    } disabled:opacity-50 disabled:cursor-not-allowed`}
                            >
                                {loading === tier.id ? (
                                    <span className="flex items-center justify-center gap-2">
                                        <svg className="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                        </svg>
                                        Processing...
                                    </span>
                                ) : tier.cta}
                            </button>
                        </div>
                    ))}
                </div>
            </div>

            {/* Features Grid / Trust */}
            <div className="bg-slate-900 py-24 sm:py-32">
                <div className="mx-auto max-w-7xl px-6 lg:px-8">
                    <div className="mx-auto max-w-2xl lg:text-center">
                        <p className="mt-2 text-3xl font-bold tracking-tight text-white sm:text-4xl">Everything you need to build intelligent audio apps</p>
                    </div>
                    <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none">
                        <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-16 lg:max-w-none lg:grid-cols-3">
                            <div className="flex flex-col">
                                <dt className="flex items-center gap-x-3 text-base font-semibold leading-7 text-white">
                                    <Shield className="h-5 w-5 flex-none text-indigo-400" aria-hidden="true" />
                                    Enterprise Grade Security
                                </dt>
                                <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-slate-400">
                                    <p className="flex-auto">We use state-of-the-art encryption at rest and in transit. Your data is isolated and secure.</p>
                                </dd>
                            </div>
                            <div className="flex flex-col">
                                <dt className="flex items-center gap-x-3 text-base font-semibold leading-7 text-white">
                                    <Zap className="h-5 w-5 flex-none text-indigo-400" aria-hidden="true" />
                                    Lightning Fast Processing
                                </dt>
                                <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-slate-400">
                                    <p className="flex-auto">Our optimized GPU clusters ensure your audio is transcribed and indexed in seconds, not minutes.</p>
                                </dd>
                            </div>
                            <div className="flex flex-col">
                                <dt className="flex items-center gap-x-3 text-base font-semibold leading-7 text-white">
                                    <Globe className="h-5 w-5 flex-none text-indigo-400" aria-hidden="true" />
                                    Global Infrastructure
                                </dt>
                                <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-slate-400">
                                    <p className="flex-auto">Deployed on Google Cloud Platform with multi-region redundancy for 99.9% uptime.</p>
                                </dd>
                            </div>
                        </dl>
                    </div>
                </div>
            </div>

            {/* FAQ */}
            <div className="mx-auto max-w-7xl px-6 lg:px-8 py-24 sm:py-32">
                <div className="mx-auto max-w-4xl divide-y divide-white/10">
                    <h2 className="text-2xl font-bold leading-10 tracking-tight text-white">Frequently asked questions</h2>
                    <dl className="mt-10 space-y-6 divide-y divide-white/10">
                        {faqs.map((faq) => (
                            <div key={faq.question} className="pt-6">
                                <dt>
                                    <span className="text-base font-semibold leading-7 text-white">{faq.question}</span>
                                </dt>
                                <dd className="mt-2 text-base leading-7 text-slate-400">{faq.answer}</dd>
                            </div>
                        ))}
                    </dl>
                </div>
            </div>
        </div>
    );
}
