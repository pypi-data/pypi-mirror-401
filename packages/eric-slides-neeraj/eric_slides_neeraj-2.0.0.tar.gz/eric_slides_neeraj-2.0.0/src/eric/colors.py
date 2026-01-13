class Colors:
    HEADER = '\033[95m' # Pink/Magenta
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m' # Yellow
    FAIL = '\033[91m'    # Red
    END = '\033[0m'      # Reset color
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def style(text, color_code):
        return f"{color_code}{text}{Colors.END}"