from enum import Enum
from random import choice

def get_random_color():
    return choice(TextColor.RAINBOW.value)

class TextColor(Enum):
    BLACK = '\033[30m'
    RED = '\033[38;5;9m'
    ORANGE = '\033[38;5;208m'
    YELLOW = '\033[38;5;11m'
    GREEN = '\033[38;5;10m'
    BLUE = '\033[38;5;12m'
    PURPLE = '\033[38;5;13m'
    WHITE = '\033[37m'
    RESET = '\033[0m'  # Resets the color to default.
    RAINBOW = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, WHITE]
    
    @classmethod
    def random(cls):
        return choice([color for color in cls if color != cls.RAINBOW])


 