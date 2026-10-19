# Progreso de las descargas

Corte: 2026-10-18 19:15:17 (Bogotá).

| Indicador | Cantidad |
|---|---:|
| Candidatos bibliográficos | 12,409 |
| Documentos con enlace y selección provisional | 2,276 |
| Procesados en esa selección | 2,276 (100.0%) |
| Pendientes de primer intento | 0 |
| PDFs verificados en el manifiesto | 1,577 |
| Archivos distintos por SHA-256 | 1,508 |
| Páginas descargadas | 45,542 |
| Errores de descarga | 369 |
| Accesos pendientes | 350 |

El porcentaje corresponde a intentos de esta selección; no mide exhaustividad ni descargas exitosas. Los candidatos aún requieren revisión de pertinencia y versiones. Este informe no comprueba si el proceso sigue activo.

| Procedencia identificada | Referencias | PDF verificado | Acceso pendiente | Sin intentar |
|---|---:|---:|---:|---:|
| SSRN | 4377 | 116 | 77 | 4116 |
| CME | 20 | 8 | 0 | 12 |

SSRN: el permiso guardado o la política del navegador volvió a rechazar el acceso directo. 49 de las 59 referencias iniciales fueron resueltas bibliográficamente en OpenAlex; las búsquedas adicionales de esa fuente amplían la tabla. CME: acceso parcial; consultar los conteos de la tabla. Las páginas HTML se archivan por separado cuando están disponibles.

Para consultar los PDFs, abrir [listado de documentos](corpus/ESTADO.md). Ese listado se actualiza durante la descarga.

Para ver conteos que se actualizan cada 15 segundos, ejecutar desde la carpeta del proyecto:

```powershell
python -X utf8 .\investigacion_trading\ver_progreso.py --watch
```

El descargador actualiza este archivo después de cada intento. Reabrirlo si el visor no refresca automáticamente. Para regenerarlo manualmente: añadir --save al comando sin --watch.