from pathlib import Path
from .embedding_service import EmbeddingSearcher
from typing import List

class RAGService:
    def __init__(self):
        # Use absolute path
        base_dir = Path(__file__).resolve().parent.parent.parent
        embeddings_dir = base_dir / 'embeddings_output'
        self.searcher = EmbeddingSearcher(embeddings_dir)
    
    def get_relevant_context(self, query: str, top_k: int = 5) -> str:
        results = self.searcher.search(query, top_k=top_k)
        context = "\n".join([r['text'] for r in results])
        return context