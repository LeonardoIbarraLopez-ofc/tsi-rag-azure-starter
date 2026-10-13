# Plan de evidencias para la entrega

## Evidencias que deben tomarse

| ID | Evidencia | Comando o pantalla | Resultado que debe verse |
|---|---|---|---|
| E01 | Preflight local | `uv run pytest` | Tests verdes y E2E omitido si no se define `E2E_BASE_URL` |
| E02 | API | Servidor + `GET /health`, `POST /search`, `POST /ask` | Proveedores, hits, respuesta, fuentes y latencias |
| E03 | Golden set | `uv run python scripts/evaluate_golden_set.py` | CSV/JSON con `keyword`, `vector`, `hybrid`, Hit@5 y abstencion |
| E04 | Sin evidencia | G11 y G12 desde API o UI | `No encuentro esa informacion en las fuentes disponibles.` y cero fuentes |
| E05 | Seguridad | `uv run pytest tests/test_security.py -vv` | Deteccion de `ignore_previous` y contexto no confiable |
| E06 | Observabilidad | `logs/queries.jsonl` despues de `/ask` | Consulta, modo, fuentes, flags y latencias; sin secretos |
| E07 | Azure | `azure_preflight.py`, indice y carga | Conexion OK, indice `tsi-rag-lab` y chunks cargados; clave oculta |
| E08 | E2E | `E2E_BASE_URL=... uv run pytest tests/e2e/test_ui.py -vv` | Flujo visible con respuesta y fuentes |
| E09 | Docker | `docker build` y `docker run` | Imagen construida, `/health` responde y consulta funciona |

## Comandos de ejecucion

```powershell
$env:UV_CACHE_DIR = Join-Path (Get-Location) '.uv-cache'
uv sync --extra dev
uv run pytest -vv
uv run python scripts/evaluate_golden_set.py
uv run uvicorn tsi_rag.api:app --host 127.0.0.1 --port 8000
```

Para E2E, instalar Chromium una vez con `uv run playwright install chromium`, mantener el servidor activo y ejecutar la prueba en una segunda terminal.

## Criterio de aceptacion

No se debe editar un reporte para mejorar resultados. Cada captura debe incluir el comando o URL, fecha visible cuando sea posible y configuracion sin secretos. Los resultados Azure y Docker solo se marcan como ejecutados despues de observar su salida real.
