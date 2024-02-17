from time import sleep
from utility import Utility, ThreadControl
from text_color import TextColor
from random import choice

class Animation:

    @staticmethod
    def animated_text(static_text: str, animated_text: str = "...", end_text:str = "", static_text_color: TextColor = TextColor.RESET, animated_text_color: TextColor = TextColor.RESET, end_text_color: TextColor = TextColor.RESET, delay_between_chars: float = 0.1, stop_event = None, continue_thread_after_stop_for = 0.001):
        def animated_text_thread(stop_event=None):
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
                print(f"{static_text_with_color}", end="")
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
                        print(static_text_with_color + animated_text_with_color, end="")
                        sleep(delay_between_chars)
                    else:
                        animated_text_with_color += f"{animated_text_color.value}{animated_text[i]}{TextColor.RESET.value}"
                        Utility.clear_line()
                        print(f"{static_text_with_color}{animated_text_with_color}", end="")
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
            print("", end=end_text_with_color)
        animation_thread = ThreadControl(animated_text_thread, stop_event)
        animation_thread.start()
        sleep(continue_thread_after_stop_for)
        return animation_thread