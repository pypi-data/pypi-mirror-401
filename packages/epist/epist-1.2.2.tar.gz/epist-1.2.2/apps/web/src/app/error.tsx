'use client'

import { useEffect } from 'react'

export default function Error({
    error,
    reset,
}: {
    error: Error & { digest?: string }
    reset: () => void
}) {
    useEffect(() => {
        // Log the error to an error reporting service
        console.error('Global Error Boundary caught:', error)
    }, [error])

    return (
        <div className="flex min-h-screen flex-col items-center justify-center bg-black text-white px-4">
            <div className="max-w-md text-center space-y-6">
                <div className="space-y-2">
                    <h2 className="text-3xl font-bold tracking-tight text-red-500">Something went wrong!</h2>
                    <p className="text-gray-400">
                        We apologize for the inconvenience. An unexpected error has occurred.
                    </p>
                    {process.env.NODE_ENV === 'development' && (
                        <div className="mt-4 p-4 bg-gray-900 rounded text-left overflow-auto max-h-48">
                            <code className="text-xs text-red-300">
                                {error.message}
                            </code>
                        </div>
                    )}
                </div>
                <div className="flex gap-4 justify-center">
                    <button
                        onClick={
                            // Attempt to recover by trying to re-render the segment
                            () => reset()
                        }
                        className="rounded-full bg-white px-6 py-2 text-black font-medium hover:bg-gray-200 transition-colors"
                    >
                        Try again
                    </button>
                    <a
                        href="mailto:admin@epist.ai"
                        className="rounded-full border border-gray-600 px-6 py-2 text-gray-300 font-medium hover:bg-gray-800 transition-colors"
                    >
                        Contact Support
                    </a>
                </div>
            </div>
        </div>
    )
}
