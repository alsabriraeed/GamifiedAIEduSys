"""
RAG Service - Simplified version without sentence-transformers
Uses ChromaDB with default embeddings
"""

import logging
import chromadb
from chromadb.config import Settings as ChromaSettings
from pathlib import Path
from typing import List, Dict
import json

from config import settings

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        logger.info("Initializing RAG service (simplified embeddings)...")
        
        # Initialize ChromaDB with default embeddings
        self.chroma_client = chromadb.PersistentClient(
            path=str(settings.VECTOR_STORE_DIR)
        )
        
        # Get or create collection
        self.collection = self.chroma_client.get_or_create_collection(
            name="course_knowledge",
            metadata={"description": "Deep learning course materials"}
        )
        
        # Check if we need to index
        if self.collection.count() == 0:
            logger.info("Knowledge base empty, indexing documents...")
            self.index_knowledge_base()
        else:
            logger.info(f"Knowledge base loaded: {self.collection.count()} documents")
    
    def index_knowledge_base(self):
        """Index all course materials"""
        documents = []
        metadatas = []
        ids = []
        
        # Index slides
        slides_index_path = settings.SLIDES_DIR / "slides_index.json"
        if slides_index_path.exists():
            with open(slides_index_path) as f:
                slides_data = json.load(f)
                for slide in slides_data.get("slides", []):
                    slide_id = slide["id"]
                    
                    # Index slide bullets
                    slide_text = f"{slide['title']}\\n" + "\\n".join(slide.get("bullets", []))
                    documents.append(slide_text)
                    metadatas.append({"source": f"slide_{slide_id:02d}", "type": "slide"})
                    ids.append(f"slide_{slide_id:02d}")
                    
                    # Index speaker notes if available
                    notes_path = settings.SLIDES_DIR / "speaker_notes" / f"slide_{slide_id:02d}.md"
                    if notes_path.exists():
                        with open(notes_path) as nf:
                            notes_content = nf.read()
                            documents.append(notes_content)
                            metadatas.append({"source": f"slide_{slide_id:02d}_notes", "type": "speaker_notes"})
                            ids.append(f"slide_{slide_id:02d}_notes")
        
        # Index documents
        for doc_path in settings.DOCUMENTS_DIR.glob("*.md"):
            with open(doc_path) as f:
                content = f.read()
                # Split into chunks
                chunks = self._split_text(content, chunk_size=500)
                for i, chunk in enumerate(chunks):
                    documents.append(chunk)
                    metadatas.append({"source": doc_path.name, "type": "document", "chunk": i})
                    ids.append(f"{doc_path.stem}_chunk_{i}")
        
        if documents:
            logger.info(f"Indexing {len(documents)} documents...")
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            logger.info("Indexing complete!")
        else:
            logger.warning("No documents found to index")
    
    def _split_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Simple text splitter"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk:
                chunks.append(chunk)
        
        return chunks
    
    def retrieve(self, query: str, current_slide_id: int = None, top_k: int = 5) -> List[Dict]:
        """
        Retrieve relevant chunks for a query
        
        Returns:
            List of dicts with 'text', 'metadata', 'similarity'
        """
        try:
            # Build query with slide context
            if current_slide_id:
                enhanced_query = f"Slide {current_slide_id}: {query}"
            else:
                enhanced_query = query
            
            # Query ChromaDB
            results = self.collection.query(
                query_texts=[enhanced_query],
                n_results=top_k
            )
            
            # Format results
            retrieved = []
            if results and results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    # Extract similarity (distance to similarity)
                    distance = results['distances'][0][i] if results.get('distances') else 1.0
                    similarity = max(0.0, 1.0 - distance)  # Convert distance to similarity
                    
                    metadata = results['metadatas'][0][i] if results.get('metadatas') else {}
                    
                    retrieved.append({
                        'text': doc,
                        'metadata': metadata,
                        'similarity': similarity
                    })
            
            logger.info(f"Retrieved {len(retrieved)} chunks for: '{query[:50]}...'")
            return retrieved
            
        except Exception as e:
            logger.error(f"Retrieval failed: {e}")
            return []
    
    def refresh_knowledge_base(self):
        """Re-index all documents"""
        logger.info("Refreshing knowledge base...")
        # Delete and recreate collection
        try:
            self.chroma_client.delete_collection("course_knowledge")
        except:
            pass
        
        self.collection = self.chroma_client.get_or_create_collection(
            name="course_knowledge",
            metadata={"description": "Deep learning course materials"}
        )
        
        self.index_knowledge_base()
        logger.info("Knowledge base refreshed!")

# Singleton instance
rag_service = RAGService()
