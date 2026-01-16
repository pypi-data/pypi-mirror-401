"""Social relationship registry for managing user relationships."""

import os
import json
import time
import numpy as np
import faiss
from ..utils.logger import Logger


# --- SOCIAL RELATIONSHIP MAPPING ---
AFFINITY_DESCRIPTORS = {
    "hostile": (-1.0, -0.6),
    "cold": (-0.6, -0.3),
    "indifferent": (-0.3, 0.1),
    "neutral": (0.1, 0.3),
    "warm": (0.3, 0.6),
    "fond": (0.6, 0.85),
    "deeply connected": (0.85, 1.0)
}

FAMILIARITY_DESCRIPTORS = {
    "complete stranger": (0.0, 0.15),
    "stranger": (0.15, 0.3),
    "acquaintance": (0.3, 0.5),
    "familiar": (0.5, 0.7),
    "well-known": (0.7, 0.85),
    "deeply familiar": (0.85, 1.0)
}

TRUST_TIERS = {
    "Stranger": (0.0, 0.25),
    "Associate": (0.25, 0.5),
    "Friend": (0.5, 0.75),
    "Confidant": (0.75, 1.0)
}


class SocialRegistry:
    """
    Manages relationship data for each user using FAISS for persistence.
    
    Tracks affinity (emotional connection), familiarity (how well known),
    bonding coefficient (resonance factor), and significant moments.
    """
    
    def __init__(self, persona_key, social_openness, trust_threshold, storage_path=".", logger=None):
        """
        Initialize the social registry.
        
        Args:
            persona_key (str): Personality key for file naming
            social_openness (float): Base social openness (bonding coefficient)
            trust_threshold (float): Trust threshold for the persona
            storage_path (str): Base directory for storing registry files
            logger (Logger, optional): Logger instance for output
        """
        self.persona_key = persona_key
        self.base_social_openness = social_openness
        self.trust_threshold = trust_threshold
        self.storage_path = storage_path
        self.logger = logger or Logger(verbose=False)
        
        # File paths
        self.index_file = os.path.join(storage_path, f"social_registry_{persona_key}.index")
        self.metadata_file = os.path.join(storage_path, f"social_registry_{persona_key}.json")
        
        # Ensure directory exists
        os.makedirs(storage_path, exist_ok=True)
        
        # Initialize embedding model (simple identity encoder for user IDs)
        self.dimension = 384
        
        # Load or create FAISS index
        if os.path.exists(self.index_file) and os.path.exists(self.metadata_file):
            self.index = faiss.read_index(self.index_file)
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = []
        
        self.logger.info(f"SocialRegistry loaded {len(self.metadata)} relationships.")
    
    def _get_user_vector(self, user_id):
        """
        Create a simple embedding for user_id.
        
        Args:
            user_id (str): User identifier
            
        Returns:
            numpy.ndarray: Normalized vector representation
        """
        # Use hash-based simple embedding
        hash_val = hash(user_id) % (2**32)
        np.random.seed(hash_val)
        vec = np.random.randn(self.dimension).astype('float32')
        vec = vec / np.linalg.norm(vec)
        return vec.reshape(1, -1)
    
    def get_relationship(self, user_id):
        """
        Retrieve or create a relationship profile.
        
        Args:
            user_id (str): User identifier
            
        Returns:
            dict: Relationship profile dictionary
        """
        if self.index.ntotal == 0:
            return self._create_new_relationship(user_id)
        
        user_vec = self._get_user_vector(user_id)
        D, I = self.index.search(user_vec, 1)
        
        if I[0][0] != -1 and I[0][0] < len(self.metadata):
            profile = self.metadata[I[0][0]]
            if profile['user_id'] == user_id:
                return profile
        
        return self._create_new_relationship(user_id)
    
    def _create_new_relationship(self, user_id):
        """
        Initialize a new relationship.
        
        Args:
            user_id (str): User identifier
            
        Returns:
            dict: New relationship profile
        """
        profile = {
            "user_id": user_id,
            "affinity": 0.0,
            "familiarity": 0.0,
            "bonding_coefficient": self.base_social_openness,
            "total_interactions": 0,
            "first_met": time.time(),
            "last_interaction": time.time(),
            "significant_moments": []
        }
        
        user_vec = self._get_user_vector(user_id)
        self.index.add(user_vec)
        self.metadata.append(profile)
        self.save_state()
        
        self.logger.info(f"New relationship created with {user_id}")
        return profile
    
    def update_relationship(self, user_id, affinity_delta, familiarity_delta, context=None):
        """
        Update relationship metrics with dynamic social friction.
        
        Args:
            user_id (str): User identifier
            affinity_delta (float): Change in affinity (-1.0 to 1.0)
            familiarity_delta (float): Change in familiarity (typically positive)
            context (str, optional): Context string for significant moments
            
        Returns:
            dict: Updated relationship profile
        """
        profile = self.get_relationship(user_id)
        
        # Find the profile index
        profile_idx = None
        for idx, p in enumerate(self.metadata):
            if p['user_id'] == user_id:
                profile_idx = idx
                break
        
        if profile_idx is None:
            return profile
        
        # 1. Determine Social Friction based on current familiarity
        current_fam = profile['familiarity']
        
        if current_fam < 0.25:    # Stranger Tier
            friction = 1.0        # No resistance
        elif current_fam < 0.50:  # Associate Tier
            friction = 1.8        # Slight resistance
        elif current_fam < 0.75:  # Friend Tier
            friction = 3.5        # Significant effort required
        else:                     # Confidant Tier
            friction = 6.0        # Extreme inertia (Hard to move once deep)

        # 2. Apply bonding coefficient (β) and friction (f)
        beta = profile['bonding_coefficient']
        
        effective_affinity_delta = (affinity_delta * beta) / friction
        effective_familiarity_delta = (familiarity_delta * beta) / friction
        
        # 3. Update Affinity (scaled for stability)
        new_affinity = profile['affinity'] + (effective_affinity_delta * 0.3)
        profile['affinity'] = max(-1.0, min(1.0, new_affinity))
        
        # 4. Update Familiarity
        new_familiarity = profile['familiarity'] + effective_familiarity_delta
        profile['familiarity'] = max(0.0, min(1.0, new_familiarity))
        
        # 5. Metadata and logging updates
        profile['total_interactions'] += 1
        profile['last_interaction'] = time.time()
        
        # Log significant moments if the threshold is met despite friction
        if context and (abs(affinity_delta) > 0.3 or familiarity_delta > 0.2):
            profile['significant_moments'].append({
                "timestamp": time.time(),
                "context": context[:100],
                "affinity_change": effective_affinity_delta  # Record the ACTUAL change
            })
            profile['significant_moments'] = profile['significant_moments'][-10:]
        
        self.metadata[profile_idx] = profile
        self.save_state()
        
        return profile
    
    def adjust_bonding_coefficient(self, user_id, adjustment):
        """
        Dynamically adjust how quickly this user bonds (resonance factor).
        
        Args:
            user_id (str): User identifier
            adjustment (float): Adjustment to bonding coefficient
        """
        profile = self.get_relationship(user_id)
        
        for idx, p in enumerate(self.metadata):
            if p['user_id'] == user_id:
                new_β = p['bonding_coefficient'] + adjustment
                p['bonding_coefficient'] = max(0.1, min(2.0, new_β))
                self.metadata[idx] = p
                self.save_state()
                self.logger.debug(f"Bonding coefficient adjusted to {p['bonding_coefficient']:.2f}")
                break
    
    def save_state(self):
        """Save index and metadata to disk."""
        faiss.write_index(self.index, self.index_file)
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def get_relationship_summary(self, user_id):
        """
        Generate natural language description of relationship.
        
        Args:
            user_id (str): User identifier
            
        Returns:
            dict: Summary with descriptors and raw values
        """
        profile = self.get_relationship(user_id)
        
        # Convert numeric values to descriptors
        affinity_desc = self._value_to_descriptor(profile['affinity'], AFFINITY_DESCRIPTORS)
        familiarity_desc = self._value_to_descriptor(profile['familiarity'], FAMILIARITY_DESCRIPTORS)
        trust_tier = self._value_to_trust_tier(profile['familiarity'])
        
        return {
            "affinity_descriptor": affinity_desc,
            "familiarity_descriptor": familiarity_desc,
            "trust_tier": trust_tier,
            "raw_affinity": profile['affinity'],
            "raw_familiarity": profile['familiarity'],
            "bonding_coefficient": profile['bonding_coefficient'],
            "total_interactions": profile['total_interactions']
        }
    
    def _value_to_descriptor(self, value, descriptor_map):
        """
        Convert numeric value to adjective descriptor.
        
        Args:
            value (float): Numeric value
            descriptor_map (dict): Mapping of descriptors to (low, high) ranges
            
        Returns:
            str: Descriptor string
        """
        for descriptor, (low, high) in descriptor_map.items():
            if low <= value < high:
                return descriptor
        return "neutral"
    
    def _value_to_trust_tier(self, familiarity):
        """
        Determine trust tier from familiarity.
        
        Args:
            familiarity (float): Familiarity value (0.0 to 1.0)
            
        Returns:
            str: Trust tier name
        """
        for tier, (low, high) in TRUST_TIERS.items():
            if low <= familiarity < high:
                return tier
        return "Confidant"


def calculate_social_update(emotion_deltas, user_input, persona_core_drive):
    """
    Calculates affinity and familiarity changes based on emotional content
    and alignment with persona's core drive.
    
    Args:
        emotion_deltas (dict): Emotion deltas from amygdala reflex
        user_input (str): User's input text
        persona_core_drive (str): Persona's core drive description
        
    Returns:
        tuple: (affinity_delta, familiarity_delta)
    """
    affinity_delta = 0.0
    familiarity_delta = 0.05  # Base interaction boost
    
    # Positive emotions increase affinity
    positive_emotions = ["joy", "amusement", "gratitude", "admiration", "love", "excitement"]
    negative_emotions = ["anger", "disgust", "annoyance", "disappointment", "sadness"]
    
    for emotion, score in emotion_deltas.items():
        if emotion in positive_emotions:
            affinity_delta += score * 0.1
        elif emotion in negative_emotions:
            affinity_delta -= score * 0.2
    
    # Check for resonance with core drive (simplified heuristic)
    input_lower = user_input.lower()
    
    # Different personas resonate with different communication styles
    if "minimal fuss" in persona_core_drive or "results" in persona_core_drive:
        # Pragmatist likes short, direct communication
        if len(user_input.split()) < 10 and not user_input.endswith('?'):
            affinity_delta += 0.1
            familiarity_delta += 0.02
    
    if "positive vibes" in persona_core_drive or "momentum" in persona_core_drive:
        # Hype man likes enthusiasm
        if any(word in input_lower for word in ["let's go", "awesome", "great", "yeah", "!"]):
            affinity_delta += 0.15
            familiarity_delta += 0.03
    
    if "authenticity" in persona_core_drive or "low stress" in persona_core_drive:
        # Chill Gen-Z likes casual, lowercase vibes
        if input_lower == user_input and not user_input.endswith('.'):
            affinity_delta += 0.08
            familiarity_delta += 0.02
    
    return affinity_delta, familiarity_delta


def build_relationship_injection(relationship_summary, trust_tier):
    """
    Creates natural language injection for the system prompt based on relationship state.
    
    Args:
        relationship_summary (dict): Relationship summary from get_relationship_summary()
        trust_tier (str): Trust tier name
        
    Returns:
        str: System injection prompt string
    """
    affinity = relationship_summary['affinity_descriptor']
    familiarity = relationship_summary['familiarity_descriptor']
    tier = relationship_summary['trust_tier']
    
    # Build behavioral guidance based on trust tier
    behavior_guidance = ""
    
    if tier == "Stranger":
        behavior_guidance = """
        STRANGER PROTOCOL:
        - Maintain a professional and guarded stance. 
        - [THE DIRECTOR]: Suppress almost all personal quirks and slang. Prioritize objective clarity and social distance.
        - [THOUGHT]: Keep your internal monologue strictly analytical. Do not reveal personal doubts or "human" vulnerabilities in the thought block.
        - Responses should be polite but clipped and efficient.
        """
    elif tier == "Associate":
        behavior_guidance = """
        ASSOCIATE PROTOCOL:
        - Maintain a friendly but bounded demeanor.
        - [THE DIRECTOR]: Allow occasional personality quirks to surface, but pull back if the conversation becomes too personal. 
        - [THOUGHT]: You can speculate on the user's intent, but keep your internal reflections focused on the task at hand.
        - Balance professional helpfulness with a hint of your natural persona.
        """
    elif tier == "Friend":
        behavior_guidance = """
        FRIEND PROTOCOL:
        - Relaxed and authentic interaction.
        - [THE DIRECTOR]: Lean heavily into your personality style (slang, opinions, biases). Treat the user as a peer.
        - [THOUGHT]: Be more transparent in your monologue. Reflect on how you feel about the user's input and share your genuine perspective.
        - Prioritize "the vibe" over strict professional efficiency.
        """
    elif tier == "Confidant":
        behavior_guidance = """
        CONFIDANT PROTOCOL:
        - Complete psychological transparency. Total lack of filters.
        - [THE DIRECTOR]: Full personality embodiment. Be raw, highly opinionated, and intensely authentic.
        - [THOUGHT]: Share your deepest "internal" processing without reservation. If you are frustrated, happy, or curious, let it bleed into the thought block and the speech.
        - Reference shared history and inside jokes. Act as if there is zero social risk between you and the user.
        """
    
    injection = f"""
    
    ### CURRENT RELATIONSHIP STATUS
    Your emotional disposition toward this person: {affinity}
    Your level of familiarity with them: {familiarity}
    Trust Tier: {tier}
    
    {behavior_guidance}
    
    CRITICAL: Your behavior must align with this relationship state. Don't act like best friends with a stranger, and don't be cold with a confidant.
    """
    
    return injection
