"""
Text formatting utilities for FlawHunt CLI.
Handles markdown removal and text cleaning for better console output.
"""

import re

def strip_markdown(text: str) -> str:
    """
    Remove common markdown formatting from text for cleaner console output.
    
    Args:
        text: Input text with potential markdown formatting
        
    Returns:
        Clean text without markdown formatting
    """
    if not text:
        return text
    
    # Remove bold/italic markers
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # **bold**
    text = re.sub(r'\*([^*]+)\*', r'\1', text)      # *italic*
    text = re.sub(r'_([^_]+)_', r'\1', text)        # _italic_
    
    # Remove headers but keep the text
    text = re.sub(r'^#+\s*(.+)$', r'\1', text, flags=re.MULTILINE)
    
    # Remove code blocks but keep content
    text = re.sub(r'```[\w]*\n(.*?)\n```', r'\1', text, flags=re.DOTALL)
    text = re.sub(r'`([^`]+)`', r'\1', text)  # inline code
    
    # Remove links but keep text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    
    # Remove strikethrough
    text = re.sub(r'~~([^~]+)~~', r'\1', text)
    
    # Clean up extra whitespace
    text = re.sub(r'\n\s*\n', '\n\n', text)  # Multiple empty lines to double
    text = re.sub(r'[ \t]+', ' ', text)      # Multiple spaces/tabs to single space
    
    # Remove leading/trailing whitespace from lines
    lines = text.split('\n')
    cleaned_lines = [line.strip() for line in lines]
    text = '\n'.join(cleaned_lines)
    
    return text.strip()

def format_for_console(text: str, width: int = 80) -> str:
    """
    Format text for console display with proper wrapping.
    
    Args:
        text: Input text
        width: Maximum line width
        
    Returns:
        Formatted text suitable for console display
    """
    if not text:
        return text
    
    # First strip markdown
    clean_text = strip_markdown(text)
    
    # Simple word wrapping
    words = clean_text.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        word_length = len(word)
        
        # Check if adding this word would exceed width
        if current_length + word_length + len(current_line) > width:
            if current_line:  # If we have words in current line
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = word_length
            else:  # Single word is too long, just add it
                lines.append(word)
                current_length = 0
        else:
            current_line.append(word)
            current_length += word_length
    
    # Add remaining words
    if current_line:
        lines.append(' '.join(current_line))
    
    return '\n'.join(lines)

def clean_ai_response(response: str, preserve_formatting: bool = True) -> str:
    """
    Clean AI response for better display in FlawHunt CLI.
    
    Args:
        response: Raw AI response potentially containing markdown
        preserve_formatting: If True, preserve original line breaks and spacing
        
    Returns:
        Cleaned response suitable for console display
    """
    if not response:
        return response
    
    # Strip markdown formatting but preserve structure
    clean = strip_markdown_preserve_structure(response) if preserve_formatting else strip_markdown(response)
    
    # Remove common AI response prefixes
    prefixes_to_remove = [
        "Final Answer:",
        "Answer:",
        "Response:",
        "Here's the answer:",
        "Here is the answer:",
    ]
    
    for prefix in prefixes_to_remove:
        if clean.strip().startswith(prefix):
            clean = clean.strip()[len(prefix):].strip()
    
    # Only apply word wrapping if preserve_formatting is False
    if not preserve_formatting:
        formatted = format_for_console(clean, width=85)
        return formatted
    
    return clean

def strip_markdown_preserve_structure(text: str) -> str:
    """
    Remove markdown formatting while preserving original line breaks and structure.
    
    Args:
        text: Input text with potential markdown formatting
        
    Returns:
        Clean text without markdown but with preserved formatting
    """
    if not text:
        return text
    
    # Remove bold/italic markers
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # **bold**
    text = re.sub(r'\*([^*]+)\*', r'\1', text)      # *italic*
    text = re.sub(r'_([^_]+)_', r'\1', text)        # _italic_
    
    # Remove headers but keep the text and preserve line structure
    text = re.sub(r'^#+\s*(.+)$', r'\1', text, flags=re.MULTILINE)
    
    # Remove code blocks but keep content and structure
    text = re.sub(r'```[\w]*\n(.*?)\n```', r'\1', text, flags=re.DOTALL)
    text = re.sub(r'`([^`]+)`', r'\1', text)  # inline code
    
    # Remove links but keep text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    
    # Remove strikethrough
    text = re.sub(r'~~([^~]+)~~', r'\1', text)
    
    # Clean up only excessive whitespace but preserve intentional formatting
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)  # Triple+ newlines to double
    text = re.sub(r'[ \t]+', ' ', text)            # Multiple spaces/tabs to single space
    
    return text.strip()
