import os
import shutil
from .parser import parse_file
from .colors import Colors

class Presentation:
    def __init__(self, slides):
        self.slides = slides
        self.current_index = 0

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw_progress_bar(self):
        term_width = shutil.get_terminal_size().columns
        total = len(self.slides)
        current = self.current_index + 1
        
        # Create a visual bar like [====......]
        bar_length = 20
        filled_length = int(bar_length * current // total)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        
        status = f" Slide {current}/{total} "
        return f"[{bar}]{status}"

    def run(self):
        if not self.slides:
            print("No slides found.")
            return

        while True:
            self.clear_screen()
            slide = self.slides[self.current_index]
            print(slide.render())
            
            # Draw Footer
            print("\n" * 2)
            print(Colors.style("=" * shutil.get_terminal_size().columns, Colors.BLUE))
            print(self.draw_progress_bar() + "  [N]ext [P]rev [Q]uit")
            
            choice = input(">> ").lower().strip()
            
            if choice in ['n', '']:
                if self.current_index < len(self.slides) - 1:
                    self.current_index += 1
            elif choice == 'p':
                if self.current_index > 0:
                    self.current_index -= 1
            elif choice == 'q':
                self.clear_screen()
                break