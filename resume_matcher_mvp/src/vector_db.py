import chromadb
from chromadb.config import Settings
import uuid
from typing import List, Dict, Optional
import json

class VectorDatabase:
    def __init__(self, collection_name: str = "resumes"):
        """Initialize ChromaDB client and collection."""
        self.collection_name = collection_name
        
        # Initialize ChromaDB client (in-memory for MVP)
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=None,  # In-memory
        ))
        
        # Create or get collection
        try:
            self.collection = self.client.get_collection(name=collection_name)
            print(f"Loaded existing collection: {collection_name}")
        except:
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            print(f"Created new collection: {collection_name}")
    
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
        
        # Store in ChromaDB
        self.collection.add(
            embeddings=[embedding],
            documents=[text_content[:1000]],  # Store first 1000 chars as document
            metadatas=[metadata],
            ids=[resume_id]
        )
        
        print(f"Stored resume: {filename} with ID: {resume_id}")
        return resume_id
    
    def search_similar(self, query_embedding: List[float], top_k: int = 10, min_similarity: float = 0.0) -> List[Dict]:
        """Find most similar resumes using vector search."""
        try:
            # Query the collection
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=min(top_k, self.collection.count())
            )
            
            # Format results
            matches = []
            if results['distances'] and len(results['distances'][0]) > 0:
                for i in range(len(results['distances'][0])):
                    # Convert distance to similarity (ChromaDB uses cosine distance)
                    distance = results['distances'][0][i]
                    similarity = 1 - distance  # Convert distance to similarity
                    
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
        
        except Exception as e:
            print(f"Search error: {str(e)}")
            return []
    
    def get_collection_stats(self) -> Dict:
        """Get statistics about the collection."""
        try:
            count = self.collection.count()
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
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            print("Collection cleared successfully")
        except Exception as e:
            print(f"Clear error: {str(e)}")

# Example usage
if __name__ == "__main__":
    db = VectorDatabase()
    print("Vector database initialized")
