import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
    // Clone the request headers and add nonces if we use Content-Security-Policy later
    // For now, we mainly focus on response headers

    const response = NextResponse.next({
        request: {
            headers: new Headers(request.headers),
        },
    })

    // Security Headers
    // Prevent clickjacking
    response.headers.set('X-Frame-Options', 'DENY')

    // Prevent MIME sniffing
    response.headers.set('X-Content-Type-Options', 'nosniff')

    // Control referrer information
    response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin')

    // HSTS (HTTP Strict Transport Security)
    // Max-age: 1 year, include subdomains, preload
    if (process.env.NODE_ENV === 'production') {
        response.headers.set(
            'Strict-Transport-Security',
            'max-age=31536000; includeSubDomains; preload'
        )
    }

    // Permissions Policy (Optional, restricts hardware access)
    response.headers.set(
        'Permissions-Policy',
        'camera=(), microphone=(), geolocation=()'
    )

    return response
}

export const config = {
    matcher: [
        /*
         * Match all request paths except for the ones starting with:
         * - api (API routes)
         * - _next/static (static files)
         * - _next/image (image optimization files)
         * - favicon.ico (favicon file)
         */
        '/((?!api|_next/static|_next/image|favicon.ico).*)',
    ],
}
