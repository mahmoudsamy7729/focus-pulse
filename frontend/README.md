# FocusPulse Frontend

The Phase 3 dashboard runtime is a Next.js App Router application.

## Runtime

- `app/` owns route composition and providers.
- `features/analytics/` owns dashboard API calls, TanStack Query hooks, schemas, utilities, and feature components.
- `components/charts/` owns reusable chart components.
- `components/layout/` owns shared page layout shells.
- `lib/api/` owns the Axios client and standard API envelope types.

## Commands

```powershell
npm install
npm run lint
npm run test
npm run build
```

Set `NEXT_PUBLIC_API_BASE_URL` when the backend is not available at `http://localhost:8000/api/v1`.

## Phase 3 Notes

The dashboard is read-only. Server state is fetched through TanStack Query and is not copied into a global store. The dashboard route starts at `/dashboard`; `/` redirects there.
