# Fundamentos de RAG

Retrieval-Augmented Generation (RAG) combina una etapa de recuperacion con una etapa de generacion. La aplicacion no debe enviar al modelo todo el repositorio documental. Primero formula una consulta, recupera fragmentos relevantes y entrega solo ese contexto al generador. La respuesta debe conservar trazabilidad hacia las fuentes recuperadas.

RAG esta justificado cuando la respuesta depende de conocimiento externo al modelo, documentacion propia, informacion que cambia o contenido que debe ser citado. Un LLM aislado puede ser suficiente cuando la tarea es puramente generativa y no necesita hechos privados ni evidencia documental. Una solucion sin LLM puede ser mejor cuando reglas, busqueda tradicional o una consulta estructurada resuelven el problema con menor costo y riesgo.

Un RAG minimo viable necesita: corpus controlado, estrategia de chunking, embeddings, indice o vector store, recuperacion top-k, prompt que delimite el contexto, generador y una forma de mostrar fuentes. Antes de optimizar prompts debe existir un golden set para evitar ajustar a impresiones subjetivas.

La arquitectura debe permitir comparar alternativas. Si un equipo incorpora RAG, debe registrar la decision en un ADR: necesidad, alternativas, evidencia, costos, riesgos y condicion de salida. El objetivo no es agregar IA generativa por moda sino demostrar valor frente a una solucion mas simple.
