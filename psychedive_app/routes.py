"""HTTP routes: config + thin proxies for Groq and Tavily.

The browser never sees an API key when the app runs through this server.
"""
from flask import Blueprint, Response, current_app, jsonify, request, stream_with_context

from .services.groq_client import groq_chat, groq_chat_stream, groq_models
from .services.tavily_client import tavily_search

import time
from collections import defaultdict, deque

bp = Blueprint('api', __name__, url_prefix='/api')
_HITS = defaultdict(deque)


@bp.before_request
def _guard():
    """Per-IP rate limit and request size cap for every /api call."""
    cfg = _cfg()
    if request.method == 'OPTIONS':
        return None
    if (request.content_length or 0) > cfg.MAX_BODY_BYTES:
        return jsonify(ok=False, error='request too large'), 413
    now, q = time.time(), _HITS[request.remote_addr or '?']
    while q and now - q[0] > 60:
        q.popleft()
    if len(q) >= cfg.RATE_LIMIT_PER_MIN and request.path != '/api/config':
        return jsonify(ok=False, error='rate limit reached, try again in a minute'), 429
    q.append(now)
    return None


def _cfg():
    return current_app.config['PDA']


@bp.get('/config')
def config():
    """Tells the front end which server-side keys are available."""
    return jsonify(_cfg().as_public_dict())


@bp.get('/groq/models')
def models():
    try:
        return jsonify(groq_models(_cfg()))
    except Exception as exc:  # pragma: no cover - network dependent
        return jsonify(ok=False, error=str(exc)), 502


@bp.post('/groq/chat/completions')
def chat_completions():
    body = request.get_json(force=True, silent=True) or {}
    cfg = _cfg()
    if not isinstance(body.get('messages'), list) or not body.get('model'):
        return jsonify(ok=False, error='model and messages are required'), 400
    if cfg.PUBLIC_MODE and cfg.DEFAULT_MODELS and body['model'] not in cfg.DEFAULT_MODELS:
        return jsonify(ok=False, error='model not allowed'), 400
    body = {k: v for k, v in body.items() if k in {'model', 'messages', 'temperature', 'max_tokens', 'stream', 'response_format', 'reasoning_effort', 'top_p'}}
    if 'max_tokens' in body:
        body['max_tokens'] = min(int(body['max_tokens'] or 0) or 1000, cfg.MAX_TOKENS_CAP)
    if body.get('stream'):
        try:
            iterator = groq_chat_stream(_cfg(), body)
        except Exception as exc:  # pragma: no cover
            return jsonify(ok=False, error=str(exc)), 502
        return Response(
            stream_with_context(iterator),
            mimetype='text/event-stream',
            headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'},
        )
    try:
        return jsonify(groq_chat(_cfg(), body))
    except Exception as exc:  # pragma: no cover
        return jsonify(ok=False, error=str(exc)), 502


@bp.post('/tavily/search')
def tavily():
    body = request.get_json(force=True, silent=True) or {}
    try:
        return jsonify(tavily_search(_cfg(), body.get('query', ''), body.get('max_results', 5)))
    except Exception as exc:  # pragma: no cover
        return jsonify(ok=False, error=str(exc)), 502
