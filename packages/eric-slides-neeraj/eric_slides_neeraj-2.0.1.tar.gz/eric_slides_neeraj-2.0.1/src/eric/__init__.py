import sys
import os
from .parser import parse_file
from .core import Presentation

def start(filepath):
    """
    Helper function to run a presentation immediately.
    Usage: eric.start("my_presentation.txt")
    """
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        return

    slides = parse_file(filepath)
    app = Presentation(slides)
    app.run()

def start_cli():
    """
    Entry point for the command line 'eric' tool.
    """
    if len(sys.argv) < 2:
        print("Usage: eric <filename>")
        print("Example: eric demo.txt")
        return
    
    # The first argument (sys.argv[1]) is the filename provided by the user
    start(sys.argv[1])