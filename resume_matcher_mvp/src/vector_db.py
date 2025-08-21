from typing import List, Dict, Optional
import json
import uuid

# Optional chroma import; provide in-memory fallback if unavailable
try:
    import chromadb
    from chromadb.config import Settings
    _CHROMA_AVAILABLE = True
except Exception:
    chromadb = None  # type: ignore
    Settings = None  # type: ignore
    _CHROMA_AVAILABLE = False
import math
import numpy as np

class VectorDatabase:
    def __init__(self, collection_name: str = "resumes"):
        """Initialize vector storage. Use Chroma if available, otherwise fallback to in-memory store."""
        self.collection_name = collection_name
        self._use_chroma = _CHROMA_AVAILABLE
        if self._use_chroma:
            try:
                self.client = chromadb.Client(Settings(
                    chroma_db_impl="duckdb+parquet",
                    persist_directory=None,  # In-memory
                ))
                try:
                    self.collection = self.client.get_collection(name=collection_name)
                    print(f"Loaded existing collection: {collection_name}")
                except Exception:
                    self.collection = self.client.create_collection(
                        name=collection_name,
                        metadata={"hnsw:space": "cosine"}
                    )
                    print(f"Created new collection: {collection_name}")
            except Exception as e:
                print(f"Chroma initialization failed, using fallback store. Error: {e}")
                self._use_chroma = False
        if not self._use_chroma:
            # Fallback in-memory store
            self._items: List[Dict] = []
    
    def store_resume(self, filename: str, embedding: List[float], text_content: str, metadata: Optional[Dict] = None) -> str:
        """Store resume embedding with metadata."""
        # Generate unique ID
        resume_id = str(uuid.uuid4())
        
        # Prepare metadata
        if metadata is None:
            metadata = {}
        
        metadata.update({
            "filename": filename,
            "content_length": len(text_content),
            "type": "resume"
        })
        
        if self._use_chroma:
            self.collection.add(
                embeddings=[embedding],
                documents=[text_content[:1000]],  # Store first 1000 chars as document
                metadatas=[metadata],
                ids=[resume_id]
            )
        else:
            self._items.append({
                "id": resume_id,
                "embedding": np.array(embedding, dtype=float),
                "document": text_content[:1000],
                "metadata": metadata,
            })
        print(f"Stored resume: {filename} with ID: {resume_id}")
        return resume_id
    
    def search_similar(self, query_embedding: List[float], top_k: int = 10, min_similarity: float = 0.0, where: Optional[Dict] = None) -> List[Dict]:
        """Find most similar resumes using vector search."""
        try:
            if self._use_chroma:
                # Query the collection
                kwargs = {
                    "query_embeddings": [query_embedding],
                    "n_results": min(top_k, self.collection.count()),
                }
                if where:
                    kwargs["where"] = where
                results = self.collection.query(**kwargs)
                matches: List[Dict] = []
                if results['distances'] and len(results['distances'][0]) > 0:
                    for i in range(len(results['distances'][0])):
                        distance = results['distances'][0][i]
                        similarity = 1 - distance
                        if similarity >= min_similarity:
                            match = {
                                "id": results['ids'][0][i],
                                "similarity": round(similarity, 4),
                                "filename": results['metadatas'][0][i].get('filename', 'Unknown'),
                                "content_preview": results['documents'][0][i][:200] + "...",
                                "metadata": results['metadatas'][0][i]
                            }
                            matches.append(match)
                return matches
            else:
                q = np.array(query_embedding, dtype=float)
                # Normalize
                q_norm = q / (np.linalg.norm(q) + 1e-12)
                results_local: List[Tuple[str, float, Dict, str]] = []
                for it in self._items:
                    if where:
                        ok = True
                        for k, v in where.items():
                            if it["metadata"].get(k) != v:
                                ok = False
                                break
                        if not ok:
                            continue
                    emb = it["embedding"]
                    emb_norm = emb / (np.linalg.norm(emb) + 1e-12)
                    sim = float(np.dot(q_norm, emb_norm))
                    if sim >= min_similarity:
                        results_local.append((it["id"], sim, it["metadata"], it["document"]))
                # Sort by similarity desc
                results_local.sort(key=lambda x: x[1], reverse=True)
                results_local = results_local[:top_k]
                out: List[Dict] = []
                for rid, sim, md, doc in results_local:
                    out.append({
                        "id": rid,
                        "similarity": round(sim, 4),
                        "filename": md.get("filename", "Unknown"),
                        "content_preview": (doc or "")[:200] + "...",
                        "metadata": md,
                    })
                return out
        
        except Exception as e:
            print(f"Search error: {str(e)}")
            return []
    
    def get_collection_stats(self) -> Dict:
        """Get statistics about the collection."""
        try:
            count = self.collection.count() if self._use_chroma else len(self._items)
            return {
                "total_resumes": count,
                "collection_name": self.collection_name
            }
        except Exception as e:
            print(f"Stats error: {str(e)}")
            return {"total_resumes": 0, "collection_name": self.collection_name}
    
    def clear_collection(self):
        """Clear all data from collection."""
        try:
            if self._use_chroma:
                self.client.delete_collection(name=self.collection_name)
                self.collection = self.client.create_collection(
                    name=self.collection_name,
                    metadata={"hnsw:space": "cosine"}
                )
            else:
                self._items.clear()
            print("Collection cleared successfully")
        except Exception as e:
            print(f"Clear error: {str(e)}")

# Example usage
if __name__ == "__main__":
    db = VectorDatabase()
    print("Vector database initialized")
