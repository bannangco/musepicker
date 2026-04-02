import { toQueryString } from './search-params';

const SERVER_DEFAULT = 'http://localhost:8080';

export function getBaseUrl() {
  if (typeof window === 'undefined') {
    return process.env.API_BASE_URL || process.env.NEXT_PUBLIC_API_BASE_URL || SERVER_DEFAULT;
  }
  return process.env.NEXT_PUBLIC_API_BASE_URL || SERVER_DEFAULT;
}

async function fetchJson(path, { params, cache = 'no-store', revalidate } = {}) {
  const baseUrl = getBaseUrl();
  const queryString = params ? toQueryString(params) : '';
  const endpoint = queryString ? `${path}?${queryString}` : path;
  const url = `${baseUrl}${endpoint}`;

  const fetchOptions = {
    headers: {
      Accept: 'application/json'
    },
    cache
  };

  if (typeof revalidate === 'number') {
    fetchOptions.next = { revalidate };
  }

  const response = await fetch(url, fetchOptions);
  if (!response.ok) {
    const body = await response.text();
    throw new Error(`API request failed (${response.status}): ${body || response.statusText}`);
  }

  return response.json();
}

export async function getRegionCities(options = {}) {
  return fetchJson('/api/regions/cities', options);
}

export async function getTrendingActivities(options = {}) {
  return fetchJson('/api/activities/trending', options);
}

export async function searchActivities(params, options = {}) {
  return fetchJson('/api/activities/search', { ...options, params });
}

export async function getActivity(activityId, options = {}) {
  return fetchJson(`/api/activities/${activityId}`, options);
}

export async function getActivityOffers(activityId, params, options = {}) {
  return fetchJson(`/api/activities/${activityId}/offers`, { ...options, params });
}

export async function getPlatforms(options = {}) {
  return fetchJson('/api/platforms', options);
}

export function buildAffiliateOutboundUrl(offer) {
  const params = new URLSearchParams({
    target: offer.affiliateUrl,
    platform: offer.platform.code
  });
  return `${getBaseUrl()}/api/affiliate/out/${offer.id}?${params.toString()}`;
}

export async function getSourceHealth(options = {}) {
  return fetchJson('/api/admin/sources/health', options);
}

export async function getMappingReviewQueue(options = {}) {
  return fetchJson('/api/admin/mappings/review', options);
}

export async function applyMappingOverride(payload, options = {}) {
  const baseUrl = getBaseUrl();
  const url = `${baseUrl}/api/admin/mappings/override`;
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload),
    cache: options.cache || 'no-store'
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`API request failed (${response.status}): ${body || response.statusText}`);
  }
  return response.json();
}

export async function getOfferAnomalies(options = {}) {
  return fetchJson('/api/admin/offers/anomalies', options);
}

export async function getMualbaActivities(options = {}) {
  return fetchJson('/api/mualba/activities', options);
}
