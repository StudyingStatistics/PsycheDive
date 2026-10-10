"""Minimal Tavily search wrapper (optional, used for extra web sources)."""
import requests

TIMEOUT = 45


def tavily_search(cfg, query, max_results=5):
    if not cfg.has_tavily():
        raise RuntimeError('TAVILY_API_KEY is not set in the environment')

    query = (query or '').strip()
    if not query:
        return {'results': []}

    try:
        limit = max(1, min(int(max_results or 5), 20))
    except (TypeError, ValueError):
        limit = 5

    payload = {
        'api_key': cfg.TAVILY_API_KEY,
        'query': query,
        'max_results': limit,
        'search_depth': 'basic',
    }
    resp = requests.post(cfg.TAVILY_BASE + '/search', json=payload, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()
