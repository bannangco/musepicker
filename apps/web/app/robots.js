const BASE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://www.musepicker.com';

export default function robots() {
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: '/admin'
      }
    ],
    sitemap: `${BASE_URL}/sitemap.xml`
  };
}
