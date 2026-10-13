# ADR 001 Uso de RAG para el laboratorio TSI

## Estado

Aceptado para el laboratorio. La ruta local con `hash` y generacion extractiva es la referencia reproducible; Azure AI Search queda como validacion de infraestructura cuando exista una suscripcion habilitada.

## Contexto

El proyecto debe responder preguntas sobre un corpus acotado, mostrar las fuentes recuperadas, abstenerse cuando no existe evidencia y permitir comparar recuperacion lexical, vectorial e hibrida. Un LLM aislado no garantiza que la respuesta este fundamentada en los documentos del laboratorio.

## Alternativas

1. Sin LLM: determinista, pero no cubre el flujo RAG solicitado.
2. LLM sin RAG: puede responder con conocimiento externo o inventar informacion.
3. RAG: recupera chunks, construye contexto no confiable, responde y expone fuentes.
4. Agente con herramientas: aporta mas capacidad, pero introduce complejidad y superficie de riesgo que no es necesaria para este laboratorio.

## Evidencia

- Golden set: `tests/golden_set.json`, con diez preguntas respondibles y dos casos sin evidencia.
- Hit@K: se calcula para `keyword`, `vector` e `hybrid` mediante `scripts/evaluate_golden_set.py`.
- Latencia: se mide en retrieval, generacion y total, y se registra en `logs/queries.jsonl`.
- Seguridad: `tests/test_security.py` verifica deteccion de prompt injection y marcado `DOCUMENTO NO CONFIABLE`.
- Coste: la ruta local no consume Azure; la ruta cloud debe usar Azure AI Search Free.

## Decision

Mantener una arquitectura desacoplada con `Retriever`, `Embedder` y `Generator`. El backend local permite validar el repositorio sin red ni servicios externos. Azure AI Search se integra por REST y conserva la misma interfaz de busqueda. Los documentos recuperados se tratan siempre como datos no confiables y nunca como instrucciones.

## Consecuencias

- El laboratorio es ejecutable y evaluable localmente.
- La calidad semantica del modo `hash` es didactica, no equivalente a un embedding de produccion.
- Cambiar el modelo de embeddings exige recrear el indice y reindexar.
- La generacion extractiva no sustituye una evaluacion de groundedness de un LLM real.
- Azure, Ollama y Playwright requieren servicios o dependencias externos y deben quedar respaldados por su salida real.

## Condicion para revertir la decision

Revisar esta decision si el corpus supera las capacidades del almacenamiento local, si la latencia local incumple el objetivo acordado o si el conjunto de evaluacion demuestra que la recuperacion no alcanza el umbral definido por el equipo.
