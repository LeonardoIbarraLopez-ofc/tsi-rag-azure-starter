from tsi_rag.chunking import chunk_text


def test_chunking_respects_size_and_overlap():
    text = ("Parrafo de prueba con informacion util. " * 80).strip()
    chunks = chunk_text(text, chunk_size=300, overlap=50)
    assert len(chunks) > 1
    assert all(len(c) <= 300 for c in chunks)


def test_overlap_must_be_smaller_than_chunk_size():
    try:
        chunk_text("texto", chunk_size=100, overlap=100)
    except ValueError:
        return
    raise AssertionError("Debio lanzar ValueError")
