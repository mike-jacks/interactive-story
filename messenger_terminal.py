import subprocess
import os
import queue
import threading
import tempfile
from time import sleep, time
from abc import ABC, abstractmethod
from text_color import TextColor
from utility import Utility
from sound import Sound
from animation import Animation

class MessageTerminal(ABC):
    """
    Abstract base class for a message terminal. This class provides the framework
    for a message display system in a terminal window.

    Attributes:
        window_name (str): The name of the terminal window.
        message_queue (queue.Queue): Queue for messages to be displayed.
        process (subprocess.Popen): Process used to execute terminal commands.
        keep_running (bool): Flag to keep the message processing thread running.
        messages (list[list[str]]): List of message lists to be displayed.
        thread (threading.Thread): Thread for processing and displaying messages.
        terminal_text_color (TextColor): Color used for the text in the terminal.
    """
     
    def __init__(self, window_name):
        """
        Initializes the message terminal with a window name.

        Parameters:
            window_name (str): The name to be assigned to the terminal window.
        """
        
        self.window_name = window_name
        self.message_queue = queue.Queue()
        self.process = None
        self.keep_running = True
        self.messages: list[list[str]] = [] # type: ignore
        self.thread = threading.Thread(target=self.process_messages, daemon=True)
        self.thread.start()
        self.terminal_text_color = self.message_terminal_text_color()
        
    @abstractmethod
    def message_terminal_text_color(self):
        """
        Abstract method to set the terminal text color.
        Must be implemented by subclasses.
        """
        
        pass
    
    def enqueue_messages(self, messages):
        """
        Adds a new list of messages to the queue to be displayed.

        Parameters:
            messages (list[str]): The messages to be added to the queue.
        """
        
        self.messages.append([])
        for message in messages:
            self.messages[-1].append(message)
    
    def display_messages_and_wait(self, animate: bool = False):
        """
        Displays messages from the last list added to the messages attribute and waits for user input.

        Parameters:
            animate (bool): If True, messages will be displayed with typing animation.
        """
        
        Utility.hide_cursor()
        # Generate a script to display all messages and wait for an input.
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.sh') as script_file:
            script_file.write("#!/bin/zsh\n")
            script_file.write("printf '\\e[8;27;150t'\n")
            script_file.write("clear\n")
            script_file.write(f'echo -n -e "\\033]0;{self.window_name}\\007"\n')
            script_file.write("tput civis\n")
            script_file.write("sleep 1\n")
            if animate:
                for message in self.messages[-1]:
                    script_file.write(f'echo -n "{self.terminal_text_color.value}{self.window_name.capitalize()}: ";')
                    self.animate_typing(message, script_file)
                    script_file.write(f'echo -n "\n";')
                    script_file.write("sleep 1\n")
            else:
                for message in self.messages[-1]:
                    script_file.write(f'echo "{self.terminal_text_color.value}{self.window_name.capitalize()}: {message}"\n')
            # Wait for an input to proceed
            script_file.write('echo "Press enter to continue..."\n')
            script_file.write('read varname\n')
            
            # AppleScript to close the terminal window
            script_file.write(f"osascript -e 'tell application \"Terminal\" to close (every window whose name contains \"{self.window_name}\")' &\n")
            
        # Make the script file executable
        os.chmod(script_file.name, 0o755)
        subprocess.run(['open', '-a', 'Terminal', script_file.name])
        sleep(2.3)
        Sound.play(Sound.MAC_OS_NOTIFICAITON_1_SOUND)
    
    def process_messages(self):
        """
        Constantly processes messages from the queue if available, displaying them in a new terminal window.
        """
        
        # Platform-specific command to open a new terminal window
        while self.keep_running:
            if not self.message_queue.empty():
                message = self.message_queue.get()
                self.display_messages_and_wait(message)
                sleep(1)
            else:
                sleep(0.1)
        
    def animate_typing(self, message, script_file, speed=0.02):
        """
        Simulates typing animation for a message and writes it to a script file.

        Parameters:
            message (str): The message to animate.
            script_file (file object): The temporary script file to write commands.
            speed (float): The speed of the typing animation.
        """
        
        for letter in message:
            # Directly use printf for each letter with proper escaping
            escaped_letter = letter.replace("'", "'\\''")  # Escape single quotes correctly
            script_file.write(f"printf '{escaped_letter}'; sleep {speed}; ") 
    
    def stop(self):
        """
        Stops the message processing thread and joins it to the main thread.
        """
        
        self.keep_running = False
        self.thread.join()
    
    def is_messages_terminal_open(self):
        """
        Checks if the terminal window with the specified window name is still open.

        Returns:
            bool: True if the window is open, False otherwise.
        """
        
        # Check if the window with given title is still open.
        script = f'''tell application "Terminal"
                        set windowList to every window whose name contains "{self.window_name}"
                        if (count of windowList) > 0 then
                            return true
                        else
                            return false
                        end if
                    end tell'''
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
        return "true" in result.stdout.strip()

    def wait_for_window_to_close(self, timeout=100):
        """
        Waits for the terminal window to close within a specified timeout.

        Parameters:
            timeout (int, optional): The timeout duration in seconds.

        Returns:
            bool: True if the window closed within the timeout, False otherwise.
        """

        timeout = float(timeout)
        start_time = time()
        while time() - start_time < timeout:
            if not self.is_messages_terminal_open():
                animated_text = f"You have disconnected from {self.window_name}'s messenger service..."
                disconnected_from_messenger_service_text_thread = Animation.animated_text(static_text="", animated_text=animated_text, end_text="\n", delay_between_chars=0.03)
                Sound.play(Sound.DIGITAL_TYPING, loop=int((len(animated_text)*0.03*10)+5), pause=0.083)
                disconnected_from_messenger_service_text_thread.stop(0.5)
                sleep(1)
                Utility.clear_screen()
                Utility.show_cursor()
                return True
            sleep(1)  # Poll every second
        print("Timeout waiting for window to close.")
        return False

class HackerMessenger(MessageTerminal):
    """
    Concrete class representing a hacker's message terminal.

    Inherits from MessageTerminal and implements message_terminal_text_color to return a green text color.
    """
    
    def __init__(self, window_name):
        """
        Initializes the hacker messenger with a specified window name.

        Parameters:
            window_name (str): The name to be assigned to the hacker's terminal window.
        """
        
        super().__init__(window_name)
    
    def message_terminal_text_color(self):
        """
        Overrides MessageTerminal's abstract method to set the terminal text color to green.

        Returns:
            TextColor: The green text color.
        """
        
        return TextColor.GREEN

class CorporationMessenger(MessageTerminal):
    """
    Concrete class representing a corporation's message terminal.

    Inherits from MessageTerminal and implements message_terminal_text_color to return a red text color.
    """
    
    def __init__(self, window_name):
        """
        Initializes the corporation messenger with a specified window name.

        Parameters:
            window_name (str): The name to be assigned to the corporation's terminal window.
        """
        
        super().__init__(window_name)
    
    def message_terminal_text_color(self):
        """
        Overrides MessageTerminal's abstract method to set the terminal text color to red.

        Returns:
            TextColor: The red text color.
        """
        
        return TextColor.RED