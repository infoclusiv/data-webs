# Data Webs — Investigación de trading

Proyecto, datos recolectados y documentos de investigación sobre opciones y futuros.

El contenido se conserva en `investigacion_trading/`. Consultar `investigacion_trading/PARA_EL_AGENTE.md`, `investigacion_trading/PROGRESO.md` y `investigacion_trading/corpus/ESTADO.md` para conocer el alcance y estado de la investigación.

## Descargar el proyecto completo

Los directorios `corpus/` y `descargas/` se almacenan mediante Git LFS. Instalar Git LFS antes de clonar:

```sh
git lfs install
git clone https://github.com/infoclusiv/data-webs.git
cd data-webs
git lfs pull
```

Si se descarga un ZIP desde GitHub, puede contener punteros LFS en lugar de los datos. Para obtener los documentos completos se recomienda clonar y ejecutar `git lfs pull`.

## Configuración local

Copiar `investigacion_trading/.env.example` a `investigacion_trading/.env` y configurar las credenciales localmente. `.env` queda excluido de Git. No incluir credenciales en código ni documentos.

Se incluyen los datos, documentos, registros y archivos temporales de investigación. Se excluyen credenciales, cachés de Python y bloqueos de procesos.
