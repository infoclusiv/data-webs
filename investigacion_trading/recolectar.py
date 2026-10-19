"""Metadata collector. Standard library only; no PDF downloads or SSRN/CME scraping.

Credentials: OPENALEX_API_KEY environment variable or local ignored .env file.
Re-run with identical parameters to resume. Use a new --out to refresh a snapshot.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

BASE = Path(__file__).resolve().parent
NS = {'a': 'http://www.w3.org/2005/Atom',
      'o': 'http://a9.com/-/spec/opensearch/1.1/',
      'x': 'http://arxiv.org/schemas/atom'}


def save(path, data):
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    for attempt in range(12):
        try:
            temp.replace(path)
            return
        except PermissionError:
            if attempt == 11:
                raise
            time.sleep(0.1 * (attempt + 1))


def abstract(index):
    if not index:
        return None
    words = {position: word for word, positions in index.items() for position in positions}
    return ' '.join(words[p] for p in sorted(words))


def get(url, key, cache, delay):
    if cache.exists():
        return cache.read_bytes()
    headers = {'User-Agent': 'DerivativesResearchMetadata/1.0'}
    if key:
        headers['Authorization'] = 'Bearer ' + key
    for attempt in range(3):
        time.sleep(max(delay, 3.1))
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=45) as response:
                data = response.read()
            cache.write_bytes(data)
            return data
        except urllib.error.HTTPError as error:
            if error.code not in (429, 500, 502, 503, 504) or attempt == 2:
                raise RuntimeError('HTTP ' + str(error.code)) from None
            time.sleep(min(30, 5 * (attempt + 1)))
    raise RuntimeError('No response')


def parse_openalex(data):
    payload = json.loads(data)
    rows = []
    for work in payload.get('results', []):
        rows.append({'source': 'OpenAlex', 'id': work['id'], 'doi': work.get('doi'),
                     'title': work.get('title'), 'published': work.get('publication_date'),
                     'authors': [a.get('author', {}).get('display_name') for a in work.get('authorships', [])],
                     'abstract': abstract(work.get('abstract_inverted_index')),
                     'open_access': work.get('open_access'), 'locations': work.get('locations'),
                     'references': work.get('referenced_works'), 'cited_by_count': work.get('cited_by_count'),
                     'content_urls': work.get('content_urls'), 'has_content': work.get('has_content'),
                     'is_retracted': work.get('is_retracted'), 'topics': work.get('topics'),
                     'status': 'Metadata only; relevance and full text pending'})
    return rows, payload.get('meta', {}).get('next_cursor'), payload.get('meta', {}).get('count')


def parse_arxiv(data):
    root = ET.fromstring(data)
    rows = []
    for entry in root.findall('a:entry', NS):
        versioned = entry.findtext('a:id', default='', namespaces=NS)
        if '/api/errors' in versioned:
            raise ValueError('arXiv returned an API error feed')
        if not versioned:
            raise ValueError('arXiv entry without identifier')
        identifier = re.sub(r'v\d+$', '', versioned.replace('http://', 'https://'))
        rows.append({'source': 'arXiv', 'id': identifier, 'version_url': versioned,
                     'title': ' '.join(entry.findtext('a:title', default='', namespaces=NS).split()),
                     'authors': [a.findtext('a:name', namespaces=NS) for a in entry.findall('a:author', NS)],
                     'published': entry.findtext('a:published', namespaces=NS),
                     'updated': entry.findtext('a:updated', namespaces=NS),
                     'doi': entry.findtext('x:doi', namespaces=NS),
                     'abstract': entry.findtext('a:summary', namespaces=NS),
                     'categories': [a.get('term') for a in entry.findall('a:category', NS)],
                     'links': [a.attrib for a in entry.findall('a:link', NS)],
                     'status': 'Metadata only; relevance and full text pending'})
    total = int(root.findtext('o:totalResults', default='0', namespaces=NS))
    return rows, total


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', choices=['openalex', 'arxiv'], required=True)
    parser.add_argument('--max-pages', type=int, default=3, help='Additional pages per query this run')
    parser.add_argument('--page-size', type=int, default=100)
    parser.add_argument('--delay', type=float, default=3.1)
    parser.add_argument('--out', type=Path, default=BASE / 'descargas')
    parser.add_argument('--max-requests', type=int, default=85)
    parser.add_argument('--config', type=Path, default=BASE / 'consultas.json')
    parser.add_argument('--extra-filter', default='')
    parser.add_argument('--record-tag', default='')
    args = parser.parse_args()
    if args.max_pages < 1 or not 1 <= args.page_size <= 200:
        parser.error('max-pages >= 1 and page-size between 1 and 200 required')
    if args.record_tag and not re.fullmatch(r'[a-z_]+', args.record_tag):
        parser.error('record-tag must contain lowercase letters or underscores')
    cfg = json.loads(args.config.read_text(encoding='utf-8'))
    args.out.mkdir(parents=True, exist_ok=True)
    cache_dir = args.out / 'cache'
    cache_dir.mkdir(exist_ok=True)
    local_env = BASE / '.env'
    if local_env.exists():
        for line in local_env.read_text(encoding='utf-8-sig').splitlines():
            if line.strip().startswith('OPENALEX_API_KEY='):
                candidate = line.split('=', 1)[1].strip().strip('\"\'')
                if candidate and candidate != 'YOUR_API_KEY_HERE':
                    os.environ.setdefault('OPENALEX_API_KEY', candidate)
    key = os.getenv('OPENALEX_API_KEY') if args.source == 'openalex' else None
    manifest = args.out / (args.source + ('_' + args.record_tag if args.record_tag else '') + '_manifest.json')
    state = json.loads(manifest.read_text(encoding='utf-8')) if manifest.exists() else {}
    failures = 0
    requests_made = 0
    for query in cfg[args.source]:
        signature = hashlib.sha256((args.source + query + str(args.page_size) + ('titleabstract-cutoff-v3-sorted' if args.source == 'openalex' else 'titleabstract-cutoff-v2') + args.extra_filter + args.record_tag).encode()).hexdigest()[:20]
        progress = state.setdefault(signature, {'query': query, 'page_size': args.page_size,
                                               'cursor': '*', 'start': 0, 'pages': 0, 'complete': False})
        if progress['complete']:
            continue
        records_path = args.out / (args.source + '_' + signature + '.json')
        records = json.loads(records_path.read_text(encoding='utf-8')) if records_path.exists() else []
        by_id = {row['id']: row for row in records}
        for _ in range(args.max_pages):
            if requests_made >= args.max_requests:
                print('Request budget reached; remaining queries pending', flush=True)
                raise SystemExit(2)
            if args.source == 'openalex':
                params = {'filter': 'title_and_abstract.search:' + query + ',to_publication_date:2026-10-18', 'per-page': args.page_size, 'sort': 'publication_date:asc'}
                if args.extra_filter:
                    params['filter'] += ',' + args.extra_filter
                if key and progress.get('cursor'):
                    params['cursor'] = progress['cursor']
                else:
                    if progress['start'] >= 10000:
                        progress['last_error'] = 'Public paging boundary 10000; key or date partition required'
                        save(manifest, state)
                        break
                    params['page'] = progress['pages'] + 1
                endpoint = 'https://api.openalex.org/works'
            else:
                params = {'search_query': '(' + query + ') AND submittedDate:[199101010000 TO 202610182359]', 'start': progress['start'],
                          'max_results': args.page_size, 'sortBy': 'submittedDate', 'sortOrder': 'ascending'}
                endpoint = 'https://export.arxiv.org/api/query'
            url = endpoint + '?' + urllib.parse.urlencode(params)
            cache = cache_dir / (hashlib.sha256(url.encode()).hexdigest() + '.raw')
            try:
                requests_made += 1
                raw = get(url, key, cache, args.delay)
                if args.source == 'openalex':
                    rows, cursor, total = parse_openalex(raw)
                    done = not rows or progress['start'] + len(rows) >= total
                else:
                    rows, total = parse_arxiv(raw)
                    cursor = None
                    done = not rows or progress['start'] + len(rows) >= total
                for row in rows:
                    row['retrieved_at_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
                    row['query'] = query
                    if args.record_tag:
                        row['record_tag'] = args.record_tag
                    by_id[row['id']] = row
                save(records_path, list(by_id.values()))
                progress.update(cursor=cursor, start=progress['start'] + len(rows),
                                pages=progress['pages'] + 1, complete=done,
                                reported_total=total, retrieved_unique=len(by_id), last_error=None)
                save(manifest, state)
                print(args.source, signature, 'pages', progress['pages'], 'unique', len(by_id), 'total', total, 'complete', done, flush=True)
                if done:
                    break
            except Exception as error:
                # Never print request headers or credentials. Endpoint has no secret query parameters.
                progress['last_error'] = type(error).__name__ + ': ' + str(error)[:150]
                progress['complete'] = False
                save(manifest, state)
                failures += 1
                print('Query failed:', signature, type(error).__name__, str(error)[:150], flush=True)
                if 'HTTP 429' in str(error) or 'HTTP 401' in str(error) or 'HTTP 402' in str(error):
                    print('Quota or authorization boundary; stopping source', flush=True)
                    raise SystemExit(3)
                break
    print('Finished. Query failures:', failures, '. A page limit is not exhaustive coverage.')
    raise SystemExit(1 if failures else 0)


if __name__ == '__main__':
    main()
