from time import sleep
from utility import Utility, ThreadControl

class Animation:
    
    @staticmethod
    def animated_text(static_text: str, animated_text: str = "...", end_text:str = "", delay_between_chars: float = 0.1, stop_event = None, continue_thread_after_stop_for = 0.0):
        def animated_text_thread(stop_event=None):
            while True:
                if stop_event and stop_event.is_set():
                    break
                Utility.clear_line()
                print(static_text, end="")
                sleep(delay_between_chars)
                for i in range(len(animated_text)):
                    Utility.clear_line()
                    print(static_text + animated_text[:i+1], end="")
                    sleep(delay_between_chars)
            print("", end=end_text)
        animation_thread = ThreadControl(animated_text_thread, stop_event)
        animation_thread.start()
        sleep(continue_thread_after_stop_for)
        return animation_thread