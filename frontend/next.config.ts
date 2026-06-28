import type { NextConfig } from "next";

const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'https://sukoon-backend-25172750096.us-central1.run.app';

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${backendUrl}/api/:path*`,
      },
    ]
  },
};

export default nextConfig;
