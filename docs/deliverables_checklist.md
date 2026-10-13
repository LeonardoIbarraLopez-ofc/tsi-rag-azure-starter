# Checklist de entrega

- [x] `.env` esta excluido por `.gitignore`; nunca se debe versionar.
- [ ] Azure AI Search Free creado; si no hay credenciales, usar `docs/azure_route_status.md` como evidencia del bloqueo.
- [ ] Indice creado con campo vectorial; ejecutar la ruta Azure antes de marcarlo.
- [x] Corpus versionado en `data/docs/`.
- [x] Golden set versionado en `tests/golden_set.json` antes de optimizar.
- [x] Comparacion `keyword`, `vector` e `hybrid` implementada en `scripts/evaluate_golden_set.py`.
- [ ] Hit@K medido; el reporte se genera con `uv run python scripts/evaluate_golden_set.py`.
- [x] Caso sin evidencia cubierto por G11/G12 y pruebas automatizadas.
- [x] Documento malicioso cubierto por `tests/test_security.py` y `security_cases.json`.
- [x] API `/health`, `/search`, `/ask` implementada.
- [ ] Tests pytest verdes; ejecutar en un entorno con dependencias disponibles.
- [ ] Prueba E2E ejecutada cuando Chromium y el servidor esten disponibles.
- [x] Logs de latencia implementados en `logs/queries.jsonl` y excluidos de Git.
- [x] ADR RAG actualizado en `docs/adr_rag.md`.
- [x] Experiment Log actualizado en `docs/experiment_log.md`.
- [x] Matriz de evidencias y comandos de entrega en `docs/evidence_plan.md`.
