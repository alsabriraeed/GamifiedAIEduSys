"""
LLM Service: Ollama Integration
Handles answer generation using local Ollama with llama3.3:latest
"""

import ollama
from typing import List, Dict, Optional
from config import settings
from models.messages import TeacherAction, ActionType, ActionTiming, Citation
import logging
import json
import re

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.client = ollama.Client(host=settings.OLLAMA_BASE_URL)
        self.model = settings.OLLAMA_MODEL
        
        # Verify model is available
        try:
            models_response = self.client.list()
            models_list = models_response.get('models', []) if isinstance(models_response, dict) else []
            
            model_names = []
            for m in models_list:
                if isinstance(m, dict):
                    # Try different possible keys
                    name = m.get('name') or m.get('model') or m.get('id', '')
                    if name:
                        model_names.append(name)
            
            if model_names:
                logger.info(f"Available Ollama models: {model_names}")
                if self.model not in model_names:
                    logger.warning(f"Model {self.model} not found. Available: {model_names}")
                else:
                    logger.info(f"✓ Using Ollama model: {self.model}")
            else:
                logger.warning("No models found in Ollama. Make sure Ollama is running and models are pulled.")
        except Exception as e:
            logger.error(f"Failed to connect to Ollama: {e}")
            logger.info(f"Will attempt to use model: {self.model} anyway")
    
    def generate_answer(
        self,
        question: str,
        retrieved_context: List[Dict],
        current_slide_id: int,
        slide_title: str
    ) -> Dict:
        """
        Generate answer using RAG context
        
        Returns:
            {
                "answer_text": str,
                "citations": List[Citation],
                "actions": List[TeacherAction],
                "confidence": float
            }
        """
        
        # Build context string
        context_str = self._format_context(retrieved_context)
        
        # Create prompt with strict grounding rules
        prompt = self._build_prompt(question, context_str, current_slide_id, slide_title)
        
        logger.info(f"Generating answer for: '{question[:50]}...'")
        
        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                options={
                    "temperature": settings.OLLAMA_TEMPERATURE,
                    "num_predict": settings.OLLAMA_MAX_TOKENS,
                }
            )
            
            answer_text = response['response'].strip()
            
            # Post-process to extract citations and actions
            citations = self._extract_citations(answer_text, retrieved_context)
            actions = self._suggest_actions(answer_text, retrieved_context, current_slide_id)
            confidence = self._estimate_confidence(retrieved_context)
            
            # Clean answer text (remove citation markers if any)
            answer_text = self._clean_answer(answer_text)
            
            logger.info(f"Generated answer ({len(answer_text)} chars, confidence: {confidence:.2f})")
            
            return {
                "answer_text": answer_text,
                "citations": citations,
                "actions": actions,
                "confidence": confidence
            }
            
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return {
                "answer_text": "I apologize, but I'm having trouble processing that question right now. Could you rephrase it?",
                "citations": [],
                "actions": [],
                "confidence": 0.0
            }
    
    def _format_context(self, retrieved_context: List[Dict]) -> str:
        """Format retrieved chunks into context string"""
        context_parts = []
        for i, chunk in enumerate(retrieved_context, 1):
            source = chunk['metadata'].get('source', 'unknown')
            text = chunk['text']
            context_parts.append(f"[Source {i}: {source}]\n{text}\n")
        return "\n".join(context_parts)
    
    def _build_prompt(self, question: str, context: str, slide_id: int, slide_title: str) -> str:
        """Build prompt with system instructions"""
        
        system_prompt = f"""You are an expert deep learning teacher in a virtual classroom. You are currently on Slide {slide_id}: {slide_title}.

STRICT RULES:
1. Answer ONLY using the provided context from slides and course materials below
2. If the information is NOT in the context, respond: "I don't see that in our course materials. Would you like a general explanation, or should we continue with {slide_title}?"
3. Always cite your sources by mentioning slide numbers or document names
4. Keep responses between 30-60 seconds when spoken (roughly 100-200 words)
5. End with a brief follow-up question to check understanding
6. Be conversational and engaging, like a real teacher
7. Use examples from the context when available

CONTEXT FROM COURSE MATERIALS:
{context}

CURRENT SLIDE: Slide {slide_id} - {slide_title}

STUDENT QUESTION: {question}

Provide a clear, educational answer that a teacher would give. Remember to cite sources and check understanding."""

        return system_prompt
    
    def _extract_citations(self, answer: str, context: List[Dict]) -> List[Citation]:
        """Extract citations from answer based on context used"""
        citations = []
        
        # Look for slide mentions in answer
        slide_pattern = r'[Ss]lide (\d+)'
        slide_matches = re.findall(slide_pattern, answer)
        
        for chunk in context[:3]:  # Top 3 most relevant
            metadata = chunk['metadata']
            source = metadata.get('source', '')
            
            # Check if this source was referenced
            confidence = chunk.get('similarity', 0.5)
            
            # Boost confidence if explicitly mentioned
            if 'slide_' in source:
                slide_num = re.search(r'slide_(\d+)', source)
                if slide_num and slide_num.group(1) in slide_matches:
                    confidence = min(confidence + 0.2, 1.0)
            
            citations.append(Citation(
                source=source,
                confidence=confidence,
                snippet=chunk['text'][:150] + "..."
            ))
        
        return citations
    
    def _suggest_actions(self, answer: str, context: List[Dict], current_slide_id: int) -> List[TeacherAction]:
        """Suggest actions based on answer content"""
        actions = []
        
        # Check if referencing a different slide
        slide_pattern = r'[Ss]lide (\d+)'
        slide_mentions = re.findall(slide_pattern, answer)
        
        for slide_num_str in slide_mentions[:1]:  # Only first mention
            slide_num = int(slide_num_str)
            if slide_num != current_slide_id:
                actions.append(TeacherAction(
                    type=ActionType.GOTO_SLIDE,
                    slide_id=slide_num,
                    timing=ActionTiming.BEFORE_SPEECH
                ))
                break
        
        # If staying on current slide, point to screen
        if not actions:
            # Check for visual/diagram references
            visual_keywords = ['see', 'look at', 'shown', 'diagram', 'equation', 'formula', 'example']
            if any(keyword in answer.lower() for keyword in visual_keywords):
                actions.append(TeacherAction(
                    type=ActionType.POINT_TO,
                    target="screen",
                    timing=ActionTiming.DURING_SPEECH,
                    at_word=20  # Rough estimate
                ))
        
        return actions
    
    def _estimate_confidence(self, context: List[Dict]) -> float:
        """Estimate confidence based on retrieval quality"""
        if not context:
            return 0.3
        
        # Average similarity of top results
        similarities = [chunk.get('similarity', 0.5) for chunk in context[:3]]
        avg_similarity = sum(similarities) / len(similarities)
        
        # Boost if top result is very relevant
        if similarities[0] > 0.85:
            avg_similarity = min(avg_similarity + 0.1, 1.0)
        
        return avg_similarity
    
    def _clean_answer(self, text: str) -> str:
        """Clean answer text"""
        # Remove potential markdown artifacts
        text = re.sub(r'\[Source \d+:.*?\]', '', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def generate_lecture_segment(self, slide_id: int, speaker_notes: str, segment_type: str = "explanation") -> str:
        """Generate lecture content for a slide"""
        
        prompt = f"""You are a deep learning teacher presenting Slide {slide_id}.

SPEAKER NOTES:
{speaker_notes}

Generate a natural, engaging {segment_type} (30-45 seconds when spoken) based on these notes. 
Sound like a real teacher, not a robot reading slides. Use "we", "you", "let's" to be conversational."""

        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                options={"temperature": 0.8, "num_predict": 256}
            )
            return response['response'].strip()
        except Exception as e:
            logger.error(f"Lecture generation failed: {e}")
            # Fallback to speaker notes
            return speaker_notes[:500]

# Singleton instance
llm_service = LLMService()
