import time
from fastapi import APIRouter, HTTPException, Depends
from models.schemas import QuestionRequest, DocumentRequest

router = APIRouter()

class APIService:
    
    def __init__(self, embedding_service, document_store, rag_service):
        self.embedding_service = embedding_service
        self.document_store = document_store
        self.rag_service = rag_service
    
    
    def get_answer(self, req: QuestionRequest):
        start = time.time()
        try:
            result = self.rag_service.ask(req.question)
            return {
                "question": req.question,
                "answer": result["answer"],
                "context_used": result.get("context", []),
                "latency_sec": round(time.time() - start, 3)
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def add_doc(self, req: DocumentRequest):
        try:
            emb = self.embedding_service.generate(req.text)
            doc_id = self.document_store.add_document(req.text, emb)
            return {"id": doc_id, "status": "added"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def get_status(self):
        return {
            "qdrant_ready": self.document_store.is_qdrant_ready(),
            "in_memory_docs_count": self.document_store.get_doc_count(),
            "graph_ready": self.rag_service.chain is not None
        }

api_service = None

def setup_services(emb_service, doc_store, rag_serv):
    """Setup services dari main.py"""
    global api_service
    api_service = APIService(emb_service, doc_store, rag_serv)

@router.post("/ask")
def ask_question(req: QuestionRequest):
    """Endpoint untuk bertanya"""
    return api_service.get_answer(req)

@router.post("/add")
def add_document(req: DocumentRequest):
    """Endpoint untuk menambah dokumen"""
    return api_service.add_doc(req)

@router.get("/status")
def status():
    """Endpoint untuk cek status"""
    return api_service.get_status()