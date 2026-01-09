from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

class DocumentStore:
    
    def __init__(self, use_qdrant: bool = False):
        self.use_qdrant = use_qdrant
        self.in_memory_docs = []
        
        if use_qdrant:
            try:
                self.client = QdrantClient("http://localhost:6333")
                self.client.recreate_collection(
                    collection_name="demo_collection",
                    vectors_config=VectorParams(size=128, distance=Distance.COSINE)
                )
            except Exception:
                self.use_qdrant = False
                print("⚠️ Qdrant not available, using in-memory storage")
    
    def add_document(self, text: str, embedding: list) -> int:
        doc_id = len(self.in_memory_docs)  
        
        if self.use_qdrant:
            self.client.upsert(
                collection_name="demo_collection",
                points=[PointStruct(id=doc_id, vector=embedding, payload={"text": text})]
            )
        else:
            self.in_memory_docs.append(text)
        
        return doc_id  
    
    def search(self, query_embedding: list, query_text: str = "") -> list:
        if self.use_qdrant:
            hits = self.client.search(
                collection_name="demo_collection", 
                query_vector=query_embedding, 
                limit=2
            )
            return [hit.payload["text"] for hit in hits]
        else:
            results = []
            for doc in self.in_memory_docs:
                if query_text.lower() in doc.lower():
                    results.append(doc)
            if not results and self.in_memory_docs:
                results = [self.in_memory_docs[0]]
            return results
    
    def get_doc_count(self) -> int:
        return len(self.in_memory_docs)
    
    def is_qdrant_ready(self) -> bool:
        return self.use_qdrant