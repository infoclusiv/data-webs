"""Build a research inventory and download accessible PDFs with page-level text.
No paywalls, challenge bypasses, paid content APIs, or credentials in URLs.
"""
import argparse
import collections
import concurrent.futures as cf
import datetime as dt
import hashlib
import json
import logging
import os
from pathlib import Path
import re
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from pypdf import PdfReader

logging.getLogger('pypdf').setLevel(logging.ERROR)
BASE = Path(__file__).resolve().parent
OUT = BASE / 'corpus'
LOCK = threading.Lock()
NEXT = {}
BLOCKED = {'papers.ssrn.com', 'ssrn.com', 'www.ssrn.com'}  # Browser-origin permission declined in this task.
INSTRUMENT = re.compile(r'\bfutures?\b|\boptions?\b|\bderivatives?\b|\bstraddles?\b|\bvariance risk|\bcommodity|\bhedging\b|\b0dte\b', re.I)
STRATEGY = re.compile(r'trad|strateg|momentum|carry|profit|return|hedg|arbitrage|reversion|volatility|backtest|risk premi|forecast|spread|seasonal|portfolio', re.I)
DIRECT = re.compile(r'futures|option.*trad|trad.*option|straddle|covered call|put.writ|iron condor|variance risk premi|gamma scalp|dispersion trad|0dte|risk reversal', re.I)
FINANCE = re.compile(r'\b(?:derivatives?|hedging|financial|arbitrage|volatility|portfolio|straddles?|commodit(?:y|ies)|equity|equities|securities|stocks?|forex|risk.premi|option pricing|futures contracts?|futures markets?|futures trading|Black.Scholes|asset pricing|interest.rates?|Treasury|bonds?|Nasdaq|S.P|VIX|SOFR)\b', re.I)


class ApprovedRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        host = urllib.parse.urlparse(newurl).hostname or ''
        if host == 'ssrn.com' or host.endswith('.ssrn.com'):
            raise RuntimeError('origin_permission_pending')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


HTTP = urllib.request.build_opener(ApprovedRedirect())


def save(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')
    for attempt in range(12):
        try:
            tmp.replace(path)
            return
        except PermissionError:
            if attempt == 11:
                raise
            time.sleep(0.1 * (attempt + 1))


def doi(value):
    return re.sub(r'^https?://(?:dx\.)?doi.org/', '', value or '').lower().strip()


def build_index():
    merged = {}
    for file in sorted((BASE / 'descargas').glob('*.json')):
        if not file.name.startswith(('openalex_', 'arxiv_')):
            continue
        if 'manifest' in file.name:
            continue
        for row in json.loads(file.read_text(encoding='utf-8')):
            key = 'doi:' + doi(row.get('doi')) if row.get('doi') else row['id']
            if key not in merged:
                merged[key] = dict(row, provenance=[], pdf_urls=[])
            target = merged[key]
            target['provenance'].append({'source': row['source'], 'id': row['id'], 'query': row.get('query')})
            if row.get('record_tag') == 'ssrn':
                target['provenance'].append({'source': 'SSRN', 'id': row.get('doi') or row['id'], 'query': 'SSRN location indexed by OpenAlex; ' + row.get('query', '')})
            if row['source'] == 'arXiv':
                target['pdf_urls'].append(re.sub(r'/abs/', '/pdf/', row.get('version_url') or row['id']).replace('http://', 'https://'))
                target['pdf_urls'].append(row['id'].replace('/abs/', '/pdf/'))
            for loc in row.get('locations') or []:
                if loc.get('is_oa') and loc.get('pdf_url'):
                    target['pdf_urls'].append(loc['pdf_url'])
            if not target.get('abstract') and row.get('abstract'):
                target['abstract'] = row['abstract']
    for seed in json.loads((BASE / 'catalogo.json').read_text(encoding='utf-8')):
        url = seed['url']
        normalized = re.sub(r'/pdf/', '/abs/', url).removesuffix('.pdf')
        target = next((r for r in merged.values() if any(p['id'] == normalized for p in r['provenance'])), None)
        if seed['fuente'] == 'SSRN':
            seed_id = urllib.parse.parse_qs(urllib.parse.urlparse(url).query).get('abstract_id', [''])[0]
            target = merged.get('doi:10.2139/ssrn.' + seed_id, target)
        if target is None:
            target = {'id': url, 'title': seed['titulo'], 'source': seed['fuente'], 'provenance': [], 'pdf_urls': []}
            merged['seed:' + url] = target
        target['provenance'].append({'source': seed['fuente'], 'id': url, 'query': 'initial_seed'})
        target['seed'] = True
        if seed['fuente'] == 'arXiv':
            target['pdf_urls'].append(normalized.replace('/abs/', '/pdf/'))
        elif seed['fuente'] == 'CME' and url.split('?')[0].endswith('.pdf'):
            target['pdf_urls'].append(url)
    rows = []
    for key, row in merged.items():
        title = row.get('title') or ''
        text = title + ' ' + (row.get('abstract') or '')
        row['doc_id'] = hashlib.sha256(key.encode()).hexdigest()[:20]
        row['pdf_urls'] = list(dict.fromkeys(u for u in row['pdf_urls'] if u.startswith(('https://', 'http://'))))
        row['relevance'] = 'priority_title' if DIRECT.search(title) else 'candidate_abstract' if INSTRUMENT.search(text) and STRATEGY.search(text) else 'context_review'
        if not FINANCE.search(text) and not row.get('seed'):
            row['relevance'] = 'context_review'
        row['eligibility'] = 'Provisional keyword screen; not a full-text relevance decision'
        rows.append(row)
    rows.sort(key=lambda r: (not r.get('seed', False), r['relevance'] != 'priority_title', r.get('published') or '', r.get('title') or ''))
    save(OUT / 'inventario.json', rows)
    return rows


def pace(host):
    if host == 'ssrn.com' or host.endswith('.ssrn.com'):
        raise RuntimeError('origin_permission_pending')
    with LOCK:
        if host in BLOCKED:
            raise RuntimeError('host_blocked_after_403_or_429')
        now = time.monotonic()
        wait = max(0, NEXT.get(host, 0) - now)
        NEXT[host] = now + wait + 3.2
    time.sleep(wait)


def download(row):
    identifier = row['doc_id']
    result = {'doc_id': identifier, 'title': row.get('title'), 'provenance': row['provenance'],
              'attempted_at_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'attempts': [], 'status': 'no_pdf_url'}
    for url in row['pdf_urls'][:5]:
        host = urllib.parse.urlparse(url).hostname or ''
        try:
            pace(host)
            req = urllib.request.Request(url, headers={'User-Agent': 'DerivativesResearchCorpus/1.0', 'Accept': 'application/pdf'})
            with HTTP.open(req, timeout=35) as response:
                data = response.read(30 * 1024 * 1024 + 1)
                final_url = response.url
                code = response.status
            if len(data) > 30 * 1024 * 1024:
                raise ValueError('size_limit_30MB')
            if not data.lstrip().startswith(b'%PDF-'):
                raise ValueError('not_a_pdf')
            import io
            reader = PdfReader(io.BytesIO(data), strict=False)
            count = len(reader.pages)
            if count == 0:
                raise ValueError('empty_pdf')
            folder = OUT / 'documentos' / identifier
            folder.mkdir(parents=True, exist_ok=True)
            pdf_path = folder / 'original.pdf'
            pdf_path.write_bytes(data)
            save(folder / 'metadatos.json', row)
            text_path = folder / 'paginas.jsonl'
            low_text, errors = 0, 0
            with text_path.open('w', encoding='utf-8') as stream:
                for number, page in enumerate(reader.pages, 1):
                    try:
                        text = page.extract_text() or ''
                        error = None
                    except Exception as exc:
                        text, error = '', type(exc).__name__
                        errors += 1
                    low_text += len(text.strip()) < 50
                    stream.write(json.dumps({'page': number, 'text': text, 'error': error}, ensure_ascii=False) + '\n')
            result.update(status='verified_pdf', local_pdf=str(pdf_path.resolve()), page_text=str(text_path.resolve()),
                          final_url=final_url, http_status=code, sha256=hashlib.sha256(data).hexdigest(),
                          bytes=len(data), pages=count, low_text_pages=low_text, extraction_error_pages=errors,
                          text_status='needs_ocr_or_review' if low_text or errors else 'extracted_not_visually_reviewed')
            result['attempts'].append({'url': url, 'status': 'verified_pdf', 'http': code})
            return result
        except urllib.error.HTTPError as exc:
            result['attempts'].append({'url': url, 'http': exc.code, 'status': 'http_error'})
            if exc.code in (403, 429):
                with LOCK:
                    BLOCKED.add(host)
            result['status'] = 'access_pending' if exc.code in (401, 403, 429) else 'download_error'
        except Exception as exc:
            result['attempts'].append({'url': url, 'status': type(exc).__name__, 'reason': str(exc)[:150]})
            if str(exc) in ('host_blocked_after_403_or_429', 'origin_permission_pending'):
                result['status'] = 'access_pending'
            elif result['status'] != 'access_pending':
                result['status'] = 'download_error'
    return result


def report(rows, state):
    hashes = {}
    for result in state.values():
        if result.get('sha256'):
            canonical = hashes.setdefault(result['sha256'], result['doc_id'])
            if canonical != result['doc_id']:
                result['identical_pdf_to'] = canonical
    coverage = {}
    for file in (BASE / 'descargas').glob('*_manifest.json'):
        values = list(json.loads(file.read_text(encoding='utf-8')).values())
        coverage[file.stem] = {'queries': len(values), 'complete_queries': sum(v.get('complete', False) for v in values),
                              'reported_results_sum_with_overlap': sum(v.get('reported_total', 0) or 0 for v in values),
                              'retrieved_results_sum_with_overlap': sum(v.get('retrieved_unique', 0) or 0 for v in values),
                              'errors': [v for v in values if v.get('last_error')]}
    summary = {'updated_at_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'inventory_records': len(rows),
               'relevance': dict(collections.Counter(r['relevance'] for r in rows)),
               'download_status': dict(collections.Counter(v['status'] for v in state.values())),
               'unique_pdf_hashes': len(hashes), 'total_pdf_pages': sum(v.get('pages', 0) for v in state.values()),
               'metadata_coverage': coverage, 'exhaustive': False,
               'limitations': ['Provisional relevance screen', 'Citation expansion pending', 'SSRN/CME discovery not complete',
                               'No PDF content API spending', 'OCR and visual full-text review pending']}
    save(OUT / 'estado.json', summary)
    save(OUT / 'descargas_manifest.json', state)
    with (OUT / 'cola_revision.jsonl').open('w', encoding='utf-8') as stream:
        for result in state.values():
            if result['status'] == 'verified_pdf':
                identifier = result['doc_id']
                stream.write(json.dumps({'doc_id': identifier, 'titulo': result['title'],
                                         'pdf': 'documentos/' + identifier + '/original.pdf',
                                         'texto_por_pagina': 'documentos/' + identifier + '/paginas.jsonl',
                                         'text_status': result.get('text_status'), 'estado_revision': 'pendiente',
                                         'instrucciones': '../PARA_EL_AGENTE.md'}, ensure_ascii=False) + '\n')
    lines = ['# Estado de la recolección', '', 'Actualizado (UTC): ' + summary['updated_at_utc'], '',
             '- Candidatos en inventario: ' + str(len(rows)),
             '- PDFs verificados: ' + str(summary['download_status'].get('verified_pdf', 0)),
             '- Archivos PDF únicos por hash: ' + str(len(hashes)),
             '- Páginas de PDF: ' + str(summary['total_pdf_pages']),
             '- Cobertura exhaustiva: todavía no.', '',
             'Los PDF están en documentos/<doc_id>/original.pdf. Cada carpeta incluye metadatos y texto por página.', '',
             '## Consultas de metadatos', '']
    for name, value in coverage.items():
        lines.append('- ' + name + ': ' + str(value['complete_queries']) + '/' + str(value['queries']) + ' consultas registradas completas.')
    lines.extend(['', 'SSRN: el permiso guardado o la política del navegador bloquea el acceso directo. CME: acceso parcial, con PDFs descargados y otros recursos pendientes.',
                  'Pendientes: expansión de citas, evaluación de pertinencia en texto completo, OCR y revisión de tablas/fórmulas.', '',
                  '## Documentos descargados', ''])
    for result in state.values():
        if result['status'] == 'verified_pdf':
            lines.append('- [' + str(result['title']).replace('[', '(').replace(']', ')') + '](documentos/' + result['doc_id'] + '/original.pdf) — ' + str(result['pages']) + ' páginas.')
    (OUT / 'ESTADO.md').write_text('\n'.join(lines), encoding='utf-8')
    from ver_progreso import snapshot
    (BASE / 'PROGRESO.md').write_text(snapshot(), encoding='utf-8')
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['index', 'download', 'report'])
    parser.add_argument('--source', choices=['all', 'arxiv', 'cme'], default='all')
    parser.add_argument('--limit', type=int, default=0, help='0 means all eligible records')
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--retry-errors', action='store_true')
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    # OS-level lock prevents two writers from overwriting the same manifest.
    lock_handle = (OUT / '.download.lock').open('a+b')
    if lock_handle.tell() == 0:
        lock_handle.write(b'0')
        lock_handle.flush()
    lock_handle.seek(0)
    if os.name == 'nt':
        import msvcrt
        try:
            msvcrt.locking(lock_handle.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError:
            parser.exit(4, 'Another corpus process is already running.\n')
    rows = build_index()
    path = OUT / 'descargas_manifest.json'
    state = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    report(rows, state)
    if args.action == 'download':
        jobs = [r for r in rows if r['pdf_urls'] and (r.get('seed') or r['relevance'] != 'context_review')
                and (r['doc_id'] not in state or (args.retry_errors and state[r['doc_id']]['status'] == 'download_error'))
                and (args.source == 'all' or any(p['source'].lower() == args.source for p in r['provenance']))]
        if args.limit:
            jobs = jobs[:args.limit]
        print('PDF queue:', len(jobs), flush=True)
        with cf.ThreadPoolExecutor(max_workers=args.workers) as pool:
            pending = iter(jobs)
            active = {pool.submit(download, row) for row in list(jobs[:args.workers])}
            for _ in range(min(len(jobs), args.workers)):
                next(pending)
            while active:
                completed, active = cf.wait(active, return_when=cf.FIRST_COMPLETED)
                for future in completed:
                    result = future.result()
                    state[result['doc_id']] = result
                    report(rows, state)
                    print(result['status'], result['doc_id'], result.get('pages', 0), str(result['title'])[:90], flush=True)
                    if not (OUT / 'detener_descarga.flag').exists():
                        row = next(pending, None)
                        if row:
                            active.add(pool.submit(download, row))
    print(json.dumps(report(rows, state), ensure_ascii=False), flush=True)
    save(OUT / 'ejecucion_finalizada.json', {'pid': os.getpid(), 'finished_at_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
                                          'state': 'download_pass_finished_not_exhaustive'})


if __name__ == '__main__':
    main()
