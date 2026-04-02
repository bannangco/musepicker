# MusePicker Web

Next.js App Router frontend for MusePicker.

## Implemented Baseline

- URL-driven filter state (`city`, `category`, `query`, `date`, `pax`, paging)
- React Query server-state for search and offer loading
- Search/list pages:
  - `/`
  - `/search`
  - `/city/[city]`
  - `/category/[category]`
  - `/activity/[activityId]`
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
