"""Central configuration for PsycheDive.

Keys are read from the environment (a local .env file is loaded automatically
when python-dotenv is installed). No key is ever hard-coded here.
"""
import os
from pathlib import Path

try:  # optional dependency
    from dotenv import load_dotenv
except Exception:  # pragma: no cover
    load_dotenv = None

BASE_DIR = Path(__file__).resolve().parent
if load_dotenv is not None:
    load_dotenv(BASE_DIR / '.env')


def _split(value: str):
    return [item.strip() for item in (value or '').split(',') if item.strip()]


class Config:
    APP_VERSION = '1.0.0'

    # --- credentials (never written to disk by the app) ---
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '').strip()
    TAVILY_API_KEY = os.getenv('TAVILY_API_KEY', '').strip()

    # --- upstream endpoints ---
    GROQ_BASE = os.getenv('GROQ_BASE', 'https://api.groq.com/openai/v1').rstrip('/')
    TAVILY_BASE = os.getenv('TAVILY_BASE', 'https://api.tavily.com').rstrip('/')

    # --- model preferences, in priority order ---
    DEFAULT_MODELS = _split(os.getenv(
        'GROQ_MODELS',
        'openai/gpt-oss-120b,qwen/qwen3.6-27b,openai/gpt-oss-20b,'
        'llama-3.3-70b-versatile,llama-3.1-8b-instant',
    ))

    # --- server ---
    # --- public deployment hardening ---
    # PUBLIC_MODE=1: the browser may never store or send its own keys; only the server key is used.
    PUBLIC_MODE = os.getenv('PUBLIC_MODE', '0') == '1'
    RATE_LIMIT_PER_MIN = int(os.getenv('RATE_LIMIT_PER_MIN', '40'))
    MAX_TOKENS_CAP = int(os.getenv('MAX_TOKENS_CAP', '8000'))
    MAX_BODY_BYTES = int(os.getenv('MAX_BODY_BYTES', '200000'))
    ALLOWED_ORIGINS = _split(os.getenv('ALLOWED_ORIGINS', ''))  # empty = same-origin only when PUBLIC_MODE

    # --- server ---
    HOST = os.getenv('HOST', '127.0.0.1')
    PORT = int(os.getenv('PORT', '5000'))
    DEBUG = os.getenv('FLASK_DEBUG', '0') == '1'
    CORS = os.getenv('CORS', '1') != '0'

    # --- helpers ---
    @classmethod
    def has_groq(cls) -> bool:
        return bool(cls.GROQ_API_KEY)

    @classmethod
    def has_tavily(cls) -> bool:
        return bool(cls.TAVILY_API_KEY)

    @classmethod
    def as_public_dict(cls) -> dict:
        """Only what the browser is allowed to know - never the keys."""
        return {
            'ok': True,
            'version': cls.APP_VERSION,
            'groq': cls.has_groq(),
            'tavily': cls.has_tavily(),
            'public': cls.PUBLIC_MODE,
            'models': cls.DEFAULT_MODELS,
        }
