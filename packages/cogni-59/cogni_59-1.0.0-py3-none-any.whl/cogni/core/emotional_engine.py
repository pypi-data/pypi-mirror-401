"""Emotional engine for managing emotional state."""

from ..config.emotions import EMOTION_VIBE_MAP
from ..utils.logger import Logger


class EmotionalEngine:
    """
    Manages emotional state based on personality configuration and input deltas.
    
    The engine processes emotion deltas from the amygdala reflex, applies
    personality-specific modifiers (volatility, forgiveness, decay), and
    generates system injection prompts based on current emotional state.
    """
    
    def __init__(self, personality_config, logger=None):
        """
        Initialize the emotional engine.
        
        Args:
            personality_config (dict): Personality configuration with:
                - volatility: Multiplier for emotion deltas
                - decay: Decay rate per turn
                - forgiveness: Reduction factor for negative emotions when positive emotions are high
                - max_delta: Maximum delta per emotion per update
            logger (Logger, optional): Logger instance for output
        """
        # Initialize state with all keys from the VIBE MAP, starting at 0.0
        self.state = {key: 0.0 for key in EMOTION_VIBE_MAP.keys()}
        
        self.volatility = personality_config.get("volatility", 1.0)
        self.decay_rate = personality_config.get("decay", 0.05)
        self.forgiveness_stat = personality_config.get("forgiveness", 0.5)
        self.max_delta = personality_config.get("max_delta", 0.3)
        self.logger = logger or Logger(verbose=False)
    
    def process_reflex(self, input_deltas):
        """
        Process emotion deltas from the amygdala reflex.
        
        This method explicitly updates the internal state based on RoBERTa outputs.
        It applies volatility scaling, forgiveness logic, and caps deltas.
        
        Args:
            input_deltas (dict): Dictionary mapping emotion labels to scores from RoBERTa
        """
        # 1. Volatility
        scaled_deltas = {k: v * self.volatility for k, v in input_deltas.items()}
        
        # 2. Forgiveness (Generalized: Joy reduces negative emotions)
        # We assume 'anger', 'annoyance', 'disapproval' are negative
        if scaled_deltas.get("joy", 0) > 0.1 or scaled_deltas.get("amusement", 0) > 0.1:
            reduction = (scaled_deltas.get("joy", 0) + scaled_deltas.get("amusement", 0)) * self.forgiveness_stat
            for neg in ["anger", "annoyance", "disgust", "sadness"]:
                if self.state[neg] > 0:
                    self.state[neg] = max(0.0, self.state[neg] - reduction)

        # 3. Update State
        for emotion, delta in scaled_deltas.items():
            if delta > 0.01: # Filter tiny noise
                # Cap the delta so one sentence doesn't max out the stat
                actual_delta = min(delta, self.max_delta)
                
                # Check if emotion exists in state (in case model output varies)
                if emotion in self.state:
                    new_val = self.state[emotion] + actual_delta
                    self.state[emotion] = max(0.0, min(1.0, new_val))

        # Log significant states
        formatted = {k: round(v, 2) for k, v in self.state.items() if v > 0.1}
        self.logger.engine_log(f"Updated Top States: {formatted}")

    def apply_decay(self):
        """Apply decay to all emotions over time."""
        for emotion in self.state:
            if self.state[emotion] > 0:
                self.state[emotion] = max(0.0, self.state[emotion] - self.decay_rate)

    def _get_vibe_description(self, emotion, intensity):
        """
        Get vibe description for an emotion at a given intensity.
        
        Args:
            emotion (str): Emotion label
            intensity (float): Emotion intensity (0.0 to 1.0)
            
        Returns:
            str: Vibe description string
        """
        # Lookup the emotion in the new map
        if emotion in EMOTION_VIBE_MAP:
            vibes = EMOTION_VIBE_MAP[emotion]
            # Select intensity level (Low, Mid, High)
            if intensity < 0.4:
                return vibes[0]
            if intensity < 0.7:
                return vibes[1]
            return vibes[2]
        return "neutral"

    def get_system_injection(self):
        """
        Generate system injection prompt based on current emotional state.
        
        Uses EMOTION_VIBE_MAP to create the prompt string with vibe descriptions.
        
        Returns:
            str: System injection prompt string, or empty string if no active emotions
        """
        # 1. Get all valid emotions (> 0.2) sorted High -> Low
        # Exclude 'neutral' from candidates
        candidates = sorted(
            [(k, v) for k, v in self.state.items() if v > 0.2 and k != "neutral"], 
            key=lambda x: x[1], reverse=True
        )
        
        if not candidates:
            return ""

        # 2. Always accept the dominant emotion
        active = [candidates[0]]
        
        # 3. Relative Threshold Logic for the runner-up
        if len(candidates) > 1:
            dominant_score = candidates[0][1]
            secondary_score = candidates[1][1]
            
            if secondary_score >= (dominant_score * 0.6):
                active.append(candidates[1])

        # 4. Build the injection strings using EMOTION_VIBE_MAP
        states = " + ".join([f"{k.upper()} ({v:.2f})" for k, v in active])
        vibes = " and ".join([self._get_vibe_description(k, v) for k, v in active])

        self.logger.engine_log(f"Injection: {states}")

        return f"""
        ### EMOTIONAL LENS ACTIVE
        CRITICAL INSTRUCTION: Filter your "Speaking Style" through this emotional blend.
        You are currently feeling a mix of: {states}
        
        BEHAVIOR GUIDANCE:
        You should act {vibes}
        """
    
    def get_state(self):
        """
        Get current emotional state.
        
        Returns:
            dict: Copy of current emotional state
        """
        return self.state.copy()

