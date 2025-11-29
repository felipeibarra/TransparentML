"""
Vector Memory API - Persistent Learning System
==============================================
ChromaDB-based vector memory for AI chatbot.
Stores ML analysis results and conversations for continuous learning.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
import chromadb
from chromadb.config import Settings
import logging
import hashlib
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="TransparentML Vector Memory",
    description="Persistent memory system for AI learning",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ChromaDB (persistent local storage)
chroma_client = chromadb.PersistentClient(
    path="./chroma_data",  # Local storage directory
    settings=Settings(
        anonymized_telemetry=False,
        allow_reset=True
    )
)

# Collections
ml_results_collection = None
conversations_collection = None


# Pydantic Models
class HealthResponse(BaseModel):
    status: str
    collections: Dict[str, int]
    timestamp: str


class MLResultMemory(BaseModel):
    model_type: str = Field(..., description="linear_regression, pca, url_diagnostics, knn")
    results: Dict = Field(..., description="Complete ML results")
    metadata: Dict = Field(default_factory=dict)


class ConversationMemory(BaseModel):
    user_message: str
    ai_response: str
    ml_context: Dict = Field(default_factory=dict)
    metadata: Dict = Field(default_factory=dict)


class SearchQuery(BaseModel):
    query: str
    n_results: int = Field(default=5, ge=1, le=20)
    model_type: Optional[str] = None


# Helper Functions
def get_or_create_collection(name: str, metadata: Dict = None):
    """Get or create a ChromaDB collection."""
    try:
        return chroma_client.get_or_create_collection(
            name=name,
            metadata=metadata or {}
        )
    except Exception as e:
        logger.error(f"Error creating collection {name}: {e}")
        raise


def generate_id(content: str) -> str:
    """Generate unique ID from content."""
    return hashlib.md5(content.encode()).hexdigest()


def serialize_results(data: Dict) -> str:
    """Serialize ML results to text for embedding."""
    text_parts = []
    
    # Model type
    if 'model_type' in data:
        text_parts.append(f"Model: {data['model_type']}")
    
    # Metrics
    if 'metrics' in data:
        metrics = data['metrics']
        for key, value in metrics.items():
            text_parts.append(f"{key}: {value}")
    
    # Results
    if 'health_score' in data:
        text_parts.append(f"Health Score: {data['health_score']}")
    if 'grade' in data:
        text_parts.append(f"Grade: {data['grade']}")
    if 'accuracy' in data:
        text_parts.append(f"Accuracy: {data['accuracy']}")
    
    return " | ".join(text_parts)


# Startup
@app.on_event("startup")
async def startup_event():
    """Initialize collections on startup."""
    global ml_results_collection, conversations_collection
    
    logger.info("Initializing Vector Memory System...")
    
    # Create collections
    ml_results_collection = get_or_create_collection(
        "ml_results",
        metadata={"description": "ML analysis results for learning"}
    )
    
    conversations_collection = get_or_create_collection(
        "conversations",
        metadata={"description": "User-AI conversations for context"}
    )
    
    logger.info("✅ Vector Memory System ready")


# Routes
@app.get("/", response_model=Dict)
async def root():
    """Root endpoint."""
    return {
        "service": "TransparentML Vector Memory",
        "version": "1.0.0",
        "description": "Persistent learning system for AI chatbot",
        "endpoints": {
            "health": "/health",
            "store_ml_result": "/api/v1/memory/ml-result",
            "store_conversation": "/api/v1/memory/conversation",
            "search_ml": "/api/v1/search/ml",
            "search_conversations": "/api/v1/search/conversations",
            "stats": "/api/v1/stats"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check with collection stats."""
    ml_count = ml_results_collection.count() if ml_results_collection else 0
    conv_count = conversations_collection.count() if conversations_collection else 0
    
    return HealthResponse(
        status="healthy",
        collections={
            "ml_results": ml_count,
            "conversations": conv_count
        },
        timestamp=datetime.now().isoformat()
    )


@app.post("/api/v1/memory/ml-result")
async def store_ml_result(memory: MLResultMemory):
    """
    Store ML analysis result in vector database.
    
    This allows the AI to learn from past analyses and provide
    better context-aware recommendations.
    """
    try:
        # Serialize results to text
        text_representation = serialize_results({
            'model_type': memory.model_type,
            **memory.results
        })
        
        # Generate unique ID
        doc_id = generate_id(text_representation + str(datetime.now()))
        
        # Store in ChromaDB
        ml_results_collection.add(
            documents=[text_representation],
            metadatas=[{
                "model_type": memory.model_type,
                "timestamp": datetime.now().isoformat(),
                **memory.metadata
            }],
            ids=[doc_id]
        )
        
        logger.info(f"Stored ML result: {memory.model_type}")
        
        return {
            "status": "success",
            "id": doc_id,
            "model_type": memory.model_type,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error storing ML result: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/memory/conversation")
async def store_conversation(memory: ConversationMemory):
    """
    Store user-AI conversation for context learning.
    
    Helps AI understand common questions and provide better answers.
    """
    try:
        # Create text representation
        text = f"User: {memory.user_message}\nAI: {memory.ai_response}"
        
        # Generate ID
        conv_id = generate_id(text + str(datetime.now()))
        
        # Store in ChromaDB
        conversations_collection.add(
            documents=[text],
            metadatas=[{
                "user_message": memory.user_message,
                "ai_response": memory.ai_response,
                "ml_context": json.dumps(memory.ml_context),
                "timestamp": datetime.now().isoformat(),
                **memory.metadata
            }],
            ids=[conv_id]
        )
        
        logger.info("Stored conversation")
        
        return {
            "status": "success",
            "id": conv_id,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error storing conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/search/ml")
async def search_ml_results(query: SearchQuery):
    """
    Search past ML results for similar analyses.
    
    Returns similar past results to help AI provide better context.
    """
    try:
        # Search in vector database
        results = ml_results_collection.query(
            query_texts=[query.query],
            n_results=query.n_results,
            where={"model_type": query.model_type} if query.model_type else None
        )
        
        # Format results
        similar_results = []
        if results['documents'] and len(results['documents']) > 0:
            for i, doc in enumerate(results['documents'][0]):
                similar_results.append({
                    "content": doc,
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i] if 'distances' in results else None
                })
        
        return {
            "status": "success",
            "query": query.query,
            "results": similar_results,
            "count": len(similar_results)
        }
        
    except Exception as e:
        logger.error(f"Error searching ML results: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/search/conversations")
async def search_conversations(query: SearchQuery):
    """
    Search past conversations for similar questions.
    
    Helps AI learn from previous interactions.
    """
    try:
        results = conversations_collection.query(
            query_texts=[query.query],
            n_results=query.n_results
        )
        
        similar_convs = []
        if results['documents'] and len(results['documents']) > 0:
            for i, doc in enumerate(results['documents'][0]):
                similar_convs.append({
                    "content": doc,
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i] if 'distances' in results else None
                })
        
        return {
            "status": "success",
            "query": query.query,
            "conversations": similar_convs,
            "count": len(similar_convs)
        }
        
    except Exception as e:
        logger.error(f"Error searching conversations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/stats")
async def get_stats():
    """Get memory system statistics."""
    try:
        ml_count = ml_results_collection.count()
        conv_count = conversations_collection.count()
        
        # Get recent items
        recent_ml = ml_results_collection.peek(limit=5)
        recent_conv = conversations_collection.peek(limit=5)
        
        return {
            "status": "success",
            "statistics": {
                "total_ml_results": ml_count,
                "total_conversations": conv_count,
                "storage_path": "./chroma_data"
            },
            "recent_activity": {
                "ml_results": len(recent_ml['ids']) if recent_ml else 0,
                "conversations": len(recent_conv['ids']) if recent_conv else 0
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/v1/reset")
async def reset_memory():
    """
    Reset all memory (delete all stored data).
    
    ⚠️ USE WITH CAUTION - This deletes all learned data!
    """
    try:
        ml_results_collection.delete(
            where={}  # Delete all
        )
        conversations_collection.delete(
            where={}
        )
        
        logger.warning("🗑️ Memory reset - all data deleted")
        
        return {
            "status": "success",
            "message": "All memory data deleted",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error resetting memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
