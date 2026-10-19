"""Retrieve one documented reference layer from resolved seed studies."""
import json
import os
import pathlib
import time
import urllib.parse
import urllib.request
from recolectar import parse_openalex, save

base = pathlib.Path(__file__).resolve().parent
out = base / 'descargas'
seeds = json.loads((out / 'openalex_semillas.json').read_text(encoding='utf-8'))
refs = sorted({ref.rsplit('/', 1)[-1] for row in seeds for ref in row.get('references') or []})
key = os.getenv('OPENALEX_API_KEY')
env = base / '.env'
if env.exists():
    for line in env.read_text(encoding='utf-8-sig').splitlines():
        if line.strip().startswith('OPENALEX_API_KEY='):
            key = line.split('=', 1)[1].strip().strip('\"\'')
headers = {'User-Agent': 'DerivativesResearchMetadata/1.0'}
if key and key != 'YOUR_API_KEY_HERE':
    headers['Authorization'] = 'Bearer ' + key
path = out / 'openalex_referencias.json'
rows = json.loads(path.read_text(encoding='utf-8')) if path.exists() else []
known = {r['id'].rsplit('/', 1)[-1] for r in rows}
audit_path = out / 'referencias_audit.json'
audit = json.loads(audit_path.read_text(encoding='utf-8')) if audit_path.exists() else []
remaining = [r for r in refs if r not in known]
for offset in range(0, len(remaining), 50):
    values = remaining[offset:offset + 50]
    url = 'https://api.openalex.org/works?' + urllib.parse.urlencode({'filter': 'openalex:' + '|'.join(values) + ',to_publication_date:2026-10-18', 'per_page': 200})
    try:
        time.sleep(3.2)
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=40) as response:
            raw = response.read()
        import hashlib
        (out / 'cache' / ('references_' + hashlib.sha256(url.encode()).hexdigest() + '.raw')).write_bytes(raw)
        new, _, total = parse_openalex(raw)
        for row in new:
            row['query'] = 'seed_references_round_1'
        rows.extend(new)
        audit.append({'round': 1, 'requested_ids': values, 'returned': len(new), 'status': 'ok'})
        save(path, rows)
        save(audit_path, audit)
        print('Reference layer:', len(rows), '/', len(refs), flush=True)
    except Exception as exc:
        audit.append({'round': 1, 'requested_ids': values, 'error': type(exc).__name__})
        save(audit_path, audit)
        print('Reference query failed:', type(exc).__name__, flush=True)
        break
