import Link from 'next/link'

export default function NotFound() {
    return (
        <div className="flex min-h-screen flex-col items-center justify-center bg-black text-white px-4">
            <div className="max-w-md text-center space-y-6">
                <div className="space-y-2">
                    <h1 className="text-6xl font-bold tracking-tight bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent">
                        404
                    </h1>
                    <h2 className="text-2xl font-semibold">Page Not Found</h2>
                    <p className="text-gray-400">
                        The page you are looking for does not exist or has been moved.
                    </p>
                </div>
                <div className="flex justify-center">
                    <Link
                        href="/dashboard"
                        className="rounded-full bg-white px-8 py-3 text-black font-medium hover:bg-gray-200 transition-colors"
                    >
                        Return Home
                    </Link>
                </div>
            </div>
        </div>
    )
}
