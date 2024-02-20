from enum import Enum
from random import choice

class TextColor(Enum):
    """
    An enumeration for different text colors using ANSI escape codes.

    Attributes:
        BLACK (str): ANSI code for black color.
        RED (str): ANSI code for red color.
        ORANGE (str): ANSI code for orange color.
        YELLOW (str): ANSI code for yellow color.
        GREEN (str): ANSI code for green color.
        BLUE (str): ANSI code for blue color.
        CYAN (str): ANSI code for cyan color.
        PURPLE (str): ANSI code for purple color.
        WHITE (str): ANSI code for white color.
        RESET (str): ANSI code to reset color to default.
        RAINBOW (list): List of ANSI codes for a spectrum of colors.
    """
    BLACK = '\033[30m'
    RED = '\033[38;5;9m'
    ORANGE = '\033[38;5;208m'
    YELLOW = '\033[38;5;11m'
    GREEN = '\033[38;5;10m'
    BLUE = '\033[38;5;12m'
    CYAN = '\033[38;5;43m'
    PURPLE = '\033[38;5;13m'
    WHITE = '\033[37m'
    RESET = '\033[0m'  # Resets the color to default.
    RAINBOW = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE]
    
    @classmethod
    def random(cls):
        """
        Selects and returns a random color from the TextColor enum, excluding the RAINBOW list itself.

        Returns:
            TextColor: An instance of the TextColor enum representing a random color.
        """
        return choice([color for color in cls if color != cls.RAINBOW])


 