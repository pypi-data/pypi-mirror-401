"""Token management utility."""

import tiktoken
import logging

logger = logging.getLogger(__name__)

class TokenManager:
    """Manager for token counting and truncation."""
    
    def __init__(self, model_name: str = "gpt-4o"):
        self.model_name = model_name
        try:
            self.encoding = tiktoken.encoding_for_model(model_name)
        except KeyError:
            # Common for newer/custom models. Fallback to cl100k_base is standard.
            logger.debug(f"Could not find encoding for model {model_name}. Using cl100k_base.")
            self.encoding = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        return len(self.encoding.encode(text))

    def truncate_text(self, text: str, max_tokens: int) -> str:
        """Truncate text to fit within max_tokens."""
        tokens = self.encoding.encode(text)
        if len(tokens) <= max_tokens:
            return text
            
        truncated_tokens = tokens[:max_tokens]
        return self.encoding.decode(truncated_tokens)

    def fit_context(self, 
                   mandatory_text: str, 
                   optional_text: str, 
                   max_total_tokens: int) -> str:
        """
        Fit context within token limit.
        Mandatory text is preserved. Optional text is truncated if needed.
        """
        mandatory_tokens = self.count_tokens(mandatory_text)
        remaining_tokens = max_total_tokens - mandatory_tokens
        
        if remaining_tokens <= 0:
            logger.warning("Mandatory text exceeds token limit! Returning only mandatory text.")
            return mandatory_text
            
        optional_tokens = self.count_tokens(optional_text)
        
        if optional_tokens <= remaining_tokens:
            return mandatory_text + optional_text
            
        truncated_optional = self.truncate_text(optional_text, remaining_tokens)
        return mandatory_text + truncated_optional
