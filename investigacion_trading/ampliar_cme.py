"""Bounded discovery of PDF links on the selected CME pages; preserves HTML."""
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = Path(__file__).resolve().parent
OUT = BASE / 'descargas' / 'cme_paginas'


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            href = dict(attrs).get('href')
            if href:
                self.links.append(href)


class CMERedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        host = urllib.parse.urlparse(newurl).hostname or ''
        if host != 'cmegroup.com' and not host.endswith('.cmegroup.com'):
            raise ValueError('redirect_outside_cme_not_requested')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    path = BASE / 'catalogo.json'
    seeds = json.loads(path.read_text(encoding='utf-8'))
    urls = {s['url'] for s in seeds}
    additions = []
    audit = []
    def add(title, url, parent):
        if url in urls:
            return
        urls.add(url)
        additions.append({'id': 'CME-' + hashlib.sha256(url.encode()).hexdigest()[:12],
                          'titulo': title, 'url': url, 'fuente': 'CME', 'fecha_consulta': '2026-10-18',
                          'estado': 'Localizado; descarga y evaluación pendientes',
                          'resultado': 'Pendiente de evaluación', 'lote_busqueda': 'cme_expansion_1',
                          'pagina_origen': parent, 'posibles_versiones_duplicadas': [],
                          'revision_pertinencia': 'Pendiente; puede ser contexto o educación'})
    for title, url in [
        ('Managed Futures Research Digest', 'https://www.cmegroup.com/education/files/research-digest.pdf'),
        ('Options on Futures as Strategic Investment Vehicles', 'https://www.cmegroup.com/education/files/options-on-futures-as-strategic-investment-vehicles.pdf'),
        ('25 Proven Strategies', 'https://www.cmegroup.com/articles/files/2022/25-proven-strategies.pdf')]:
        add(title, url, 'Official CME pages checked with web search on 2026-10-18')
    http = urllib.request.build_opener(CMERedirect())
    for row in seeds:
        if row['fuente'] != 'CME' or urllib.parse.urlparse(row['url']).path.endswith('.pdf'):
            continue
        item = {'url': row['url']}
        try:
            time.sleep(3.3)
            req = urllib.request.Request(row['url'], headers={'User-Agent': 'DerivativesResearchCorpus/1.0'})
            with http.open(req, timeout=30) as response:
                raw = response.read(5 * 1024 * 1024 + 1)
                if len(raw) > 5 * 1024 * 1024:
                    raise ValueError('html_size_limit')
                final = response.url
            filename = hashlib.sha256(row['url'].encode()).hexdigest()[:20] + '.html'
            (OUT / filename).write_bytes(raw)
            parser = Links()
            parser.feed(raw.decode('utf-8', errors='replace'))
            pdfs = []
            for href in parser.links:
                url = urllib.parse.urljoin(final, href)
                parsed = urllib.parse.urlparse(url)
                if parsed.scheme == 'https' and (parsed.hostname == 'cmegroup.com' or (parsed.hostname or '').endswith('.cmegroup.com')) and parsed.path.lower().endswith('.pdf'):
                    pdfs.append(url)
                    add(parsed.path.rsplit('/', 1)[-1].removesuffix('.pdf').replace('-', ' '), url, row['url'])
            item.update(status='saved_html', file=filename, pdf_links=list(dict.fromkeys(pdfs)))
        except urllib.error.HTTPError as exc:
            item.update(status='http_error', code=exc.code)
            audit.append(item)
            if exc.code in (401, 403, 429):
                print('CME discovery stopped on HTTP', exc.code, flush=True)
                break
            continue
        except Exception as exc:
            item.update(status=type(exc).__name__)
        audit.append(item)
        print(item['status'], row['titulo'], flush=True)
    (OUT / 'audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding='utf-8')
    temp = path.with_suffix('.json.tmp')
    temp.write_text(json.dumps(seeds + additions, ensure_ascii=False, indent=2), encoding='utf-8')
    temp.replace(path)
    print('New CME references:', len(additions), flush=True)


if __name__ == '__main__':
    main()
