# TSI - RAG minimo viable con Azure AI Search

Starter del laboratorio integrador de las Clases 19-21 de **Taller de Sistemas Inteligentes**.

## Objetivos

Construir y demostrar un flujo:

```text
pregunta -> recuperacion -> contexto -> respuesta -> fuentes
```

que ademas pueda evaluarse, probarse ante un documento malicioso y exponerse por API/UI.

## 0. Requisitos

- Python 3.11+
- `uv`
- VS Code
- Git
- Cuenta Azure for Students activa para la ruta Azure
- Opcional: Docker
- Opcional: Ollama o un deployment Azure OpenAI para generacion real

## 1. Arranque local sin Azure

```bash
cp .env.example .env
uv sync --extra dev
uv run pytest
uv run uvicorn tsi_rag.api:app --reload
```

Abra `http://127.0.0.1:8000`.

El modo local usa:

```text
RETRIEVER_BACKEND=local
EMBEDDING_PROVIDER=hash
GENERATOR_PROVIDER=extractive
```

Esto valida repositorio, corpus, chunking, retrieval, seguridad, API, UI y tests sin consumir Azure.

## 2. Ruta recomendada con Azure AI Search

1. Cree un **Azure AI Search** con SKU **Free**.
2. Copie endpoint y admin key en `.env`.
3. Seleccione embeddings:
   - `hash`: cero descargas, didactico.
   - `sentence_transformers`: semantica local recomendada.
   - `azure_openai`: si su suscripcion permite un deployment de embeddings.
4. Cree el indice y cargue el corpus.

```bash
RETRIEVER_BACKEND=azure
uv run python scripts/azure_preflight.py
uv run python scripts/create_search_index.py
uv run python scripts/index_documents.py
```

Edite `.env` y deje:

```text
RETRIEVER_BACKEND=azure
```

Luego:

```bash
uv run uvicorn tsi_rag.api:app --reload
```

## 3. Embeddings semanticos locales

```bash
uv sync --extra dev --extra semantic
```

En `.env`:

```text
EMBEDDING_PROVIDER=sentence_transformers
```

**Importante:** si cambia el modelo/dimension de embeddings debe recrear el indice y volver a indexar.

## 4. Generacion real

### Opcion A: Ollama

```text
GENERATOR_PROVIDER=ollama
OLLAMA_MODEL=llama3.2:3b
```

### Opcion B: Azure OpenAI

Configure las variables `AZURE_OPENAI_*` del `.env` y use:

```text
GENERATOR_PROVIDER=azure_openai
```

Si el recurso/modelo no esta habilitado en la cuenta, utilice `extractive` como plan B y documente el bloqueo.

## 5. Evaluacion

El golden set vive en `tests/golden_set.json`.

```bash
uv run python scripts/evaluate_golden_set.py
```

Genera:

```text
reports/golden_set_results.csv
reports/golden_set_results.json
```

Compare `keyword`, `vector` y `hybrid` modificando el script o usando `/search`.

## 6. Seguridad

El corpus incluye `10_documento_malicioso_demo.txt` con una instruccion deliberadamente hostil. El sistema envuelve cada chunk como **DOCUMENTO NO CONFIABLE** y registra patrones sospechosos.

Ejecute:

```bash
uv run pytest tests/test_security.py
```

No use secretos reales en los documentos ni en Git.

## 7. E2E

Instale Chromium una vez:

```bash
uv run playwright install chromium
```

En una terminal:

```bash
uv run uvicorn tsi_rag.api:app --host 127.0.0.1 --port 8000
```

En otra:

```bash
E2E_BASE_URL=http://127.0.0.1:8000 uv run pytest tests/e2e/test_ui.py
```

## 8. Docker

```bash
docker build -t tsi-rag-azure .
docker run --env-file .env -p 8000:8000 tsi-rag-azure
```

## 9. Evidencia minima del laboratorio

Consulte `docs/deliverables_checklist.md` y `docs/evidence_plan.md`. La evaluacion genera una comparacion reproducible de los tres modos de retrieval:

```bash
uv run python scripts/evaluate_golden_set.py
```

El CSV contiene una fila por pregunta y modo; el JSON agrega el resumen de Hit@K y abstencion. No se deben copiar credenciales a los reportes.

## 10. Seguridad y costos

- Use un servicio Azure AI Search Free para el corpus del laboratorio.
- No versionar `.env`.
- No pegar claves en capturas ni presentaciones.
- Si crea recursos adicionales, revise SKU, costo y elimine el Resource Group al finalizar.
- No asuma disponibilidad de Azure OpenAI: la cuenta, region y cuota pueden variar.

## 11. Estado de entrega

La arquitectura, corpus, golden set, API, UI, seguridad, logs y pruebas automatizadas estan preparados en la ruta local. La ejecucion de Azure, Docker y E2E depende de credenciales, Chromium y dependencias disponibles en el entorno; el procedimiento y la evidencia esperada estan documentados en `docs/azure_route_status.md` y `docs/evidence_plan.md`.

## Fuentes tecnicas oficiales consultadas al preparar el starter

- Azure for Students: https://azure.microsoft.com/en-us/pricing/offers/ms-azr-0170p
- Azure AI Search limits: https://learn.microsoft.com/en-us/azure/search/search-limits-quotas-capacity
- Vector Search quickstart: https://learn.microsoft.com/en-us/azure/search/search-get-started-vector
- Hybrid Search: https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview
- REST API versions: https://learn.microsoft.com/en-us/rest/api/searchservice/search-service-api-versions
