import re

def secure_filename(filename: str) -> str:
    """
    Sanitizes a filename to prevent directory traversal and command injection.
    Only allows alphanumeric characters, dashes, underscores, and a single dot for extension.
    """
    if not filename:
        return "unnamed_file"
    
    # Keep only alphanumeric, dash, underscore, and dot
    filename = re.sub(r'[^a-zA-Z0-9_\-\.]', '', filename)
    
    # Prevent directory traversal
    filename = filename.lstrip('.')
    
    # Ensure no multiple dots or missing name
    if not filename:
        return "unnamed_file"
        
    return filename
