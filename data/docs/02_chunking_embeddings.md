# Chunking y embeddings

El chunking divide documentos en fragmentos que puedan recuperarse de forma independiente. Fragmentos demasiado grandes pueden mezclar temas y desperdiciar contexto. Fragmentos demasiado pequenos pueden perder relaciones necesarias para responder. El tamano debe evaluarse con preguntas reales y no elegirse solo por costumbre.

El overlap conserva una pequena zona compartida entre chunks consecutivos para reducir cortes abruptos de informacion. Un overlap excesivo aumenta almacenamiento y repeticion de resultados. En este laboratorio se comparan al menos dos configuraciones de chunk_size y se registra su efecto en Hit@K y latencia.

Un embedding convierte texto en un vector numerico. Vectores de textos similares tienden a quedar cercanos bajo una metrica como cosine similarity cuando se usa un modelo semantico apropiado. El starter incluye un embedding hash determinista para evitar bloqueos de instalacion o cuota; sirve para ejercitar el flujo tecnico, pero no reemplaza un modelo semantico en una evaluacion real.

Si se cambia el modelo de embeddings o cambia la dimension del vector, el indice debe recrearse y el corpus debe volver a indexarse. Mezclar vectores generados por modelos diferentes invalida la comparacion.
