from tsi_rag.azure_search import AzureSearchClient
from tsi_rag.chunking import load_corpus
from tsi_rag.config import Settings
from tsi_rag.embeddings import get_embedder


settings = Settings()
embedder = get_embedder(settings)
chunks = load_corpus(settings.corpus_dir, settings.chunk_size, settings.chunk_overlap)
vectors = embedder.embed_many([c.content for c in chunks])
for chunk, vector in zip(chunks, vectors, strict=True):
    chunk.vector = vector

client = AzureSearchClient(settings)
count = client.upload_chunks(chunks)
print(f"Chunks cargados: {count}")
