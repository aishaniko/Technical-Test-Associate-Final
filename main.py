from fastapi import FastAPI
from services.embedding_service import EmbeddingService
from services.document_store import DocumentStore
from services.rag_service import RAGService
from api.routes import router, setup_services

# Initialize services
embedding_service = EmbeddingService()
document_store = DocumentStore(use_qdrant=False)
rag_service = RAGService(embedding_service, document_store)

# Setup services in routes
setup_services(embedding_service, document_store, rag_service)

# Create FastAPI app
app = FastAPI(title="Refactored RAG Demo")

# Include router
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)