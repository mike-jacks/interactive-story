from time import sleep
from utility import Utility, ThreadControl
from text_color import TextColor
from random import choice
import sys
class Animation:
    """
    This class provides methods to create text animations in the console.
    It uses various text colors and can animate the text with a typing effect.
    """

    @staticmethod
    def animated_text(static_text: str = "", animated_text: str = "...", end_text:str = "", static_text_color: TextColor = TextColor.RESET, animated_text_color: TextColor = TextColor.RESET, end_text_color: TextColor = TextColor.RESET, delay_between_chars: float = 0.1, stop_event = None, continue_thread_after_stop_for = 0.001):
        """
        Prints animated text to the console with specified colors and delays.

        Parameters:
        - static_text (str): Text to remain static before the animated text.
        - animated_text (str): Text to be animated, like a loading spinner.
        - end_text (str): Text to display after the animation ends.
        - static_text_color (TextColor): Color of the static text.
        - animated_text_color (TextColor): Color of the animated text.
        - end_text_color (TextColor): Color of the end text.
        - delay_between_chars (float): Time in seconds between each character's animation.
        - stop_event (threading.Event): Event to stop the animation thread externally.
        - continue_thread_after_stop_for (float): Time in seconds to continue the thread after a stop event is set.

        Returns:
        ThreadControl: A thread control object for the animation thread.
        """
        def animated_text_thread(stop_event=None):
            """
            Inner function that runs the animation loop. This function is designed to be run in a separate thread to allow asynchronous text animation.

            Parameters:
            - stop_event (threading.Event): Event to stop the animation thread externally.
            """
            while True:
                if stop_event and stop_event.is_set():
                    break
                Utility.clear_line()
                static_text_with_color = ""
                if static_text_color == TextColor.RAINBOW:
                    rainbow_index = 0
                    for letter in static_text:
                        static_text_with_color += static_text_color.value[rainbow_index] + letter + TextColor.RESET.value
                        rainbow_index += 1
                        if rainbow_index == len(TextColor.RAINBOW.value):
                            rainbow_index = 0
                else:
                    static_text_with_color = f"{static_text_color.value}{static_text}{TextColor.RESET.value}"
                sys.stdout.write(static_text_with_color)
                sys.stdout.flush()
                #print(f"{static_text_with_color}", end="")
                sleep(delay_between_chars)
                animated_text_with_color = ""
                rainbow_index = rainbow_index if static_text_color == TextColor.RAINBOW else 0
                for i in range(len(animated_text)):
                    if animated_text_color == TextColor.RAINBOW:
                        animated_text_with_color += animated_text_color.value[rainbow_index] + animated_text[i] + TextColor.RESET.value
                        rainbow_index += 1
                        if rainbow_index == len(TextColor.RAINBOW.value):
                            rainbow_index = 0
                        Utility.clear_line()
                        sys.stdout.write(static_text_with_color + animated_text_with_color)
                        sys.stdout.flush()
                        #print(static_text_with_color + animated_text_with_color, end="")
                        sleep(delay_between_chars)
                    else:
                        animated_text_with_color += f"{animated_text_color.value}{animated_text[i]}{TextColor.RESET.value}"
                        Utility.clear_line()
                        sys.stdout.write(static_text_with_color + animated_text_with_color)
                        sys.stdout.flush()
                        #print(f"{static_text_with_color}{animated_text_with_color}", end="")
                        sleep(delay_between_chars)
            if end_text_color == TextColor.RAINBOW:
                if animated_text_color == TextColor.RAINBOW:
                    rainbow_index = rainbow_index if animated_text_color == TextColor.RAINBOW else 0
                elif static_text_color == TextColor.RAINBOW:
                    rainbow_index = rainbow_index if static_text_color == TextColor.RAINBOW else 0
                else:
                    rainbow_index = 0
                end_text_with_color = ""
                for letter in end_text:
                    end_text_with_color += end_text_color.value[rainbow_index] + letter + TextColor.RESET.value
                    rainbow_index += 1
                    if rainbow_index == len(TextColor.RAINBOW.value):
                        rainbow_index = 0
            else:
                end_text_with_color = f"{end_text_color.value}{end_text}{TextColor.RESET.value}"
            sys.stdout.write(end_text_with_color)
            sys.stdout.flush()
            #print("", end=end_text_with_color)
        animation_thread = ThreadControl(animated_text_thread, stop_event)
        animation_thread.start()
        sleep(continue_thread_after_stop_for)
        return animation_thread