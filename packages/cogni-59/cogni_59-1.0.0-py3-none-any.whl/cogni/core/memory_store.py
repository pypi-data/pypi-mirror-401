"""Memory store classes for short-term, long-term, and synthetic memories."""

import os
import json
import time
import math
import numpy as np
import torch
import faiss
from transformers import AutoTokenizer, AutoModel
from ..utils.logger import Logger


class MemoryStore:
    """
    Base class for memory storage using FAISS vector indexes.
    
    Handles embedding generation and index management.
    """
    
    def __init__(self, index_file, metadata_file, logger=None):
        """
        Initialize memory store.
        
        Args:
            index_file (str): Path to FAISS index file
            metadata_file (str): Path to metadata JSON file
            logger (Logger, optional): Logger instance for output
        """
        self.index_file = index_file
        self.metadata_file = metadata_file
        self.logger = logger or Logger(verbose=False)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(index_file) if os.path.dirname(index_file) else '.', exist_ok=True)
        os.makedirs(os.path.dirname(metadata_file) if os.path.dirname(metadata_file) else '.', exist_ok=True)
        
        # Load embedding model
        self.tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-small-en")
        self.model = AutoModel.from_pretrained("BAAI/bge-small-en")
        self.dimension = 384
        
        # Load or initialize index
        if os.path.exists(self.index_file) and os.path.exists(self.metadata_file):
            self.index = faiss.read_index(self.index_file)
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = []

    def get_embedding(self, text):
        """
        Generate embedding for text.
        
        Args:
            text (str): Text to embed
            
        Returns:
            numpy.ndarray: Normalized embedding vector
        """
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        embeddings = outputs.last_hidden_state[:, 0].numpy()
        norm = np.linalg.norm(embeddings, axis=1, keepdims=True)
        normalized_embeddings = embeddings / norm
        
        return normalized_embeddings

    def save_state(self):
        """Save index and metadata to disk."""
        faiss.write_index(self.index, self.index_file)
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f)


class ShortTermMemory(MemoryStore):
    """
    Short-term memory with time-decaying retrieval.
    
    Stores recent conversation turns and retrieves based on
    semantic similarity with time-based decay.
    """
    
    def __init__(self, storage_path=".", logger=None):
        """
        Initialize short-term memory.
        
        Args:
            storage_path (str): Base directory for storing index files
            logger (Logger, optional): Logger instance for output
        """
        index_file = os.path.join(storage_path, "stm.index")
        metadata_file = os.path.join(storage_path, "stm.json")
        super().__init__(index_file, metadata_file, logger)

    def add_memory(self, text, role):
        """
        Add a memory to short-term storage.
        
        Args:
            text (str): Memory text
            role (str): Role identifier (e.g., "dialogue")
        """
        vector = self.get_embedding(text)
        self.index.add(vector)
        meta = {"text": text, "role": role, "timestamp": time.time()}
        self.metadata.append(meta)
        self.save_state()

    def retrieve(self, query, k=5, decay_alpha=0.0001):
        """
        Retrieve memories based on similarity with time decay.
        
        Args:
            query (str): Query text
            k (int): Number of results to return
            decay_alpha (float): Decay rate for time weighting
            
        Returns:
            list: List of memory text strings
        """
        if self.index.ntotal == 0:
            return []
        
        q_vector = self.get_embedding(query)
        D, I = self.index.search(q_vector, k * 2)
        scored_memories = []
        current_time = time.time()
        
        for dist, idx in zip(D[0], I[0]):
            if idx != -1 and idx < len(self.metadata):
                item = self.metadata[idx]
                similarity = 1 / (1 + dist) 
                age_seconds = current_time - item['timestamp']
                time_weight = math.exp(-decay_alpha * age_seconds)
                final_score = similarity * time_weight
                scored_memories.append((final_score, item['text']))
        
        scored_memories.sort(key=lambda x: x[0], reverse=True)
        return [m[1] for m in scored_memories[:k]]

    def get_recent_turns(self, turns=6):
        """
        Retrieves the last N turns of raw dialogue for analysis.
        
        Args:
            turns (int): Number of recent turns to retrieve
            
        Returns:
            str: Formatted history string
        """
        if len(self.metadata) == 0:
            return ""
        
        # Get last N items
        recent_items = self.metadata[-turns:]
        # Format them as "User: text \n Bot: text"
        formatted_history = []
        for item in recent_items:
            formatted_history.append(item['text'])
            
        return "\n".join(formatted_history)


class LongTermMemory(MemoryStore):
    """
    Long-term memory for permanent facts and user preferences.
    
    Stores consolidated facts extracted from conversations.
    """
    
    def __init__(self, storage_path=".", logger=None):
        """
        Initialize long-term memory.
        
        Args:
            storage_path (str): Base directory for storing index files
            logger (Logger, optional): Logger instance for output
        """
        index_file = os.path.join(storage_path, "ltm.index")
        metadata_file = os.path.join(storage_path, "ltm.json")
        super().__init__(index_file, metadata_file, logger)

    def add_fact(self, text):
        """
        Add a fact to long-term memory.
        
        Args:
            text (str): Fact text to store
        """
        vector = self.get_embedding(text)
        self.index.add(vector)
        self.metadata.append({"text": text, "timestamp": time.time()})
        self.save_state()

    def retrieve(self, query, k=2):
        """
        Retrieve facts based on semantic similarity.
        
        Args:
            query (str): Query text
            k (int): Number of results to return
            
        Returns:
            list: List of fact text strings
        """
        if self.index.ntotal == 0:
            return []
        
        q_vector = self.get_embedding(query)
        _, I = self.index.search(q_vector, k)
        results = []
        
        for idx in I[0]:
            if idx != -1 and idx < len(self.metadata):
                results.append(self.metadata[idx]['text'])
        
        return results


class SyntheticMemory(MemoryStore):
    """
    Handles read-only synthetic memories loaded from JSON.
    
    Index is built once if missing, or loaded from disk.
    """
    
    def __init__(self, persona_key, synthetic_data_dir=None, logger=None):
        """
        Initialize synthetic memory.
        
        Args:
            persona_key (str): Personality key (e.g., "THE_PRAGMATIST")
            synthetic_data_dir (str, optional): Directory containing JSON files.
                If None, uses current directory.
            logger (Logger, optional): Logger instance for output
        """
        if synthetic_data_dir is None:
            synthetic_data_dir = "."
        
        # Ensure directory exists
        if not os.path.exists(synthetic_data_dir):
            os.makedirs(synthetic_data_dir, exist_ok=True)

        # Naming: synthetic_past_data/THE_PRAGMATIST.json
        self.json_source = os.path.join(synthetic_data_dir, f"{persona_key}.json")
        index_path = os.path.join(synthetic_data_dir, f"{persona_key}.index")
        meta_path = os.path.join(synthetic_data_dir, f"{persona_key}_meta.json")

        super().__init__(index_path, meta_path, logger)
        self.persona_key = persona_key
        self.json_source = self.json_source

        # If index is empty but JSON source exists, build the index
        if self.index.ntotal == 0 and os.path.exists(self.json_source):
            self._build_index_from_source()

    def _build_index_from_source(self):
        """Build index from JSON source file."""
        self.logger.info(f"Building index from {self.json_source}...")
        try:
            with open(self.json_source, 'r') as f:
                raw_memories = json.load(f)
            
            for mem in raw_memories:
                text = mem.get("memory_text", "")
                if text:
                    vector = self.get_embedding(text)
                    self.index.add(vector)
                    self.metadata.append(mem) # Store full object including tags
            
            self.save_state()
            self.logger.success(f"Index built. {self.index.ntotal} memories loaded.")
        except Exception as e:
            self.logger.error(f"Failed to build index: {e}")

    def retrieve_relevant(self, query, k=1, threshold=0.78):
        """
        Retrieve relevant memories above similarity threshold.
        
        Args:
            query (str): Query text
            k (int): Number of results to check
            threshold (float): Minimum similarity threshold
            
        Returns:
            list: List of memory text strings above threshold
        """
        if self.index.ntotal == 0:
            return []
        
        q_vector = self.get_embedding(query)
        D, I = self.index.search(q_vector, k)
        
        results = []
        self.logger.debug(f"Scanning for: '{query}'")
        
        for dist, idx in zip(D[0], I[0]):
            if idx != -1 and idx < len(self.metadata):
                # Convert L2 distance to Similarity roughly
                similarity = 1 / (1 + dist)
                mem_text = self.metadata[idx]['memory_text']
                
                if similarity > threshold:
                    self.logger.debug(f"[HIT]  Sim: {similarity:.2f} | {mem_text[:60]}...")
                    results.append(mem_text)
                else:
                    self.logger.debug(f"[MISS] Sim: {similarity:.2f} | {mem_text[:60]}...")
                    
        return results

