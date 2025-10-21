import type { NextConfig } from "next";
import path from "path";

const nextConfig: NextConfig = {
  output: 'standalone',
  outputFileTracingRoot: path.join(__dirname, '../../'),
  turbopack: {
    root: path.join(__dirname, '../../'),
  },
  images: {
    domains: ["lh3.googleusercontent.com", "avatars.githubusercontent.com"],
  },
  // Vercel will auto-detect this config
  // No custom rewrites needed for static export
};

export default nextConfig;
