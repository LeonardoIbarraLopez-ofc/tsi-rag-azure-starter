# Despliegue y observabilidad minima

Un MVP defendible debe ser reproducible. El repositorio debe contener dependencias, variables documentadas, comandos de arranque y, cuando corresponda, Dockerfile. La configuracion sensible se inyecta por variables de entorno y nunca se incluye en la imagen ni en el repositorio.

La observabilidad minima de una consulta RAG registra identificador temporal, consulta, modo de retrieval, fuentes recuperadas, latencia de recuperacion, latencia de generacion, latencia total, generador utilizado y alertas de seguridad. Si el proveedor informa tokens o costo, se pueden agregar esos campos.

Los logs deben permitir diagnosticar por que una respuesta fue mala sin guardar informacion sensible innecesaria. En un entorno real se recomienda correlation ID para seguir una solicitud entre UI, API, retrieval y generacion.

Antes de una demostracion se ejecuta un smoke test: `/health`, una consulta conocida, una consulta sin evidencia y los tests principales. El equipo debe preparar un plan B de demostracion que documente fallas sin ocultarlas.
