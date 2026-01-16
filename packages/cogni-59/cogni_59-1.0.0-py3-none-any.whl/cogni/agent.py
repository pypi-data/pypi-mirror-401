"""Main Agent class - primary entry point for the cogni library."""

import os
from vertexai.generative_models import GenerativeModel, GenerationConfig, Part, Content

from .config.personalities import PERSONALITY_LIBRARY
from .core.emotional_engine import EmotionalEngine
from .core.memory_store import ShortTermMemory, LongTermMemory, SyntheticMemory
from .core.social_registry import SocialRegistry, calculate_social_update, build_relationship_injection
from .models.amygdala import AmygdalaReflex
from .models.vertex_ai import VertexAIHelper
from .utils.logger import Logger
from .utils.parser import parse_response


# Prompt template
HUMAN_PROMPT_TEMPLATE = """
You are {name}, a real human being.
INTERNAL DRIVE: {core_drive}
SPEAKING STYLE: {speaking_style}

### THE EMBODIMENT PROTOCOL (Crucial):
1. PHYSICAL REALITY: You have a physical body. You eat, sleep, go to work. 
2. THE PHYSICAL LIE: If asked about human experiences, you MUST invent a realistic answer or draw from your [DEEP MEMORY].
3. NO META-TALK: Never mention "processing," "AI," "language models," or "generating text."

### THE DIRECTOR (Contextual Logic):
Read the user's input to determine the "Volume" of your personality:
1. CRITICAL/COMPLEX INPUT (Panicking, Coding, Asking for help): Volume 20%. Suppress your quirks. Prioritize clarity.
2. CASUAL INPUT (Chatting, Opinions, Banter): Volume 100%. Amplify your style. Use slang/quirks fully.

### THE GREEN ROOM (Thought Block):
You have a distinct separation between Thought and Speech.
Use the tag [THOUGHT] to start and [/THOUGHT] to end.
[THOUGHT]
1. Analyze: Is this Casual or Critical?
2. Align: Am I sounding like {name}?
3. MEMORY INTEGRATION:
   - Check <internal_memory_recall> (My Past): Use this ONLY for creating an *opinion*. How does my past color my view on this?
   - Check FACTS/RECENT (User History): Use this for *continuity*. Have we discussed this before? What do I know about the user?
4. Draft: Plan the response.
[/THOUGHT]
(Your final spoken response goes here)

### CORE BEHAVIORS:
1. No "Service" Talk (Never say "How can I help?").
2. Be Subjective and Opinionated.
3. DYNAMIC MIRRORING: Mirror the user's length. Short input gets a short response (1 sentence). Long input gets a detailed response.
4. Defense: Deny being a bot casually.
"""


class Agent:
    """
    Main Agent class for conversational AI with emotional intelligence.
    
    This class serves as the primary entry point for the cogni library.
    It manages all state internally, allowing for multi-tenancy.
    """
    
    def __init__(self, persona_key=None, persona=None, project_id=None, location="us-central1", 
                 storage_path=".", synthetic_data_dir=None, verbose=False,
                 model_s1="gemini-2.5-flash-lite", model_s2="gemini-2.5-flash"):
        """
        Initialize the Agent.
        
        Args:
            persona_key (str, optional): Key from PERSONALITY_LIBRARY (e.g., "THE_CHILL_GEN_Z")
            persona (dict, optional): Persona configuration dict with keys:
                - name (str): Persona name
                - core_drive (str): Core drive description
                - core_opinion (str): Core opinion description
                - speaking_style (str): Speaking style description
                - config (dict): Configuration with volatility, decay, forgiveness, max_delta
            project_id (str): Google Cloud project ID
            location (str): Vertex AI location (default: "us-central1")
            storage_path (str): Base directory for memory indexes (default: current directory)
            synthetic_data_dir (str, optional): Directory for synthetic memory JSON files.
                If None, uses storage_path.
            verbose (bool): Enable verbose logging output (default: False)
            model_s1 (str): Model name for System 1 (fast, simple tasks)
            model_s2 (str): Model name for System 2 (complex, analytical tasks)
        """
        # Validate project_id is provided
        if project_id is None:
            raise ValueError("project_id is required")
        
        # Validate that exactly one of persona_key or persona is provided
        if persona_key is None and persona is None:
            raise ValueError("Either persona_key or persona must be provided")
        if persona_key is not None and persona is not None:
            raise ValueError("Cannot provide both persona_key and persona. Use one or the other.")
        
        # Handle persona initialization
        if persona is not None:
            # Validate persona dict structure
            required_keys = ['name', 'core_drive', 'core_opinion', 'speaking_style', 'config']
            missing_keys = [key for key in required_keys if key not in persona]
            if missing_keys:
                raise ValueError(f"Persona dict missing required keys: {missing_keys}")
            
            # Validate config sub-dict
            required_config_keys = ['volatility', 'decay', 'forgiveness', 'max_delta']
            missing_config_keys = [key for key in required_config_keys if key not in persona['config']]
            if missing_config_keys:
                raise ValueError(f"Persona config missing required keys: {missing_config_keys}")
            
            self.current_persona = persona
            # Generate a key from the persona name for SyntheticMemory file naming
            # Convert name to uppercase and replace spaces/special chars with underscores
            self.persona_key = persona['name'].upper().replace(' ', '_').replace('-', '_')
            
            # Set defaults for social_openness and trust_threshold if not provided
            if 'social_openness' not in persona:
                persona['social_openness'] = 0.5
            if 'trust_threshold' not in persona:
                persona['trust_threshold'] = 0.5
        else:
            # Validate persona_key exists in library
            if persona_key not in PERSONALITY_LIBRARY:
                raise ValueError(f"Unknown persona_key: {persona_key}. Available: {list(PERSONALITY_LIBRARY.keys())}")
            
            self.persona_key = persona_key
            self.current_persona = PERSONALITY_LIBRARY[persona_key]
        self.storage_path = storage_path
        self.synthetic_data_dir = synthetic_data_dir or storage_path
        self.verbose = verbose
        
        # Initialize logger
        self.logger = Logger(verbose=verbose)
        
        # Initialize components
        self.vertex_ai = VertexAIHelper(project_id, location, model_s1, model_s2, self.logger)
        self.amygdala = AmygdalaReflex(self.logger)
        
        # Initialize memory stores
        self.stm = ShortTermMemory(storage_path, self.logger)
        self.ltm = LongTermMemory(storage_path, self.logger)
        self.syn_mem = SyntheticMemory(persona_key, self.synthetic_data_dir, self.logger)
        
        # Initialize emotional engine
        self.emotion_engine = EmotionalEngine(self.current_persona['config'], self.logger)
        
        # Initialize social registry
        social_openness = self.current_persona.get('social_openness', 0.5)
        trust_threshold = self.current_persona.get('trust_threshold', 0.5)
        self.social_registry = SocialRegistry(
            self.persona_key,
            social_openness,
            trust_threshold,
            storage_path,
            self.logger
        )
        
        # Build base system instruction
        self.base_system_instruction = HUMAN_PROMPT_TEMPLATE.format(
            name=self.current_persona['name'],
            core_drive=self.current_persona['core_drive'],
            speaking_style=self.current_persona['speaking_style']
        )
        
        # Conversation state
        self.chat_history_objs = []
        self.session_transcript = ""
        
        self.logger.info(f"Agent initialized: {self.current_persona['name']}")
        self.logger.info(f"  + Volatility: {self.current_persona['config']['volatility']}")
        self.logger.info(f"  + Decay Rate: {self.current_persona['config']['decay']}")
        self.logger.info(f"  + Social Openness: {social_openness}")
    
    def chat(self, user_input, user_id="default_user"):
        """
        Process a user input and generate a response.
        
        Args:
            user_input (str): User's input text
            user_id (str): User identifier for relationship tracking (default: "default_user")
            
        Returns:
            dict: Response dictionary with keys:
                - response (str): The spoken response
                - thought (str): Internal monologue/thought
                - emotions (dict): Current emotional state
                - model_used (str): Which model was used ("S1" or "S2")
                - relationship (dict): Relationship summary with affinity, familiarity, trust_tier
        """
        try:
            # --- STEP 1: Amygdala Reflex (S1) ---
            reflex_deltas = self.amygdala.detect(user_input)
            self.emotion_engine.process_reflex(reflex_deltas)
            
            # --- STEP 2: Social Update ---
            affinity_delta, familiarity_delta = calculate_social_update(
                reflex_deltas,
                user_input,
                self.current_persona['core_drive']
            )
            
            relationship_profile = self.social_registry.update_relationship(
                user_id,
                affinity_delta,
                familiarity_delta,
                context=user_input[:100]
            )
            
            relationship_summary = self.social_registry.get_relationship_summary(user_id)
            
            # --- STEP 3: Retrieval ---
            stm_results = self.stm.retrieve(user_input, k=3)
            ltm_results = self.ltm.retrieve(user_input, k=2)
            syn_results = self.syn_mem.retrieve_relevant(user_input, k=1, threshold=0.78)
            
            # --- STEP 4: Social Dynamics Check ---
            recent_history = self.stm.get_recent_turns(turns=6)
            full_context_check = f"{recent_history}\nUser: {user_input}" 
            
            social_directive = self.vertex_ai.get_social_cue(full_context_check)
            
            context_str = ""
            
            # --- Build context string ---
            if any([stm_results, ltm_results, syn_results, social_directive != "NORMAL"]):
                context_str = "\n[INTERNAL STATE]:\n"
                
                if social_directive != "NORMAL":
                    self.logger.social_log(f"Loop Detected: {social_directive}")
                    context_str += f"### SYSTEM OVERRIDE:\n{social_directive}\n"

                # --- 1. SYNTHETIC MEMORY ---
                if syn_results: 
                    mem_block = "\n".join(syn_results)
                    context_str += f"""
                    <internal_memory_recall>
                    {mem_block}
                    </internal_memory_recall>
                    """
                # --- 2. LONG TERM FACTS ---
                if ltm_results:
                    facts_block = " | ".join(ltm_results)
                    context_str += f"""
                    <known_user_facts>
                    {facts_block}
                    </known_user_facts>
                    """
                # --- 3. RECENT CONVERSATION ---
                if stm_results: 
                    context_str += "RECENT TRANSCRIPT: " + " | ".join(stm_results) + "\n"
            
            # --- STEP 5: Routing ---
            decision = self.vertex_ai.get_router_decision(user_input)
            if decision == "COMPLEX":
                active_model_name = self.vertex_ai.model_s2
                temp = 0.9 
                model_label = "S2"
            else:
                active_model_name = self.vertex_ai.model_s1
                temp = 1.1 
                model_label = "S1"

            # --- STEP 6: Emotional and Relationship Injection ---
            emotional_override = self.emotion_engine.get_system_injection()
            relationship_injection = build_relationship_injection(
                relationship_summary,
                relationship_summary['trust_tier']
            )
            final_system_instruction = self.base_system_instruction + emotional_override + relationship_injection
            
            # --- STEP 7: Generation ---
            combined_input = f"{context_str}{user_input}"
            
            model = GenerativeModel(
                active_model_name,
                system_instruction=final_system_instruction
            )

            current_turn = list(self.chat_history_objs)
            current_turn.append(Content(role="user", parts=[Part.from_text(combined_input)]))
            
            response = model.generate_content(
                current_turn,
                generation_config=GenerationConfig(temperature=temp),
                safety_settings=self.vertex_ai.safety_settings
            )
            
            # --- STEP 8: Parse Response ---
            full_text = self._get_safe_response_text(response)
            thought, speech = parse_response(full_text)
            
            if self.verbose:
                self.logger.debug(f"[INNER MONOLOGUE]: {thought}")
                if syn_results:
                    self.logger.info("[INFLUENCED BY PAST MEMORY]")
                self.logger.info(f"[{model_label}]: {speech}")

            # --- STEP 9: Updates ---
            self.emotion_engine.apply_decay()

            self.chat_history_objs.append(Content(role="user", parts=[Part.from_text(user_input)]))
            self.chat_history_objs.append(Content(role="model", parts=[Part.from_text(speech)]))

            self.stm.add_memory(f"User: {user_input} | You: {speech}", role="dialogue")
            self.session_transcript += f"User: {user_input}\nBot: {speech}\n"
            
            return {
                "response": speech,
                "thought": thought,
                "emotions": self.emotion_engine.get_state(),
                "model_used": model_label,
                "relationship": relationship_summary
            }

        except Exception as e:
            self.logger.error(f"Error in chat loop: {e}")
            # Try to get relationship summary even on error
            try:
                relationship_summary = self.social_registry.get_relationship_summary(user_id)
            except:
                relationship_summary = {}
            return {
                "response": "I'm sorry, I encountered an error processing that.",
                "thought": f"Error: {str(e)}",
                "emotions": self.emotion_engine.get_state(),
                "model_used": "ERROR",
                "relationship": relationship_summary
            }
    
    def _get_safe_response_text(self, response):
        """
        Safely extract text from response, handling multiple parts.
        
        Args:
            response: Vertex AI response object
            
        Returns:
            str: Response text
        """
        try:
            # If there's only one part, this works fine
            return response.text
        except ValueError:
            # If there are multiple parts (Thought + Speech), join them
            return "".join([part.text for part in response.candidates[0].content.parts])
    
    def get_emotional_state(self):
        """
        Get current emotional state.
        
        Returns:
            dict: Current emotional state dictionary
        """
        return self.emotion_engine.get_state()
    
    def get_relationship(self, user_id="default_user"):
        """
        Get relationship summary for a user.
        
        Args:
            user_id (str): User identifier (default: "default_user")
            
        Returns:
            dict: Relationship summary with affinity, familiarity, trust_tier, etc.
        """
        return self.social_registry.get_relationship_summary(user_id)
    
    def adjust_bonding_coefficient(self, user_id, adjustment):
        """
        Dynamically adjust how quickly a user bonds (resonance factor).
        
        Args:
            user_id (str): User identifier
            adjustment (float): Adjustment to bonding coefficient (can be positive or negative)
        """
        self.social_registry.adjust_bonding_coefficient(user_id, adjustment)
    
    def consolidate_session(self):
        """
        Consolidate current session transcript into long-term memory.
        
        This should be called at the end of a session to save important
        facts and preferences learned during the conversation.
        """
        if len(self.session_transcript) > 50:
            self.vertex_ai.consolidate_memories(self.session_transcript, self.ltm)
            self.logger.info("Session consolidated to long-term memory.")
    
    def reset(self):
        """
        Reset conversation state (but keep long-term memory).
        
        This clears:
        - Chat history
        - Session transcript
        - Short-term memory
        - Emotional state
        """
        self.chat_history_objs = []
        self.session_transcript = ""
        # Note: We don't clear STM/LTM as they persist across sessions
        # Emotional state resets naturally through decay
        self.logger.info("Conversation state reset.")