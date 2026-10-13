# Gestion de secretos

Las claves de Azure AI Search, tokens y credenciales no deben almacenarse en Git, archivos Markdown, notebooks ni capturas compartidas. Para desarrollo local se utiliza un archivo `.env` excluido mediante `.gitignore`, acompañado de `.env.example` sin valores reales.

Los secretos deben limitarse al alcance minimo necesario. Una clave administrativa de Azure AI Search permite operaciones de escritura y administracion; no debe distribuirse a un frontend. Las aplicaciones cliente no deben recibir una admin key. En despliegues reales se prefieren identidades administradas y RBAC cuando el servicio y arquitectura lo permiten.

Si una clave se expone, debe considerarse comprometida: rotarla, actualizar el secreto en el entorno y revisar los logs. No basta con borrar el commit porque el secreto puede seguir en el historial.

La defensa del proyecto debe demostrar que las credenciales se gestionan por configuracion externa. El README debe explicar como crear `.env` desde `.env.example` sin incluir valores reales.
