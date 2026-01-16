"""Response parsing utilities."""

import re


def parse_response(raw_text):
    """
    Parse a response text to extract thought and spoken content.
    
    The model uses [THOUGHT]...[/THOUGHT] tags to separate internal
    monologue from spoken response.
    
    Args:
        raw_text (str): Raw response text from the model
        
    Returns:
        tuple: (thought_content, spoken_content)
    """
    if not raw_text: 
        return "Thinking...", "..."
    
    # 1. Global cleanup: Remove all markdown bolding (**). 
    clean_text = raw_text.replace("**", "")

    # 2. Define a "Flexible" Regex Pattern
    pattern = r"\[\s*THOUGHT\s*\](.*?)\[\s*/\s*THOUGHT\s*\]"
    match = re.search(pattern, clean_text, re.DOTALL | re.IGNORECASE)
    
    if match:
        thought_content = match.group(1).strip()
        spoken_content = re.sub(pattern, "", clean_text, flags=re.DOTALL | re.IGNORECASE).strip()
    else:
        start_pattern = r"\[\s*THOUGHT\s*\]"
        start_match = re.search(start_pattern, clean_text, re.IGNORECASE)
        
        if start_match:
            thought_content = clean_text.replace(start_match.group(0), "").strip()
            spoken_content = "..." # Model got stuck in thought loop
        else:
            thought_content = "No internal monologue detected."
            spoken_content = clean_text.strip()
            
    if not spoken_content: 
        spoken_content = "..."
        
    return thought_content, spoken_content

