# Incidentes y rollback

Cuando una liberacion falla, el equipo debe priorizar recuperar el servicio antes de experimentar cambios adicionales. El procedimiento basico consiste en confirmar el impacto, detener despliegues nuevos, identificar la ultima version conocida como estable, ejecutar rollback y realizar un smoke test.

Despues del rollback se verifica salud, flujo principal, logs y metricas. Si la falla persiste, se activa el plan de contingencia y se documentan responsables, tiempos y evidencia. No se deben borrar logs antes de completar el diagnostico.

El postmortem breve describe que ocurrio, impacto, linea de tiempo, causa probable, controles que funcionaron o fallaron y acciones preventivas. Su objetivo es aprendizaje y mejora, no asignacion de culpa.

Una estrategia de liberacion reproducible utiliza tags o identificadores de version. El runbook debe explicar como desplegar, verificar, revertir y escalar un incidente.
