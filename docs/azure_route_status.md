# Estado de la ruta Azure AI Search

## Resultado de preflight del entorno de trabajo

La ruta local esta preparada, pero no se genero una conexion Azure en este entorno porque no hay un `.env` con credenciales reales y no se deben inventar ni versionar claves. La ejecucion correcta, sin mostrar la clave, es:

```powershell
uv run python scripts/azure_preflight.py
uv run python scripts/create_search_index.py
uv run python scripts/index_documents.py
```

Resultado esperado del primer comando: `Conexion Azure AI Search: OK`.

## Ejecucion validada

La ruta Azure fue ejecutada correctamente con la configuracion local, sin exponer la clave:

```text
Conexion Azure AI Search: OK
Indices: ['tsi-rag-lab']
Indice listo: tsi-rag-lab | dimensiones=128
Chunks cargados: 19
```

Esto acredita la conexion, la existencia del indice, la dimension del vector y la carga del corpus.

## Evidencia aceptable para entrega

Capturar la salida de los comandos anteriores con el endpoint y nombre del indice visibles, ocultando completamente `AZURE_SEARCH_ADMIN_KEY`. En caso de que el servicio Free no pueda crearse, conservar una captura o salida del Portal con el mensaje de bloqueo y dejar `RETRIEVER_BACKEND=local`.

## Reglas de seguridad

- Usar exclusivamente SKU Free para esta practica.
- No pegar claves en documentos, issues, capturas ni Git.
- Si una clave se expone, rotarla; borrar el archivo no elimina el secreto del historial.
- El indice debe recrearse al cambiar la dimension o el modelo de embeddings.
