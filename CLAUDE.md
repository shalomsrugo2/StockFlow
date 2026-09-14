@AGENTS.md

## Learning priority for this project (from the user)

The user's top goal right now is to genuinely understand StockFlow well enough to explain it confidently in a job interview — not to memorize every generated line. The #1 priority, above shipping new features, is teaching the **mental model** of Next.js as things get built:

1. How the App Router works: folders = routes, `page.tsx` renders a route, `layout.tsx` wraps shared UI.
2. Server Components vs. Client Components: server runs by default, `"use client"` opts into the browser — and why that split exists.
3. How data actually moves: Server Component data fetching, route handlers/API routes, and Server Actions — traced end-to-end from a UI click to the server and back.

When implementing or explaining anything in this repo, default to teaching, not just doing:
- Explain new Next.js concepts in plain, beginner-friendly language — as if talking to a smart teenager who has never seen Next.js before. No jargon without a plain-English definition attached.
- Prefer short, concrete explanations tied to the actual file/feature just built over abstract theory.
- After implementing a feature, proactively summarize *why* it's structured the way it is (why this is a Server vs. Client Component, why this data fetch lives here, etc.) rather than waiting to be asked.
- It's fine to slow down and teach before moving to the next task — thoroughness on the mental model matters more than speed right now.
