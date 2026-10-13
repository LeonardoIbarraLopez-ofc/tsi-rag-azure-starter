from tsi_rag.azure_search import AzureSearchClient
from tsi_rag.config import Settings


settings = Settings()
client = AzureSearchClient(settings)
print("Conexion Azure AI Search: OK")
print("Indices:", client.list_indexes())
