# API, health checks e integracion E2E

La API separa la interfaz del motor RAG. El laboratorio expone `/health` para comprobar que la aplicacion responde, `/search` para observar retrieval sin generacion y `/ask` para ejecutar el flujo completo.

Un health check confirma que el proceso esta vivo. Un readiness check, cuando se implementa, debe comprobar que la aplicacion esta preparada para atender solicitudes, por ejemplo verificando configuracion y acceso a dependencias criticas. No deben confundirse: un proceso puede estar vivo pero no listo para operar.

Una prueba unitaria valida una pieza aislada. Una prueba de integracion valida la comunicacion entre componentes. Una prueba E2E recorre el flujo visible desde la interfaz hasta el resultado final. En este laboratorio, la prueba E2E abre la UI, escribe una pregunta, pulsa el boton, espera la respuesta y verifica que se muestren fuentes.

Los errores deben ser controlados. Timeouts, dependencias no disponibles, entradas invalidas y ausencia de evidencia no deben producir respuestas ambiguas. La UI debe mostrar un estado comprensible y la API debe conservar informacion suficiente para diagnosticar el fallo sin revelar secretos.
