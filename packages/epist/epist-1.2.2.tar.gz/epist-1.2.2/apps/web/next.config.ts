import { withSentryConfig } from "@sentry/nextjs";
import { createMDX } from 'fumadocs-mdx/next';
import type { NextConfig } from "next";

const nextConfig = {
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
} satisfies NextConfig;

const withMDX = createMDX();

export default withSentryConfig(withMDX(nextConfig), {
  silent: true,
  org: "epist",
  project: "epist-frontend",
});
