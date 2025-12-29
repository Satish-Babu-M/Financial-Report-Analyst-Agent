import faiss
import numpy as np
import pickle
from pathlib import Path
from sentence_transformers import SentenceTransformer
from config import settings
import logging

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        self.index_path = settings.VECTOR_INDEX_PATH
        self.metadata_path = self.index_path.with_suffix(".meta.pkl")
        
        # Initialize Embedding Model
        logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)
        self.dimension = self.model.get_sentence_embedding_dimension()
        
        # Load or Create Index
        if self.index_path.exists():
            self.index = faiss.read_index(str(self.index_path))
            with open(self.metadata_path, 'rb') as f:
                self.metadata = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = [] # List of dicts mapping index ID to {doc_id, chunk_id, content}

    def add_texts(self, texts: list, Metadatas: list):
        """
        Embeds texts and adds them to the index.
        """
        if not texts:
            return
            
        embeddings = self.model.encode(texts)
        self.index.add(np.array(embeddings).astype('float32'))
        
        # Keep track of metadata
        self.metadata.extend(Metadatas)
        
        self.save()
        logger.info(f"Added {len(texts)} vectors to index.")

    def search(self, query: str, k: int = 3, filter_doc_id: str = None):
        """
        Semantic search.
        """
        query_vector = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_vector).astype('float32'), k * 2) # Fetch more to filter
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx == -1: continue
            
            meta = self.metadata[idx]
            
            # Simple client-side filtering (FAISS IDMap is better for prod, but this is fine for local)
            if filter_doc_id and meta.get('doc_id') != filter_doc_id:
                continue
                
            results.append({
                "content": meta.get("content"),
                "score": float(distances[0][i]),
                "metadata": meta
            })
            
            if len(results) >= k:
                break
                
        return results

    def save(self):
        faiss.write_index(self.index, str(self.index_path))
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(self.metadata, f)
