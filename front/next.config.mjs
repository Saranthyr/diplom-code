/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: "/auth/login",
        destination: "http://api:5000/auth/login",
      },
      {
        source: "/auth/register",
        destination: "http://api:5000/auth/register",
      },
      {
        source: "/auth/refresh",
        destination: "http://api:5000/auth/refresh",
      },
      {
        source: "/posts/create",
        destination: "http://api:5000/posts/create",
      },
      {
        source: "/regions",
        destination: "http://api:5000/regions",
      },
      {
        source: "/tourism",
        destination: "http://api:5000/tourism",
      },
    ];
  },
};

export default nextConfig;
