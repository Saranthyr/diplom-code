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
      {
        source: "/user",
        destination: "http://api:5000/user/",
      },
      {
        source: "/search/posts",
        destination:
          "http://api:5000/search/posts?order_by=rating&rating=0&way=desc&page=1&draft=false&archived=false",
      },
      {
        source: "/posts/:id",
        destination: "http://api:5000/posts/:id",
      },
      {
        source: "/posts/:id/comments",
        destination: "http://api:5000/posts/:id/comments",
      },
      {
        source: "/auth/register",
        destination: "http://api:5000/auth/register",
      },
      {
        source: "/auth/activate",
        destination: "http://api:5000/auth/activate",
      },
    ];
  },
};

export default nextConfig;
