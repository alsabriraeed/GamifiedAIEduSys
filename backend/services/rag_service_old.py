"""
RAG Service: Retrieval-Augmented Generation
Handles vector search and knowledge retrieval from slides and documents
"""

import json
import chromadb
from pathlib import Path
from typing import List, Dict, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from sentence_transformers import SentenceTransformer
from config import settings
import logging

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(path=str(settings.VECTOR_STORE_DIR))
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(name="knowledge_base")
            logger.info("Loaded existing knowledge base")
        except:
            self.collection = self.client.create_collection(
                name="knowledge_base",
                metadata={"description": "Deep learning course knowledge base"}
            )
            logger.info("Created new knowledge base")
            self._ingest_knowledge()
    
    def _ingest_knowledge(self):
        """Load and index all knowledge base content"""
        logger.info("Ingesting knowledge base...")
        
        documents = []
        
        # Load slides and speaker notes
        slides_index_path = settings.SLIDES_DIR / "slides_index.json"
        if slides_index_path.exists():
            with open(slides_index_path) as f:
                slides_data = json.load(f)
            
            for slide in slides_data.get("slides", []):
                slide_id = slide["id"]
                
                # Add slide content
                slide_text = f"Slide {slide_id}: {slide['title']}\n"
                slide_text += "\n".join(f"- {bullet}" for bullet in slide["bullets"])
                
                documents.append(Document(
                    page_content=slide_text,
                    metadata={
                        "source": f"slide_{slide_id:02d}",
                        "type": "slide",
                        "slide_id": slide_id,
                        "title": slide["title"]
                    }
                ))
                
                # Add speaker notes
                notes_path = Path(slide["speaker_notes_path"])
                if notes_path.exists():
                    with open(notes_path) as f:
                        notes_content = f.read()
                    
                    documents.append(Document(
                        page_content=notes_content,
                        metadata={
                            "source": f"slide_{slide_id:02d}_notes",
                            "type": "speaker_notes",
                            "slide_id": slide_id,
                            "title": slide["title"]
                        }
                    ))
        
        # Load documents (syllabus, fundamentals)
        for doc_path in settings.DOCUMENTS_DIR.glob("*.md"):
            with open(doc_path) as f:
                content = f.read()
            
            documents.append(Document(
                page_content=content,
                metadata={
                    "source": doc_path.name,
                    "type": "document"
                }
            ))
        
        logger.info(f"Loaded {len(documents)} documents")
        
        # Chunk documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""]
        )
        
        chunks = text_splitter.split_documents(documents)
        logger.info(f"Created {len(chunks)} chunks")
        
        # Generate embeddings and add to ChromaDB
        texts = [chunk.page_content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        
        # Batch processing for efficiency
        batch_size = 100
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            batch_metadatas = metadatas[i:i+batch_size]
            batch_ids = ids[i:i+batch_size]
            
            embeddings = self.embedding_model.encode(batch_texts).tolist()
            
            self.collection.add(
                embeddings=embeddings,
                documents=batch_texts,
                metadatas=batch_metadatas,
                ids=batch_ids
            )
        
        logger.info("Knowledge base ingestion complete")
    
    def retrieve(self, query: str, current_slide_id: Optional[int] = None, top_k: int = None) -> List[Dict]:
        """
        Retrieve relevant chunks for a query
        
        Args:
            query: Student's question
            current_slide_id: Current slide number for context boosting
            top_k: Number of results to return
        
        Returns:
            List of relevant chunks with metadata and scores
        """
        if top_k is None:
            top_k = settings.TOP_K_RETRIEVAL
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])[0].tolist()
        
        # Search with optional filtering for current slide
        where_filter = None
        if current_slide_id is not None:
            # First try to get results from current slide
            where_filter = {"slide_id": current_slide_id}
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k * 2, 20),  # Get more results for filtering
            where=where_filter
        )
        
        # If we have slide filter and got < top_k results, search without filter
        if where_filter and len(results['documents'][0]) < top_k:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
        
        # Format results
        retrieved_chunks = []
        for i, (doc, metadata, distance) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        )):
            # Convert distance to similarity (ChromaDB uses L2 distance)
            similarity = 1 / (1 + distance)
            
            if similarity >= settings.SIMILARITY_THRESHOLD or i < 2:  # Always include top 2
                retrieved_chunks.append({
                    "text": doc,
                    "metadata": metadata,
                    "similarity": similarity,
                    "rank": i + 1
                })
        
        logger.info(f"Retrieved {len(retrieved_chunks)} chunks for query: '{query[:50]}...'")
        
        return retrieved_chunks[:top_k]
    
    def get_slide_context(self, slide_id: int) -> Optional[Dict]:
        """Get full context for a specific slide"""
        results = self.collection.query(
            query_embeddings=None,
            where={"slide_id": slide_id, "type": "slide"},
            n_results=1
        )
        
        if results['documents'][0]:
            return {
                "text": results['documents'][0][0],
                "metadata": results['metadatas'][0][0]
            }
        return None
    
    def refresh_knowledge_base(self):
        """Re-ingest knowledge base (useful after content updates)"""
        self.client.delete_collection("knowledge_base")
        self.collection = self.client.create_collection(
            name="knowledge_base",
            metadata={"description": "Deep learning course knowledge base"}
        )
        self._ingest_knowledge()

# Singleton instance
rag_service = RAGService()
