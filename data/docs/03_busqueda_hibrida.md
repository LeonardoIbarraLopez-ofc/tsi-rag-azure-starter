# Busqueda keyword, vectorial e hibrida

La busqueda de texto completo favorece coincidencias lexicas y terminos concretos. Es muy util cuando la consulta contiene nombres, identificadores, comandos o palabras que aparecen literalmente en los documentos.

La busqueda vectorial compara el embedding de la consulta con los embeddings de los chunks. Con un modelo semantico adecuado puede recuperar fragmentos relacionados aunque no compartan exactamente las mismas palabras.

La busqueda hibrida ejecuta busqueda textual y vectorial en una misma consulta y combina sus rankings. En Azure AI Search, una consulta hibrida puede incluir simultaneamente el parametro search y vectorQueries. El servicio fusiona los resultados en un ranking unificado usando Reciprocal Rank Fusion (RRF).

No debe asumirse que hybrid siempre gana. El laboratorio exige comparar keyword, vector y hybrid sobre un golden set. La decision debe apoyarse en Hit@K, calidad de respuesta, latencia y caracteristicas del corpus.
