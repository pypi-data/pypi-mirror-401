from .slide import Slide

def parse_file(filepath):
    """
    Reads a text file and splits it into Slide objects based on the '---' separator.
    """
    slides = []
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            full_text = f.read()
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return []
    
    # Split the text wherever we see "---"
    raw_slides = full_text.split("---")
    
    for raw_content in raw_slides:
        # .strip() removes extra whitespace from start/end
        clean_content = raw_content.strip()
        if clean_content: # Only add if there is text
            slides.append(Slide(clean_content))
        
    return slides