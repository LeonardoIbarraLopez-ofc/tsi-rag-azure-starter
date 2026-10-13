# Arquitectura del laboratorio

```text
Documentos -> chunking -> embeddings -> Azure AI Search
                                      ^
Pregunta -> embedding ----------------|
             | keyword + vector -> top-k -> contexto no confiable -> generador
                                                          |
                                                          v
                                                   FastAPI -> UI
                                                          |
                                                          v
                                                   pytest / E2E
```

## Decisiones intencionales

- Azure AI Search es el componente cloud obligatorio del camino Azure.
- `hash` es un embedding didactico de cero descargas para evitar bloqueos de cuota.
- `sentence_transformers` es la ruta recomendada para semantica local real.
- Azure OpenAI y Ollama son generadores opcionales.
- `extractive` es un fallback de laboratorio para validar recuperacion, API y pruebas cuando no existe acceso a un LLM.
