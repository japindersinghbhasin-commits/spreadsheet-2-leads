# -*- coding: utf-8 -*-
"""
Shared fast DDG search helper used by both Furniture and Real Estate engines.
- Each thread gets its own curl_cffi session (no lock contention)
- Falls back to Jina if DDG returns empty
"""
import threading, urllib.request, urllib.parse, re

try:
    from curl_cffi import requests as cffi_requests
    _USE_CFFI = True
except ImportError:
    _USE_CFFI = False

_local = threading.local()

def _get_session():
    """Return a per-thread curl_cffi session."""
    if not _USE_CFFI:
        return None
    if not hasattr(_local, 'session'):
        _local.session = cffi_requests.Session(impersonate="chrome120")
    return _local.session

_DDG_HDRS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://html.duckduckgo.com/',
}

def ddg_search(q_str):
    """
    Search DuckDuckGo for q_str.
    Returns list of (handle, fol_or_None, title, snippet_text) tuples.
    """
    data = urllib.parse.urlencode({'q': q_str, 'b': ''}).encode('utf-8')
    text = ""

    # 1. Try curl_cffi per-thread session (fastest, no lock)
    sess = _get_session()
    if sess:
        try:
            r = sess.post('https://html.duckduckgo.com/html/', data=data,
                          headers=_DDG_HDRS, timeout=12)
            if r.status_code in (200, 202) and len(r.text) >= 500:
                text = r.text
        except Exception:
            pass

    # 2. Jina fallback (no rate-limit issues at moderate concurrency)
    if len(text) < 500:
        try:
            jina_url = "https://r.jina.ai/https://duckduckgo.com/html/?q=" + urllib.parse.quote(q_str)
            req = urllib.request.Request(jina_url,
                headers={'Accept': 'text/plain', 'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=12) as rp:
                text = rp.read().decode('utf-8', errors='ignore')
        except Exception:
            return []

    if len(text) < 200:
        return []

    results = []

    # ── Jina markdown format ──────────────────────────────────────────────────
    if '## [' in text:
        blocks = re.split(r'\n(?=##\s+\[)', text.replace('**', ''))
        for blk in blocks[1:]:
            m_h     = re.search(r'\(@([a-zA-Z0-9_.]+)\)', blk)
            m_ig    = re.search(r'instagram\.com/([a-zA-Z0-9_.]+)', blk) if not m_h else None
            m_fol   = re.search(r'([0-9.,]+)\s*([KkMm]?)\s*Followers', blk, re.IGNORECASE)
            m_title = re.search(r'##\s+\[(.*?)\]', blk)
            handle  = m_h or m_ig
            if not handle:
                continue
            h   = handle.group(1).lower().strip('.')
            fol = None
            if m_fol:
                num  = float(m_fol.group(1).replace(',', ''))
                unit = m_fol.group(2).upper()
                fol  = int(num * 1_000_000) if unit == 'M' else (int(num * 1000) if unit == 'K' else int(num))
            results.append((h, fol, m_title.group(1) if m_title else h, blk))

    # ── Raw HTML format ───────────────────────────────────────────────────────
    else:
        # Split on result boundaries
        for chunk in re.split(r'(?=<a\s[^>]*href=["\']https?://www\.instagram\.com)', text):
            m_ig  = re.search(r'instagram\.com/([a-zA-Z0-9_.]+)', chunk, re.IGNORECASE)
            m_fol = re.search(r'([0-9.,]+)\s*([KkMm]?)\s*Followers', chunk, re.IGNORECASE)
            if not m_ig:
                continue
            h   = m_ig.group(1).lower().strip('.')
            fol = None
            if m_fol:
                num  = float(m_fol.group(1).replace(',', ''))
                unit = m_fol.group(2).upper()
                fol  = int(num * 1_000_000) if unit == 'M' else (int(num * 1000) if unit == 'K' else int(num))
            snippet = re.sub(r'<[^>]+>', ' ', chunk)
            snippet = ' '.join(snippet.split())[:400]
            results.append((h, fol, h, snippet))

    return results
