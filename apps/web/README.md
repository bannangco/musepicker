# MusePicker Web

Next.js App Router frontend for MusePicker.

## Implemented Baseline

- URL-driven filter state (`city`, `category`, `query`, `date`, `pax`, paging)
- React Query server-state for search and offer loading
- Figma-referenced customer pages:
  - `/`
  - `/city/[city]`
  - `/search`
  - `/category/[category]`
  - `/activity/[activityId]`
- List pages include client-side sort controls (`price low-high`, `price high-low`, `best discount`) over loaded page items.
- Activity detail includes grouped ticket offers, map/reviews/nearby placeholder sections, and nearby tickets strip.
- Backoffice overview page:
  - `/admin`
- Affiliate outbound tracking:
  - primary contract: `GET {API_BASE_URL}/api/affiliate/out/{offerId}?target=<affiliate-url>&platform=<platform-code>`
  - compatibility alias: `/out/[offerId]?target=<affiliate-url>&platform=<platform-code>`

## Run

```bash
cd apps/web
npm install
npm run dev
```

## Production Test Domain

- `NEXT_PUBLIC_SITE_URL=https://musepicker.shimyunbo.com`
- `NEXT_PUBLIC_API_BASE_URL=https://api.musepicker.shimyunbo.com`
- `API_BASE_URL=https://api.musepicker.shimyunbo.com`
