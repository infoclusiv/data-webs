"""Local read-only dashboard. Binds only to loopback; never serves .env or arbitrary files."""
import argparse
from collections import Counter, deque
import ctypes
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import threading
import time
from urllib.parse import urlparse

BASE = Path(__file__).resolve().parent
CORPUS = BASE / 'corpus'
GUARD = threading.Lock()
CACHE = {}
HISTORY = deque(maxlen=720)


def read(path):
    for attempt in range(5):
        try:
            return json.loads(path.read_text(encoding='utf-8-sig'))
        except (PermissionError, json.JSONDecodeError):
            if attempt == 4:
                raise
            time.sleep(.05)


def alive(pid):
    if not isinstance(pid, int) or pid <= 0:
        return False
    if os.name == 'nt':
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.OpenProcess.restype = ctypes.c_void_p
        kernel.OpenProcess.argtypes = [ctypes.c_ulong, ctypes.c_int, ctypes.c_ulong]
        kernel.GetExitCodeProcess.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ulong)]
        kernel.CloseHandle.argtypes = [ctypes.c_void_p]
        handle = kernel.OpenProcess(0x1000, False, pid)
        if not handle:
            return None if ctypes.get_last_error() == 5 else False
        try:
            code = ctypes.c_ulong()
            return code.value == 259 if kernel.GetExitCodeProcess(handle, ctypes.byref(code)) else None
        finally:
            kernel.CloseHandle(handle)
    try:
        os.kill(pid, 0)
        return True
    except PermissionError:
        return None
    except ProcessLookupError:
        return False


def snapshot():
    with GUARD:
        now = time.time()
        if now - CACHE.get('time', 0) < 2:
            return CACHE['data']
        index_path = CORPUS / 'inventario.json'
        stamp = index_path.stat().st_mtime_ns
        if CACHE.get('index_stamp') != stamp:
            CACHE['rows'] = read(index_path)
            CACHE['index_stamp'] = stamp
        rows = CACHE['rows']
        state = read(CORPUS / 'descargas_manifest.json')
        counts = Counter(v['status'] for v in state.values())
        selected = [r for r in rows if r['pdf_urls'] and (r.get('seed') or r['relevance'] != 'context_review')]
        queue_counts = Counter(state.get(r['doc_id'], {}).get('status', 'pending') for r in selected)
        sources = []
        for name in ['OpenAlex', 'arXiv', 'SSRN', 'CME']:
            subset = [r for r in rows if any(p['source'] == name for p in r['provenance'])]
            sc = Counter(state.get(r['doc_id'], {}).get('status', 'pending') for r in subset)
            sources.append({'name': name, 'records': len(subset), 'pdf': sc['verified_pdf'],
                            'blocked': sc['access_pending'], 'errors': sc['download_error'],
                            'without_pdf_link': sum(not r['pdf_urls'] for r in subset)})
        process_path = CORPUS / 'proceso_descarga.json'
        process = read(process_path) if process_path.exists() else {}
        latest = max((v.get('attempted_at_utc', '') for v in state.values()), default='')
        by_id = {r['doc_id']: r for r in rows}
        documents = []
        for result in sorted(state.values(), key=lambda r: r.get('attempted_at_utc', ''), reverse=True):
            row = by_id.get(result['doc_id'], result)
            sources_for_doc = list(dict.fromkeys(p['source'] for p in row.get('provenance', [])))
            attempts = result.get('attempts', [])
            last = attempts[-1] if attempts else {}
            detail = ('HTTP ' + str(last['http'])) if last.get('http') else last.get('reason', last.get('status', ''))
            documents.append({'id': result['doc_id'], 'title': result.get('title') or 'Sin título',
                              'status': result['status'], 'sources': sources_for_doc,
                              'pages': result.get('pages', 0), 'at': result.get('attempted_at_utc'),
                              'detail': detail, 'ocr': result.get('text_status') == 'needs_ocr_or_review'})
        coverage = []
        for path in sorted((BASE / 'descargas').glob('*_manifest.json')):
            values = list(read(path).values())
            coverage.append({'name': path.stem.replace('_manifest', ''), 'total': len(values),
                             'complete': sum(bool(v.get('complete')) for v in values)})
        pdf_count = counts['verified_pdf']
        HISTORY.append({'t': now, 'pdf': pdf_count})
        data = {'server_time': datetime.now(timezone.utc).isoformat(), 'latest_attempt': latest,
                'process': {'pid': process.get('pid'), 'alive': alive(process.get('pid')), 'started': process.get('started')},
                'inventory': len(rows), 'selected': len(selected), 'queue': dict(queue_counts),
                'counts': dict(counts), 'unique': len({v['sha256'] for v in state.values() if v.get('sha256')}),
                'pages': sum(v.get('pages', 0) for v in state.values()),
                'bytes': sum(v.get('bytes', 0) for v in state.values()),
                'ocr': sum(v.get('text_status') == 'needs_ocr_or_review' for v in state.values()),
                'no_link': sum(not r['pdf_urls'] for r in rows), 'sources': sources,
                'coverage': coverage, 'history': list(HISTORY), 'documents': documents}
        CACHE.update(time=now, data=data)
        return data


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        path = urlparse(self.path).path
        try:
            if path == '/':
                self.send_bytes((BASE / 'panel.html').read_bytes(), 'text/html; charset=utf-8')
            elif path == '/api/progreso':
                self.send_bytes(json.dumps(snapshot(), ensure_ascii=False).encode(), 'application/json; charset=utf-8')
            elif re.fullmatch(r'/pdf/[a-f0-9]{20}', path):
                identifier = path.rsplit('/', 1)[-1]
                result = read(CORPUS / 'descargas_manifest.json').get(identifier, {})
                pdf = CORPUS / 'documentos' / identifier / 'original.pdf'
                if result.get('status') != 'verified_pdf' or not pdf.is_file():
                    self.send_error(404)
                else:
                    self.send_bytes(pdf.read_bytes(), 'application/pdf')
            else:
                self.send_error(404)
        except (OSError, ValueError, KeyError):
            self.send_bytes(b'{"error":"No se pudo leer el estado. Reintentando en breve."}', 'application/json', 503)

    def send_bytes(self, data, content_type, status=200):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; object-src 'none'; frame-ancestors 'self'")
        self.end_headers()
        try:
            self.wfile.write(data)
        except (BrokenPipeError, ConnectionResetError):
            pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    print(f'Panel local: http://127.0.0.1:{args.port}', flush=True)
    server.serve_forever()
