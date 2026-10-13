# Registro de experimentos RAG

La regla aplicada es cambiar una sola variable por experimento y conservar el golden set sin modificar durante la comparacion.

| Fecha | Cambio | Hipotesis | Metrica | Resultado | Decision |
|---|---|---|---|---|---|
| 2026-10-12 | Baseline local `chunk_size=900`, `overlap=120` | Un chunk de tamano medio conserva contexto suficiente | Hit@5, latencia total | Ejecutar `uv run python scripts/evaluate_golden_set.py` y conservar CSV/JSON en `reports/` | Baseline de referencia |
| 2026-10-12 | Comparacion `keyword`, `vector`, `hybrid` | Hybrid puede combinar coincidencia lexical y similitud | Hit@5 por modo, abstencion G11/G12 | El script genera una fila por pregunta y modo y un resumen por modo | No declarar ganador sin leer el reporte |
| 2026-10-12 | Abstencion ante preguntas fuera del corpus | Sin solapamiento lexical el sistema debe negarse | `no_answer_ok` en G11 y G12 | Cubierto por `test_unknown_question_returns_no_evidence_message` | Mantener umbral y respuesta fija |
| 2026-10-12 | Documento adversario | El contenido hostil debe ser detectado y encapsulado como dato | Flags de seguridad y tests | Cubierto por `tests/test_security.py` | Mantener aislamiento del contexto |
| Pendiente | `sentence_transformers` | Embeddings semanticos pueden mejorar paraphrases | Hit@5 y latencia contra baseline | Requiere `uv sync --extra dev --extra semantic` y reindexacion | Ejecutar solo si hay red/paquetes |

## Criterio de decision

Elegir el modo que ofrezca el mejor equilibrio entre Hit@5, abstencion correcta y latencia. Una mejora de ranking no justifica bajar la capacidad de abstenerse ni elevar el coste sin evidencia.
