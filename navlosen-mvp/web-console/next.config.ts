import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'standalone',
  experimental: {
    turbo: {
      root: process.cwd(),
    },
  },
};

export default nextConfig;
