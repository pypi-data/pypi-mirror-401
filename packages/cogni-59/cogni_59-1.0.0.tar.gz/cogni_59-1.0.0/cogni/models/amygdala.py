"""RoBERTa-based emotion detection (Amygdala Reflex)."""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from ..utils.logger import Logger


class AmygdalaReflex:
    """
    Encapsulates RoBERTa emotion detection model.
    
    This class loads the emotion model once and provides a detect() method
    to analyze user input for emotional content.
    """
    
    EMOTION_MODEL_NAME = "SamLowe/roberta-base-go_emotions"
    
    def __init__(self, logger=None):
        """
        Initialize the Amygdala Reflex model.
        
        Args:
            logger (Logger, optional): Logger instance for output. If None, creates a silent logger.
        """
        self.logger = logger or Logger(verbose=False)
        self.tokenizer = None
        self.model = None
        self._model_loaded = False
    
    def _load_model(self):
        """Lazily load the emotion model."""
        if not self._model_loaded:
            self.logger.info("Loading RoBERTa Emotion Model...")
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(self.EMOTION_MODEL_NAME)
                self.model = AutoModelForSequenceClassification.from_pretrained(self.EMOTION_MODEL_NAME)
                self._model_loaded = True
                self.logger.info("RoBERTa Emotion Model loaded successfully.")
            except Exception as e:
                self.logger.error(f"Failed to load RoBERTa model: {e}")
                raise
    
    def detect(self, user_input):
        """
        Detect emotions in user input using RoBERTa model.
        
        Args:
            user_input (str): The user's input text to analyze
            
        Returns:
            dict: Dictionary mapping emotion labels to scores (only scores > 0.05)
        """
        if not self._model_loaded:
            self._load_model()
        
        if self.model is None or self.tokenizer is None:
            self.logger.error("Model not loaded. Returning empty results.")
            return {}
        
        try:
            inputs = self.tokenizer(user_input, return_tensors="pt", truncation=True, max_length=512)
            
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            # Get probabilities using Sigmoid (multilabel classification)
            probs = torch.sigmoid(outputs.logits).squeeze()

            id2label = self.model.config.id2label
            results = {}
            
            # Create dictionary of {label: score}
            for idx, score in enumerate(probs):
                label = id2label[idx]
                score_val = score.item()

                if score_val > 0.05: 
                    results[label] = score_val
            
            # Debug log
            top_emotions = sorted(results.items(), key=lambda x: x[1], reverse=True)[:3]
            self.logger.debug(f"Amygdala detected: {top_emotions}")
            
            return results

        except Exception as e:
            self.logger.error(f"RoBERTa Amygdala detection failed: {e}")
            return {}

