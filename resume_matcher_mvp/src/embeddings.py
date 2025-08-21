from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Union
import os

class EmbeddingEngine:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize sentence transformer model."""
        self.model_name = model_name
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        print(f"Model loaded successfully. Embedding dimension: {self.model.get_sentence_embedding_dimension()}")
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding vector for input text."""
        if not text or text.strip() == "":
            raise ValueError("Empty text provided for embedding")
        
        # Generate embedding
        embedding = self.model.encode([text])[0]
        
        # Normalize for cosine similarity
        embedding = embedding / np.linalg.norm(embedding)
        
        return embedding.tolist()
    
    def generate_batch_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts efficiently."""
        if not texts:
            return []
        
        # Filter empty texts
        valid_texts = [text for text in texts if text and text.strip()]
        if not valid_texts:
            raise ValueError("No valid texts provided")
        
        # Generate embeddings in batch
        embeddings = self.model.encode(valid_texts)
        
        # Normalize each embedding
        normalized_embeddings = []
        for embedding in embeddings:
            norm_embedding = embedding / np.linalg.norm(embedding)
            normalized_embeddings.append(norm_embedding.tolist())
        
        return normalized_embeddings
    
    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings."""
        # Convert to numpy arrays
        emb1 = np.array(embedding1)
        emb2 = np.array(embedding2)
        
        # Calculate cosine similarity (dot product of normalized vectors)
        similarity = np.dot(emb1, emb2)
        
        # Ensure similarity is between 0 and 1
        return max(0.0, min(1.0, float(similarity)))

# Example usage
if __name__ == "__main__":
    engine = EmbeddingEngine()
    
    # Test embedding generation
    sample_text = "Python developer with 5 years experience in machine learning"
    embedding = engine.generate_embedding(sample_text)
    print(f"Generated embedding with {len(embedding)} dimensions")
