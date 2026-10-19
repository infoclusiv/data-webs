"""Read-only download monitor. --watch refreshes the console every 15 seconds."""
import argparse
from collections import Counter
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import time

BASE = Path(__file__).resolve().parent


def snapshot():
    corpus = BASE / 'corpus'
    rows = json.loads((corpus / 'inventario.json').read_text(encoding='utf-8'))
    state = json.loads((corpus / 'descargas_manifest.json').read_text(encoding='utf-8'))
    eligible = [r for r in rows if r['pdf_urls'] and (r.get('seed') or r['relevance'] != 'context_review')]
    attempted = sum(r['doc_id'] in state for r in eligible)
    counts = Counter(r['status'] for r in state.values())
    now = datetime.now(timezone(timedelta(hours=-5))).strftime('%Y-%m-%d %H:%M:%S')
    lines = ['# Progreso de las descargas', '', f'Corte: {now} (Bogotá).', '',
             '| Indicador | Cantidad |', '|---|---:|',
             f'| Candidatos bibliográficos | {len(rows):,} |',
             f'| Documentos con enlace y selección provisional | {len(eligible):,} |',
             f'| Procesados en esa selección | {attempted:,} ({attempted / len(eligible):.1%}) |' if eligible else '| Procesados | 0 |',
             f'| Pendientes de primer intento | {len(eligible)-attempted:,} |',
             f'| PDFs verificados en el manifiesto | {counts["verified_pdf"]:,} |',
             f'| Archivos distintos por SHA-256 | {len({r["sha256"] for r in state.values() if r.get("sha256")}):,} |',
             f'| Páginas descargadas | {sum(r.get("pages", 0) for r in state.values()):,} |',
             f'| Errores de descarga | {counts["download_error"]:,} |',
             f'| Accesos pendientes | {counts["access_pending"]:,} |', '',
             'El porcentaje corresponde a intentos de esta selección; no mide exhaustividad ni descargas exitosas. '
             'Los candidatos aún requieren revisión de pertinencia y versiones. Este informe no comprueba si el proceso sigue activo.', '',
             '| Procedencia identificada | Referencias | PDF verificado | Acceso pendiente | Sin intentar |',
             '|---|---:|---:|---:|---:|']
    for source in ['SSRN', 'CME']:
        subset = [r for r in rows if any(p['source'] == source for p in r['provenance'])]
        statuses = Counter(state.get(r['doc_id'], {}).get('status', 'not_attempted') for r in subset)
        lines.append(f'| {source} | {len(subset)} | {statuses["verified_pdf"]} | {statuses["access_pending"]} | {statuses["not_attempted"]} |')
    lines += ['', 'SSRN: el permiso guardado o la política del navegador volvió a rechazar el acceso directo. '
              '49 de las 59 referencias iniciales fueron resueltas bibliográficamente en OpenAlex; las búsquedas adicionales de esa fuente amplían la tabla. '
              'CME: acceso parcial; consultar los conteos de la tabla. Las páginas HTML se archivan por separado cuando están disponibles.', '',
              'Para consultar los PDFs, abrir [listado de documentos](corpus/ESTADO.md). '
              'Ese listado se actualiza durante la descarga.', '',
              'Para ver conteos que se actualizan cada 15 segundos, ejecutar desde la carpeta del proyecto:', '',
              '```powershell', 'python -X utf8 .\\investigacion_trading\\ver_progreso.py --watch', '```', '',
              'El descargador actualiza este archivo después de cada intento. Reabrirlo si el visor no refresca automáticamente. Para regenerarlo manualmente: añadir --save al comando sin --watch.']
    return '\n'.join(lines)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--watch', action='store_true')
    parser.add_argument('--save', action='store_true')
    args = parser.parse_args()
    try:
        while True:
            result = snapshot()
            print(result, flush=True)
            if args.save:
                (BASE / 'PROGRESO.md').write_text(result, encoding='utf-8')
            if not args.watch:
                break
            time.sleep(15)
    except KeyboardInterrupt:
        pass
