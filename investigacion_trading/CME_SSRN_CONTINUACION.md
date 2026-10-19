# Continuación de CME y SSRN

Corte: 18 de octubre de 2026. Los tres documentos de la tabla ya fueron incorporados al inventario, descargados y verificados: firma PDF, páginas, texto por página y SHA-256. Se inspeccionó visualmente la portada del Research Digest.

## CME

Ocho de las 20 referencias CME actuales tienen PDF verificado. Las otras doce son páginas HTML pendientes de revisar; algunas son material educativo sin PDF independiente. El intento de recuperación HTML recibió HTTP 403 en la primera página y se detuvo; auditoría en descargas/cme_paginas/audit.json.

Nuevos documentos localizados en páginas oficiales:

| Documento | Enlace | Uso previsto |
|---|---|---|
| Managed Futures Research Digest | https://www.cmegroup.com/education/files/research-digest.pdf | Compendio de resúmenes: localizar después los estudios originales y deduplicarlos |
| Options on Futures as Strategic Investment Vehicles | https://www.cmegroup.com/education/files/options-on-futures-as-strategic-investment-vehicles.pdf | Informe: revisar metodología y evidencia |
| 25 Proven Strategies | https://www.cmegroup.com/articles/files/2022/25-proven-strategies.pdf | Guía educativa; el título no demuestra rentabilidad empírica |

Siguiente ampliación: examinar las doce páginas iniciales cuando su acceso esté disponible y buscar informes por producto (índices, tasas, divisas, energía, metales y agricultura), spreads, carry, momentum y volatilidad. Conservar artículos HTML cuando no exista PDF original, indicando su formato. Separar evidencia empírica, teoría y material educativo durante la revisión.

## SSRN

Hay 59 referencias iniciales; 49 se resolvieron en OpenAlex. Es una resolución de metadatos, no una descarga de 49 PDFs. Se completaron seis consultas específicas dentro de la fuente SSRN Electronic Journal de OpenAlex (S4210172589): 4.624 coincidencias sumadas y 4.344 identificadores OpenAlex distintos. El inventario integrado alcanzó 12.409 candidatos tras descontar coincidencias con la colección anterior. La pertinencia es provisional. El detalle está en descargas/ssrn_expansion_audit.json y descargas/openalex_ssrn_manifest.json; las consultas están en consultas_ssrn.json. Los registros conservan sus ubicaciones y procedencia; su asociación con SSRN no significa que se haya descargado desde ese dominio.

El usuario autorizó un nuevo intento de navegador en esta conversación. La herramienta volvió a rechazar papers.ssrn.com por un permiso guardado o una política administrada. La autorización en el chat no cambió esa configuración. No se ha confirmado una ruta concreta de interfaz para modificarla.

Para avanzar en acceso directo debe habilitarse ese dominio en los permisos del navegador de la aplicación, si la configuración lo permite; una política administrada requeriría intervención de su administrador. Después se podrá comprobar una ficha y un PDF, y solo entonces ampliar la descarga con registro de resultados. No sustituir el acceso rechazado por solicitudes Python u otro navegador.

Mientras tanto, continuar la identificación bibliográfica en OpenAlex: DOI, versiones, referencias y citantes. Cada referencia pendiente debe conservar su causa. Una cuenta SSRN no resuelve por sí sola el bloqueo del navegador.

Documentación oficial sobre cuentas: https://www.elsevier.support/ssrn/answer/free-account
