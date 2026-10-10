#!/usr/bin/env python3
"""PsycheDive - entry point.

Serves the single-file app from static/psychedive.html and proxies the two
optional services so their keys can live in .env instead of the browser:

    GET  /                      the app
    GET  /api/config            which server-side keys are configured
    GET  /api/groq/models       Groq model list
    POST /api/groq/chat/completions   Groq chat (streaming supported)
    POST /api/tavily/search     Tavily web search (optional)

Run:
    pip install -r requirements.txt
    cp .env.example .env      # then paste your keys
    python app.py
"""
from config import Config
from psychedive_app import create_app

app = create_app()

if __name__ == '__main__':
    print('PsycheDive %s' % Config.APP_VERSION)
    print('  Groq   key : %s' % ('configured' if Config.has_groq() else 'not set'))
    print('  Tavily key : %s' % ('configured' if Config.has_tavily() else 'not set'))
    print('  serving on http://%s:%s' % (Config.HOST, Config.PORT))
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG, threaded=True)
