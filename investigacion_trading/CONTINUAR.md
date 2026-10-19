# Uso de la biblioteca y continuidad

La recolección de metadatos y la descarga de documentos son etapas distintas. Que una consulta esté paginada por completo no demuestra que todo el tema esté cubierto. La evaluación de pertinencia es provisional y no se ha efectuado una revisión sistemática de los textos completos.

## Estado y documentos

- `PROGRESO.md` se actualiza tras cada intento con cola procesada, pendientes y conteos por procedencia. Reabrirlo si el visor no refleja cambios. `ver_progreso.py --watch` muestra conteos cada 15 segundos.

- Abrir `corpus/ESTADO.md` para ver los conteos y el listado enlazado de PDFs. Se actualiza después de cada intento de descarga.
- `corpus/estado.json` contiene los mismos conteos en formato estructurado.
- `corpus/inventario.json` conserva candidatos y procedencia de consultas.
- `corpus/descargas_manifest.json` registra intentos, bloqueos, rutas, SHA-256, páginas y estado de extracción de texto.
- `corpus/documentos/` contiene los PDFs originales y textos por página.
- `corpus/cola_revision.jsonl` y `PARA_EL_AGENTE.md` preparan la revisión por otro agente. No se ha enviado ningún archivo a un servicio externo.

## Proceso local

El proceso de descarga se lanzó oculto en Windows, con sus identificadores y rutas de registro en `corpus/proceso_descarga.json`. Requiere que el equipo siga encendido y con conexión. No es una automatización programada ni un servicio con reinicio automático. Consultar si el PID sigue vivo y si el registro continúa avanzando; la existencia del archivo de proceso no basta para confirmar actividad.

`corpus/ejecucion_finalizada.json` se escribe al terminar una pasada. Comparar su fecha y PID con los del proceso actual; una pasada terminada no significa cobertura exhaustiva. Los archivos y el manifiesto permiten reanudar después de un cierre o error.

Desde esta carpeta, para reanudar cuando no haya otra instancia:

```powershell
python -X utf8 .\gestionar_corpus.py download --workers 4
```

Para volver a intentar errores de descarga (no bloqueos de acceso):

```powershell
python -X utf8 .\gestionar_corpus.py download --workers 4 --retry-errors
```

No ejecutar dos instancias; el bloqueo de proceso impide escritores simultáneos en Windows. La reanudación omite documentos ya registrados, por lo que las restricciones requieren resolución específica antes de reintentar. Las respuestas 403/429 detienen solicitudes posteriores al host durante esa pasada. SSRN está excluido de accesos directos y redirecciones porque el permiso del navegador no fue concedido en esta sesión.

## Cobertura de esta fase

Ampliación completada: seis consultas restringidas a ubicaciones de SSRN Electronic Journal en OpenAlex devolvieron 4.624 coincidencias y 4.344 identificadores distintos. Se integraron al inventario (12.409 candidatos al corte de la ampliación). CME tiene ocho PDFs verificados de veinte referencias. Consultar `CME_SSRN_CONTINUACION.md` para detalles y restricciones. La conexión directa con SSRN sigue bloqueada por el permiso guardado o la política del navegador, pese a la autorización del usuario.

Se completaron las 25 consultas iniciales precisas de OpenAlex y las cinco de arXiv con fecha de corte 2026-10-18. Los resultados suman 7.424 y 1.502 respectivamente antes de descontar solapamientos entre consultas. OpenAlex resolvió 49 DOI de las 59 referencias SSRN iniciales; diez DOI no fueron devueltos en esa consulta. Esto no significa que esos diez estudios no existan.

Se consultó una primera capa de 1.050 identificadores citados por las 49 semillas resueltas. Se devolvieron 1.023 registros con el filtro de fecha de corte; 27 no se devolvieron y requieren revisión de los identificadores, la fecha y la disponibilidad. El detalle está en `descargas/referencias_audit.json`. Las búsquedas más amplias retiradas por exceso de ruido permanecen en `descargas/exploratoria/` y no se incorporan al inventario activo.

Esta fase aún no acredita exhaustividad: faltan expansión adicional de referencias y citantes, búsquedas complementarias por producto/tema, completar SSRN y CME, resolver registros sin PDF y restricciones, evaluar pertinencia y versiones en texto completo y aplicar OCR donde corresponda. Las consultas iniciales de arXiv usan categorías y términos en inglés; eso limita la cobertura y exige búsquedas complementarias.

## Credenciales y consumo

La clave local de OpenAlex se lee desde `.env`, excluido de Git, o desde `OPENALEX_API_KEY`. No se imprime ni debe incluirse en paquetes para el otro agente. No se han activado compras ni descargas de pago de la API de contenido de OpenAlex. La descarga usa enlaces originales de PDF localizados en los metadatos y arXiv; tener una clave no garantiza acceso a todos los PDFs.

No entregar `.env`, registros del sistema ajenos al proyecto ni directorios de configuración al agente revisor. Entregar la carpeta de corpus y las instrucciones, conservando las licencias y la procedencia de cada documento.
