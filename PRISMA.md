# Optional Prisma (Node) database

This repo is primarily Python, but it includes an **optional** Prisma setup for managing the same `workflows` + `ai_models` tables against a Postgres database (including Prisma Postgres).

## Safety / default behavior

- Prisma is **OFF by default** (`PRISMA_ENABLED=0`).
- Do **not** commit real database credentials to `.env`.

## Setup

1) Install Node deps (from repo root):

```bash
npm install
```

If you hit an `EPERM` error during install (some Windows environments block Prisma's install scripts), use:

```bash
npm install --ignore-scripts --cache .npm-cache --no-audit --no-fund
```

2) Put your real connection string(s) in environment variables (recommended) or an untracked local env file:

- `DATABASE_URL` (used by Prisma Migrate and the runtime adapter)
- `SHADOW_DATABASE_URL` (optional; used for `migrate dev` on some setups)
- `PRISMA_ENABLED=1` (only needed when running the example Node scripts)

Tip: you can put secrets in `.env.prisma` (gitignored) and run Prisma like:

```bash
DOTENV_CONFIG_PATH=.env.prisma npx prisma generate
```

3) Generate Prisma Client:

```bash
npx prisma generate
```

4) Create/apply the initial migration:

```bash
npx prisma migrate dev --name init
```

5) Quick sanity test (queries the `workflows` table):

```bash
PRISMA_ENABLED=1 node app/scripts/test-prisma.mjs
```

## Files

- `prisma/schema.prisma` – Prisma schema for `workflows` + `ai_models`
- `prisma.config.ts` – Prisma 7 config (datasource URLs live here)
- `app/db/prisma.js` – optional Prisma Client wrapper (uses `@prisma/adapter-pg`)
- `app/scripts/test-prisma.mjs` – small query script for verification
