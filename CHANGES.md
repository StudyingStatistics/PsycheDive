# PsycheDive v2 — what changed against the 20-point checklist

Status key: NEW = added now · FIXED = existed but was broken/incomplete · OK = already worked, checked, left alone.

| # | Item | Status | Notes |
|---|------|--------|-------|
| 1 | Claim verification | NEW | Every claim must carry an exact quote copied from its source. Checked: quote exists in the source; claim words match the quote; figures, names and populations appear in it; absolutes ("always", "proves") not stronger than the source; causal claim from correlational evidence is rejected. Passage is stored and shown. Old articles keep their old numbers-only check and say so. |
| 2 | Evidence vs model knowledge | NEW | Follow-up answers return `from_research` (cited [n]) and `from_model` (no citations) separately and are shown in two labelled boxes. Follow-ups still search again when evidence is thin. |
| 3 | Secure API | NEW | One `callAI()` gateway for all Groq calls. Server: per-IP rate limit, request-size cap, model allowlist, token cap, no CORS in `PUBLIC_MODE=1`. In public mode the browser deletes any stored key and refuses to take one. |
| 4 | Genuine agent loop | NEW | Phases are now Understand · Search · Compare · Verify · Explain · Discover and are driven by real steps. Each article shows "N sources explored · N claims verified · N new trails discovered" computed from the saved data. |
| 5 | Concept map | FIXED/NEW | Wheel-zoom toward cursor, drag-pan, +/−/reset already worked. Added: click selects (with Open / Zoom here / Bookmark / Clear panel), Tab to nodes, Enter selects, arrows pan, +/−/0 zoom/reset, Esc clears, double-click opens. |
| 6 | Home button | OK + NEW | Floating Home worked. Added a Home link inside the Explain-My-Brain drawer, which covered it. |
| 7 | Bookmarks | FIXED/NEW | Opening a bookmark now opens the saved article directly (it used to re-run the research). ★ shows on the home "continue" list and on map nodes. |
| 8 | Calendar → Day summary | NEW | Calendar tab shows "Today's exploration" for any day with recorded activity (concepts, depth, questions, topics, trails, bookmarks, reflections) and a Generate Day Summary button. The summary is composed from the logs only; the AI is not involved. Also fixed: the calendar/Play tabs were bound to the unwrapped functions. |
| 9 | Accessibility | NEW | Reading width (narrow/normal/wide), focus mode, listen-to-article with speed, live-region announcements for progress and new reads, map keyboard support. Text size was already persistent. |
| 10 | Homepage | NEW | Title, one-line tagline, Explore → Situation → Go deeper → Continue your trail. Long explanations moved to "How it works". Go deeper opens the latest read and its deep-report button (that report had no button before). |
| 11 | Cloudflare beacon | NEW | Only one existed (not a duplicate); removed because it is an analytics call that contradicts "stays on your device". |
| 12 | Centralise API logic | NEW | `callAI`, `getJSON` (timeout + retry), one `extractClaims` used by both the read and the deep report. |
| 13 | Failure handling | NEW | Planner failure falls back to standard queries; a failed claim batch is skipped; unreadable AI JSON is repaired before failing; source failures are logged and shown as "Partial research". |
| 14 | Citations stay attached | NEW | Each [n] is checked against the clause it supports; moved to a better source if one fits, otherwise removed. Count shown. |
| 15 | Explicit uncertainty | NEW | "Evidence is limited", "Research is mixed", "correlation, not causation", "N claims could not be verified". |
| 16 | PDF export | NEW | Title header, no controls, page numbers, avoid-break rules, URLs printed after source links. |
| 17-20 | QA | PARTIAL | See the report in the chat. |

Also fixed: choosing a depth crashed the page (`pickDepth` stored `{article}` instead of the article).

---
# v3 — restoring the original PsycheDive feel

Audit against your original `psychedive5.html`: all 515 functions, all 31 `@keyframes` animations and all 143 CSS classes are present. The only thing lost was the About page on the left.

- **About page restored** on the left page (Welcome in / What you can do here / Why you can trust it / Where it leads), with your original wording and wipe-in animation, plus a new "What is inside" section and a "Who made this" credit: original idea by Vrinda Kukreja, code by Claude.
- **The four steps** (Explore, Situation, Go deeper, Continue your trail) moved to the right page, under the sticky notes ("Where to begin").
- **Opening book animation** now plays on every visit (before, only once per browser tab, so a refresh showed nothing). Skip button unchanged.
- **Reduced-motion devices:** if your computer is set to reduce motion (Windows "Show animations" off, battery saver), the intro and every animation pause, exactly as before. The home page now says so and offers "Play them anyway". Settings has "Always play animations", "Skip the opening animation" and "Replay the opening".
- Fixed: with Quiet background on, the home page used to wait 7 seconds for an intro that never played.
