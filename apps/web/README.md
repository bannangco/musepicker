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
- Affiliate outbound tracking redirect:
  - `/out/[offerId]?target=<affiliate-url>&platform=<platform-code>`

## Run

```bash
cd apps/web
npm install
npm run dev
```
