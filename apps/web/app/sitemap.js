import { getRegionCities, getTrendingActivities } from '@/lib/api';

const BASE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://musepicker.shimyunbo.com';

export default async function sitemap() {
  const entries = [
    {
      url: `${BASE_URL}/`,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1
    },
    {
      url: `${BASE_URL}/search`,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 0.9
    }
  ];

  try {
    const [cities, trending] = await Promise.all([getRegionCities(), getTrendingActivities()]);
    for (const city of cities ?? []) {
      entries.push({
        url: `${BASE_URL}/city/${encodeURIComponent(city.city)}`,
        lastModified: new Date(),
        changeFrequency: 'daily',
        priority: 0.8
      });
    }
    for (const activity of trending ?? []) {
      entries.push({
        url: `${BASE_URL}/activity/${activity.id}`,
        lastModified: new Date(),
        changeFrequency: 'daily',
        priority: 0.8
      });
    }
  } catch {
    // Keep base entries if API is unavailable at build/render time.
  }

  return entries;
}
