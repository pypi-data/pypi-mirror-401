import shutil
from .colors import Colors

class Slide:
    def __init__(self, content):
        self.content = content

    def highlight_syntax(self, line):
        """Adds colors to specific keywords to look like a code editor."""
        keywords = {
            "def ": Colors.BLUE,
            "class ": Colors.BLUE,
            "import ": Colors.HEADER, # Magenta/Pink
            "from ": Colors.HEADER,
            "return ": Colors.WARNING,
            "print": Colors.CYAN,
            "# ": Colors.GREEN # Comments
        }
        
        # Check for Headers (Markdown style)
        if line.strip().startswith("#"):
            return Colors.style(line, Colors.BOLD + Colors.CYAN)

        # Check for Code Keywords
        for key, color in keywords.items():
            if key in line:
                line = line.replace(key, f"{color}{key}{Colors.END}")
        
        return line

    def render(self):
        terminal_size = shutil.get_terminal_size()
        width = terminal_size.columns
        height = terminal_size.lines

        lines = self.content.split('\n')
        
        # Calculate vertical padding to center text
        content_height = len(lines)
        # Reserve 4 lines for the footer/header space
        vertical_padding = max(0, (height - content_height - 4) // 2)
        
        output = []
        output.append('\n' * vertical_padding)

        for line in lines:
            styled_line = self.highlight_syntax(line)
            # We center based on the original length (ignoring invisible color codes)
            padding = max(0, (width - len(line)) // 2)
            centered_line = " " * padding + styled_line
            output.append(centered_line)
        
        return "\n".join(output)