from sentence_transformers import SentenceTransformer
from langchain.schema import Document
from pathlib import Path
import faiss
import pickle
import numpy as np


def load_chunks(file_path: Path) -> list[Document]:
    with open(file_path, "rb") as f:
        chunks_data = pickle.load(f)

    if isinstance(chunks_data[0], dict):
        return [Document(page_content=ch["text"], metadata=ch["metadata"]) for ch in chunks_data]
    return chunks_data


class ContextLookup:
    def __init__(self, root: str | Path):
        root = Path(root)
        self.index = faiss.read_index(str(root / "book.index"))
        self.chunks = load_chunks(root / "book_chunks.pkl")
        self.model = SentenceTransformer("intfloat/multilingual-e5-large")
        self.k = 30
        self.threshold = 0.65

    def lookup(self, query):
        query_embedding = self.model.encode(query, normalize_embeddings=True)
        query_embedding = np.expand_dims(query_embedding, axis=0).astype(np.float32)
        scores, indices = self.index.search(query_embedding, self.k)

        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if score >= self.threshold:
                doc = self.chunks[idx]
                results.append({
                    "rank": i+1,
                    "score": float(score),
                    "text": doc.page_content,
                    "source": doc.metadata['source'],
                    "idx": idx,
                })
        results.sort(key=lambda x: x['idx'])
        return results
