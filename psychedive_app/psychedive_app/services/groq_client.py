"""Minimal Groq pass-through (models + chat completions, streaming aware)."""
from typing import Iterator

import requests

TIMEOUT_SHORT = 30
TIMEOUT_LONG = 120
TIMEOUT_STREAM = 300


def _headers(cfg):
    return {
        'Authorization': 'Bearer ' + cfg.GROQ_API_KEY,
        'Content-Type': 'application/json',
    }


def groq_models(cfg):
    if not cfg.has_groq():
        raise RuntimeError('GROQ_API_KEY is not set in the environment')
    resp = requests.get(cfg.GROQ_BASE + '/models', headers=_headers(cfg), timeout=TIMEOUT_SHORT)
    resp.raise_for_status()
    return resp.json()


def groq_chat(cfg, body):
    if not cfg.has_groq():
        raise RuntimeError('GROQ_API_KEY is not set in the environment')
    payload = {k: v for k, v in dict(body).items() if k != 'stream'}
    resp = requests.post(
        cfg.GROQ_BASE + '/chat/completions',
        headers=_headers(cfg), json=payload, timeout=TIMEOUT_LONG,
    )
    resp.raise_for_status()
    return resp.json()


def groq_chat_stream(cfg, body) -> Iterator[bytes]:
    """Yield raw SSE bytes straight through, so the browser sees the live text."""
    if not cfg.has_groq():
        raise RuntimeError('GROQ_API_KEY is not set in the environment')
    payload = dict(body)
    payload['stream'] = True

    resp = requests.post(
        cfg.GROQ_BASE + '/chat/completions',
        headers=_headers(cfg), json=payload, stream=True, timeout=TIMEOUT_STREAM,
    )
    resp.raise_for_status()
    try:
        for chunk in resp.iter_content(chunk_size=None):
            if chunk:
                yield chunk
    finally:
        resp.close()
