from tsi_rag.azure_search import AzureSearchClient
from tsi_rag.config import Settings
from tsi_rag.embeddings import get_embedder


settings = Settings()
embedder = get_embedder(settings)
client = AzureSearchClient(settings)
result = client.create_or_update_index(embedder.dimensions)
print(f"Indice listo: {result.get('name')} | dimensiones={embedder.dimensions}")
