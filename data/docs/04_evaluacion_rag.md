# Evaluacion de RAG

El golden set es una coleccion versionada de preguntas y expectativas creada antes de optimizar prompts o parametros. Para cada pregunta puede indicar la fuente esperada, respuesta esperada, fragmentos relevantes o que el sistema deberia declarar falta de evidencia.

Hit@K pregunta si una fuente relevante aparece dentro de los primeros K resultados. Si ocho de diez preguntas recuperan la fuente esperada dentro del top 5, Hit@5 es 80 por ciento. Recall@K puede utilizarse cuando existen varias fuentes relevantes para una misma consulta. Estas metricas evalúan recuperacion, no la calidad total de la respuesta.

La generacion debe evaluarse tambien por groundedness o fidelidad: las afirmaciones importantes deben estar respaldadas por el contexto recuperado. Un sistema que produce respuestas fluidas pero agrega hechos no presentes en el contexto falla el objetivo de RAG.

La suite debe incluir preguntas conocidas, preguntas sin evidencia, variaciones de redaccion, fallas de dependencias y casos adversarios. Registrar latencia de recuperacion, latencia de generacion y latencia total permite detectar regresiones de rendimiento. Si existe un proveedor de pago, tambien se deben registrar tokens y costo estimado.
