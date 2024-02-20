from datetime import datetime
import os, sys
import threading
from time import sleep

class Utility:
    """
    A utility class providing static methods for common system tasks such as clearing the screen, managing cursor visibility, and getting current time and date.
    """
    @staticmethod
    def get_current_time():
        """
        Gets the current system time.

        Returns:
            str: The current system time formatted as 'YYYY-MM-DD HH:MM:SS'.
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_current_date():
        """
        Gets the current system date.

        Returns:
            str: The current system date formatted as 'YYYY-MM-DD'.
        """
        return datetime.now().strftime("%Y-%m-%d")
    
    @staticmethod
    def clear_screen():
        """
        Clears the terminal screen.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def clear_line():
        """
        Clears the current line in the terminal.
        """
        sys.stdout.write("\033[2K\r")
        sys.stdout.flush()
    
    @staticmethod
    def clear_multi_line(string: str):
        """
        Clears multiple lines in the terminal based on the input string's line count.

        Args:
            string (str): The string whose lines should be cleared from the terminal.
        """
        num_lines = string.count("\n")
        sys.stdout.write(f"\033[{num_lines + 1}A")
        
    
    @staticmethod
    def hide_cursor():
        """
        Hides the cursor in the terminal.
        """
        print("\033[?25l", end="")
    
    @staticmethod
    def show_cursor():
        """
        Shows the cursor in the terminal.
        """
        print("\033[?25h", end="")
    

class ThreadControl:
    """
    A class to control the execution of a thread, providing methods to start and stop the thread.

    Attributes:
        target (Callable): The target function to be executed by the thread.
        args (tuple): Arguments to pass to the target function.
    """
    def __init__(self, target, *args):
        """
        Initializes a new instance of the ThreadControl class.

        Args:
            target (Callable): The target function to be executed by the thread.
            args: Variable length argument list for the target function.
        """
        self.target = target
        self.args = args
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target = self._run)
    
    def _run(self):
        """
        Internal method that runs the target function and passes the stop event to it.
        """
        self.target(self.stop_event)
    
    def start(self):
        """
        Starts the thread.
        """
        self.thread.start()
    
    def stop(self, wait_before_continueing_after_thread_stop_for = 0.0):
        """
        Signals the thread to stop and waits for it to finish.

        Args:
            wait_before_continuing_after_thread_stop_for (float, optional): Time in seconds to wait after the thread stops before continuing execution.
        """
        self.stop_event.set()
        self.thread.join()
        sleep(wait_before_continueing_after_thread_stop_for)