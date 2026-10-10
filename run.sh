#!/usr/bin/env bash
# PsycheDive - start the server
set -e
cd "$(dirname "$0")"
if [ ! -d .venv ]; then
  python3 -m venv .venv 2>/dev/null || true
fi
if [ -d .venv ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate 2>/dev/null || true
fi
pip install -q -r requirements.txt
[ -f .env ] || cp .env.example .env
python app.py
