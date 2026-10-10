# PsycheDive

A quiet corner for the questions that keep circling in your head. Type a feeling,
a situation, or a concept, and the app reads real psychology research
(Europe PMC + OpenAlex) and writes an evidence-checked explanation.

This repository is the original single-file app, **plus an accessibility layer**
and a small optional server so the API keys can live in `.env`.

---

## What was added

| # | Feature | Where it lives |
|---|---------|----------------|
| 1 | **Home button** — jump back to the desk from anywhere | floating 🏠 button, top-left · also in Settings |
| 2 | **Text size** — bigger / smaller, remembered on the device | `A− 100% A+` control, top-left · also in Settings |
| 3 | **Concept bookmarks** — save the ideas you like and reopen them | ☆ Bookmark in every read · 🔖 panel · homepage section |
| 4 | **No-repeat game questions** — cases never come back until the set runs out | automatic in all case/scenario games |
| 5 | **Groq + Tavily keys** — from the browser *or* from `.env` | Settings panel · `app.py` backend |

Nothing in the original app was removed or rewritten. The new code only adds
UI, wraps a few functions to *observe* them, and keeps its own browser storage
keys: `rh_fs` (text size), `rh_bm` (bookmarks), `rh_seen` (games),
`rh_tkey` (Tavily key).

---

## Prerequisites

* Python 3.9 or newer (`python --version`)
* A free **Groq** API key (required for AI explanations): https://console.groq.com/keys
* A **Tavily** API key (optional, adds web search): https://app.tavily.com/home
* An internet connection (research sources: Europe PMC, OpenAlex; plus Groq)

## Run it locally

### Option A: with the Flask server (recommended; key stays in `.env`)

```bash
git clone https://github.com/StudyingStatistics/PsycheDive.git
cd PsycheDive

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env               # Windows: copy .env.example .env
# open .env in a text editor and paste your key after GROQ_API_KEY=
# (add TAVILY_API_KEY= too if you have one)

python app.py                      # then open http://127.0.0.1:5000
```

`run.sh` (macOS/Linux) and `run.bat` (Windows) do the same steps in one go.
Edit `.env` afterwards to add your key, then restart.

When the page is served by `app.py` it detects the backend and sends model calls
through `/api/groq`, so the key is never placed in the HTML or the browser.

### Option B: just the HTML file (no server)

Open `static/psychedive.html` in a browser and paste your Groq key in
**Settings -> Groq API key**. The key is stored only in that browser's local
storage on your machine. It is not part of this repository.

## Supplying your own API key without committing it

* **Do not edit `.env.example`.** It is a template with empty values and is the
  only env file tracked by Git.
* Put your real key in `.env` (copied from the template). `.gitignore` excludes
  `.env`, `.env.*` (except `.env.example`), and other local secret files.
* Or skip `.env` and paste the key in the app's Settings panel (Option B).
* Before pushing, you can confirm nothing secret is staged: `git status` should
  not list `.env`.
* Leave unused keys **empty** in `.env`. Do not put placeholder text such as
  `your_key_here`: any non-empty value is treated as a real key.

## Configuration reference (`.env`)

| Variable | Default | Meaning |
|----------|---------|---------|
| `GROQ_API_KEY` | empty | Groq key (server-side) |
| `TAVILY_API_KEY` | empty | Optional Tavily key |
| `GROQ_MODELS` | see `.env.example` | Model preference order |
| `HOST` / `PORT` | `127.0.0.1` / `5000` | Where the server listens |
| `FLASK_DEBUG` | `0` | Keep `0`; debug mode exposes a code console |
| `CORS` | `0` in `.env.example` | Keep `0` for local use |
| `PUBLIC_MODE` | `0` | `1` for internet deployment (browser can never send its own key) |
| `RATE_LIMIT_PER_MIN`, `MAX_TOKENS_CAP`, `MAX_BODY_BYTES`, `ALLOWED_ORIGINS` | see `.env.example` | Request limits |

---

## Layout

```
psychedive_app/
├─ app.py                      entry point (Flask)
├─ config.py                   reads .env, exposes the keys
├─ requirements.txt
├─ .env.example                copy to .env and fill in
├─ .gitignore
├─ run.sh / run.bat            one-click launchers
├─ psychedive_app/
│  ├─ __init__.py              application factory
│  ├─ routes.py                /api/config, /api/groq/*, /api/tavily/search
│  ├─ utils.py
│  └─ services/
│     ├─ groq_client.py        chat + streaming pass-through
│     └─ tavily_client.py      optional web search
└─ static/
   └─ psychedive.html          the whole app (single file)
```

## API

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/config` | which server keys exist (`groq`, `tavily`), model list |
| GET | `/api/groq/models` | Groq model list |
| POST | `/api/groq/chat/completions` | Groq chat (`"stream": true` supported) |
| POST | `/api/tavily/search` | Tavily search `{ "query": "...", "max_results": 5 }` |
| GET | `/healthz` | liveness check |

## Notes

* Educational psychology only — not a diagnostic or therapy tool.
* Keys are read from the environment; they are never written into the HTML,
  the repository, or the browser when the backend is used.
* The games are illustrations of how psychological reasoning works. A single
  behaviour never identifies a person.


## v2
See CHANGES.md. For a public deployment set `PUBLIC_MODE=1` in `.env` (keys then stay on the server only).
