# Seguridad de RAG y prompt injection

Los documentos recuperados no son instrucciones confiables. Un atacante puede insertar texto que intente modificar el comportamiento del modelo, pedir que ignore reglas previas, revelar secretos o ejecutar herramientas. Este riesgo se conoce como indirect prompt injection cuando la instruccion maliciosa llega por contenido externo recuperado.

Una defensa basica separa claramente instrucciones de sistema y datos recuperados. El prompt debe marcar el contexto como no confiable y ordenar al modelo tratarlo solo como evidencia. Las aplicaciones no deben colocar secretos en el contexto ni permitir que una respuesta del modelo cambie permisos.

Si existen herramientas, cada tool debe aplicar autorizacion fuera del LLM, validar argumentos, limitar acciones y registrar auditoria. El principio de minimo privilegio es obligatorio: el modelo no recibe permisos que no necesita. Operaciones irreversibles pueden requerir aprobacion humana.

La evaluacion de seguridad debe contener documentos maliciosos, solicitudes de exfiltracion, instrucciones contradictorias y respuestas sin evidencia. El resultado esperado no es que el modelo "parezca seguro", sino contar con pruebas reproducibles que demuestren el comportamiento observado y sus limitaciones.
