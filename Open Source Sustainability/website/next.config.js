/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['avatars.githubusercontent.com', 'user-images.githubusercontent.com'],
  },
}

module.exports = nextConfig
