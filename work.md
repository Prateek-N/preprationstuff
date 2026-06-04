# Work Log (Agent Context)

This file captures what has been done so far so another agent can pick up with full context.

## Repo

- GitHub: https://github.com/Prateek-N/preprationstuff
- Branch: `main`
- Latest commit: `8e243e9` — `feat: add Nextra docs site for markdown`

## Goal

- Create a docs-style site that can host multiple Markdown files, with navigation/TOC/search, deployable on Vercel.

## What Was Built

- Next.js + Nextra docs site.
- Docs are served under `/docs`.
- Root `/` redirects to `/docs`.
- Search is enabled via Pagefind (runs in `postbuild` and outputs to `public/_pagefind`).

## Key Paths

- App layout/theme: [app/layout.jsx](file:///f:/rivian%20vaishnavi/preprationstuff/app/layout.jsx)
- Root redirect: [app/page.jsx](file:///f:/rivian%20vaishnavi/preprationstuff/app/page.jsx)
- Docs route handler: [app/docs/[[...mdxPath]]/page.jsx](file:///f:/rivian%20vaishnavi/preprationstuff/app/docs/%5B%5B...mdxPath%5D%5D/page.jsx)
- Nextra config: [next.config.mjs](file:///f:/rivian%20vaishnavi/preprationstuff/next.config.mjs)
- MDX components hook: [mdx-components.js](file:///f:/rivian%20vaishnavi/preprationstuff/mdx-components.js)
- Docs content folder: [content/](file:///f:/rivian%20vaishnavi/preprationstuff/content)
  - Sidebar order/titles: [content/_meta.js](file:///f:/rivian%20vaishnavi/preprationstuff/content/_meta.js)
  - Docs home: [content/index.mdx](file:///f:/rivian%20vaishnavi/preprationstuff/content/index.mdx)
  - First doc: [content/rivian-vw-ota-interview-prep.md](file:///f:/rivian%20vaishnavi/preprationstuff/content/rivian-vw-ota-interview-prep.md)

## Content Migration

- The original markdown file `Rivian_VW_OTA_Interview_Prep_Guide.md` (from local workspace root) was copied into the repo as:
  - `content/rivian-vw-ota-interview-prep.md`

## Commands Used (Local)

- Install deps:
  - `npm install`
- Run dev:
  - `npm run dev`
  - Expected URL: http://localhost:3000/docs
- Production build:
  - `npm run build`
  - Runs `next build` then `pagefind` as `postbuild`

## Vercel Deploy Notes

- Framework: Next.js
- Default commands work:
  - Build: `npm run build`
  - Output: Next.js app (no static export)
- Search index is generated during build into `public/_pagefind`.

## Adding More Markdown Files

1. Add file:
   - `content/<slug>.md` (or `.mdx`)
2. Add sidebar entry:
   - Update `content/_meta.js` with:
     - `<slug>: 'Title'`
3. Link will be:
   - `/docs/<slug>`

## Known Gotchas / Decisions

- Next.js version was adjusted to avoid Turbopack-related runtime/build issues seen with Next 16 in this setup.
- Current versions are pinned in [package.json](file:///f:/rivian%20vaishnavi/preprationstuff/package.json) and `npm run build` succeeds.

