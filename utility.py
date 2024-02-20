from datetime import datetime
import os, sys
import threading
from time import sleep

class Utility:
    @staticmethod
    def get_current_time():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_current_date():
        return datetime.now().strftime("%Y-%m-%d")
    
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def clear_line():
        sys.stdout.write("\033[2K\r")
        sys.stdout.flush()
    
    @staticmethod
    def clear_multi_line(string: str):
        num_lines = string.count("\n")
        sys.stdout.write(f"\033[{num_lines + 1}A")
        
    
    @staticmethod
    def hide_cursor():
        print("\033[?25l", end="")
    
    @staticmethod
    def show_cursor():
        print("\033[?25h", end="")
    

class ThreadControl:
    def __init__(self, target, *args):
        self.target = target
        self.args = args
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target = self._run)
    
    def _run(self):
        self.target(self.stop_event)
    
    def start(self):
        self.thread.start()
    
    def stop(self, wait_before_continueing_after_thread_stop_for = 0.0):
        self.stop_event.set()
        self.thread.join()
        sleep(wait_before_continueing_after_thread_stop_for)