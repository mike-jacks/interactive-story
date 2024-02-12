import threading
import sys
from time import sleep
from utility import Utility, ThreadControl

class Animation:
    
    @staticmethod
    def text_animating_after_static_text(message: str, animated_text: str = "...", end_text:str = "", delay_animation: float = 0.1, stop_event = None, hold_thread_for = 0.0):
        def text_animating_after_static_text_thread(stop_event=None):
            while True:
                if stop_event and stop_event.is_set():
                    break
                Utility.clear_line()
                print(message, end="")
                sleep(delay_animation)
                for i in range(len(animated_text)):
                    Utility.clear_line()
                    print(message + animated_text[:i+1], end="")
                    sleep(delay_animation)
            print("", end=end_text)
        animation_thread = ThreadControl(text_animating_after_static_text_thread, stop_event)
        animation_thread.start()
        sleep(hold_thread_for)
        return animation_thread