function toStringValue(value) {
  if (Array.isArray(value)) {
    return value[0] ?? '';
  }
  return value ?? '';
}

function toInt(value, fallback) {
  const parsed = Number.parseInt(value, 10);
  return Number.isFinite(parsed) ? parsed : fallback;
}

export function normalizeSearchParams(searchParams = {}) {
  const city = toStringValue(searchParams.city).trim();
  const category = toStringValue(searchParams.category).trim();
  const query = toStringValue(searchParams.query).trim();
  const date = toStringValue(searchParams.date).trim();
  const pax = Math.max(1, toInt(toStringValue(searchParams.pax), 1));
  const page = Math.max(0, toInt(toStringValue(searchParams.page), 0));
  const size = Math.min(100, Math.max(1, toInt(toStringValue(searchParams.size), 20)));

  return {
    city,
    category,
    query,
    date,
    pax,
    page,
    size
  };
}

export function toQueryString(params) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value === undefined || value === null || value === '') {
      return;
    }
    query.set(key, String(value));
  });
  return query.toString();
}
