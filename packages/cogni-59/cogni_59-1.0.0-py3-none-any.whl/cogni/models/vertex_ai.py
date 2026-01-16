"""Vertex AI/Gemini helper functions."""

import json
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
from ..config.safety import get_safety_settings
from ..utils.logger import Logger


# Prompt templates
ROUTER_PROMPT = """
Analyze input. Output 'SIMPLE' or 'COMPLEX'.
SIMPLE: Greetings, small talk, personal questions, short queries.
COMPLEX: Coding, logic puzzles, physics explanations, long instructions, deep analysis.
Input: {user_input}
Decision:
"""

SOCIAL_DYNAMICS_PROMPT = """
You are a Conversation Flow Monitor.
Analyze the last 3 turns of dialogue between User and Bot.

OBJECTIVE: Detect if the conversation is stuck in a loop.

Signs of a Loop:
1. Repetitive Refusal: Bot is giving the same answer to the same request multiple times.
2. Circular Argument: Neither side is providing new information.
3. Stagnation: The conversation has stalled.

If a LOOP is detected:
Output a directive to BREAK THE PATTERN.
Crucial: Do not specify *how* to break it (e.g. don't say "get angry"). 
Just order the bot to CHANGE TACTICS immediately.

Example Output: "[DIRECTIVE]: Loop detected. User is persisting. STOP REPEATING YOURSELF. Change tactics immediately."

If NORMAL:
Output "NORMAL"

Chat History:
{history}

Analysis:
"""

CONSOLIDATION_PROMPT = """
You are a Memory Consolidation System. 
Extract **Permanent Facts** and **User Preferences** from the transcript.
Ignore small talk.

Return a JSON list of strings.
Transcript:
{transcript}

Output JSON:
"""


class VertexAIHelper:
    """
    Helper class for Vertex AI/Gemini operations.
    
    Manages model instances and provides methods for routing, consolidation,
    and social dynamics analysis.
    """
    
    def __init__(self, project_id, location, model_s1="gemini-2.5-flash-lite", 
                 model_s2="gemini-2.5-flash", logger=None):
        """
        Initialize Vertex AI helper.
        
        Args:
            project_id (str): Google Cloud project ID
            location (str): Vertex AI location (e.g., "us-central1")
            model_s1 (str): Model name for System 1 (fast, simple tasks)
            model_s2 (str): Model name for System 2 (complex, analytical tasks)
            logger (Logger, optional): Logger instance for output
        """
        self.project_id = project_id
        self.location = location
        self.model_s1 = model_s1
        self.model_s2 = model_s2
        self.logger = logger or Logger(verbose=False)
        self.safety_settings = get_safety_settings()
        
        # Initialize Vertex AI
        try:
            vertexai.init(project=project_id, location=location)
            self.logger.info(f"Vertex AI initialized: project={project_id}, location={location}")
        except Exception as e:
            self.logger.error(f"Vertex AI Init Failed: {e}")
            raise
    
    def get_router_decision(self, user_input):
        """
        Determine if input is SIMPLE or COMPLEX.
        
        Args:
            user_input (str): User's input text
            
        Returns:
            str: "SIMPLE" or "COMPLEX"
        """
        try:
            model = GenerativeModel(self.model_s1)
            response = model.generate_content(
                ROUTER_PROMPT.format(user_input=user_input),
                generation_config=GenerationConfig(temperature=0.0, max_output_tokens=10),
                safety_settings=self.safety_settings
            )
            decision = response.text.strip().upper()
            return "COMPLEX" if "COMPLEX" in decision else "SIMPLE"
        except Exception as e:
            self.logger.warning(f"Router decision failed: {e}. Defaulting to SIMPLE.")
            return "SIMPLE"
    
    def consolidate_memories(self, session_transcript, ltm):
        """
        Consolidate session transcript into long-term memory facts.
        
        Args:
            session_transcript (str): Full conversation transcript
            ltm: LongTermMemory instance to add facts to
        """
        if not session_transcript or len(session_transcript) < 50:
            return
        
        self.logger.info("Consolidating memories...")
        try:
            model = GenerativeModel(self.model_s1)
            response = model.generate_content(
                CONSOLIDATION_PROMPT.format(transcript=session_transcript),
                generation_config=GenerationConfig(response_mime_type="application/json"),
                safety_settings=self.safety_settings
            )
            facts = json.loads(response.text)
            for fact in facts:
                self.logger.debug(f"Learning: {fact}")
                ltm.add_fact(fact)
        except Exception as e:
            self.logger.warning(f"Consolidation failed: {e}")
    
    def get_social_cue(self, chat_history_text):
        """
        Detect conversation loops using social dynamics analysis.
        
        Args:
            chat_history_text (str): Recent chat history as text
            
        Returns:
            str: "NORMAL" or a directive string if loop detected
        """
        # Don't check if the chat history is too short
        if len(chat_history_text) < 50:
            return "NORMAL"
        
        try:
            model = GenerativeModel(self.model_s1)
            response = model.generate_content(
                SOCIAL_DYNAMICS_PROMPT.format(history=chat_history_text),
                generation_config=GenerationConfig(temperature=0.0, max_output_tokens=50),
                safety_settings=self.safety_settings
            )
            analysis = response.text.strip()
            
            # Only return if it actually triggered a directive
            if "DIRECTIVE" in analysis:
                return analysis
            return "NORMAL"
        except Exception as e:
            self.logger.warning(f"Social cue detection failed: {e}")
            return "NORMAL"
    
    def get_model_instance(self, model_name):
        """
        Get a GenerativeModel instance for the specified model name.
        
        Args:
            model_name (str): Model name (typically model_s1 or model_s2)
            
        Returns:
            GenerativeModel: Model instance
        """
        return GenerativeModel(model_name)

