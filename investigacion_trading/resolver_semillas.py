"""Resolve seed identifiers through OpenAlex, without visiting SSRN."""
import json
import pathlib
import time
import urllib.parse
import urllib.request
from recolectar import parse_openalex, save

base = pathlib.Path(__file__).resolve().parent
seeds = json.loads((base / 'catalogo.json').read_text(encoding='utf-8'))
identifiers = []
for row in seeds:
    if row['fuente'] == 'SSRN':
        value = urllib.parse.parse_qs(urllib.parse.urlparse(row['url']).query).get('abstract_id', [])
        if value:
            identifiers.append('https://doi.org/10.2139/ssrn.' + value[0])
records = []
audit = []
out = base / 'descargas'
out.mkdir(exist_ok=True)
for offset in range(0, len(identifiers), 20):
    values = identifiers[offset:offset + 20]
    url = 'https://api.openalex.org/works?' + urllib.parse.urlencode({'filter': 'doi:' + '|'.join(values), 'per_page': 200})
    try:
        time.sleep(3.2)
        request = urllib.request.Request(url, headers={'User-Agent': 'DerivativesResearchMetadata/1.0'})
        with urllib.request.urlopen(request, timeout=40) as response:
            raw = response.read()
        (out / 'cache' / ('seed_doi_' + str(offset) + '.raw')).write_bytes(raw)
        rows, _, count = parse_openalex(raw)
        for row in rows:
            row['query'] = 'initial_seed_ssrn_doi_via_openalex'
        records.extend(rows)
        audit.append({'requested_dois': values, 'returned_count': count, 'status': 'ok'})
        save(out / 'openalex_semillas.json', records)
        print('Seed DOIs:', len(values), 'resolved:', len(rows), flush=True)
    except Exception as exc:
        audit.append({'requested_dois': values, 'error': type(exc).__name__})
        print('Seed lookup failed:', type(exc).__name__, flush=True)
        break
save(out / 'semillas_audit.json', audit)
