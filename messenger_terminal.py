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
     
    def __init__(self, window_name):
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
        pass
    
    def enqueue_messages(self, messages):
        self.messages.append([])
        for message in messages:
            self.messages[-1].append(message)
    
    def display_messages_and_wait(self, animate: bool = False):
        Utility.hide_cursor()
        # Generate a script to display all messages and wait for an input.
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.sh') as script_file:
            script_file.write("#!/bin/zsh\n")
            script_file.write("clear\n")
            script_file.write(f'echo -n -e "\\033]0;{self.window_name}\\007"\n')
            if animate:
                for message in self.messages[-1]:
                    script_file.write(f'echo -n "{self.terminal_text_color.value}{self.window_name}: ";')
                    self.animate_typing(message, script_file)
                    script_file.write(f'echo -n "\n";')
                    script_file.write("sleep 1\n")
            else:
                for message in self.messages[-1]:
                    script_file.write(f'echo "{self.terminal_text_color.value}{self.window_name}: {message}"\n')
            # Wait for an input to proceed
            script_file.write('echo "Press enter to continue..."\n')
            script_file.write('read varname\n')
            
            # AppleScript to close the terminal window
            script_file.write(f"osascript -e 'tell application \"Terminal\" to close (every window whose name contains \"{self.window_name}\")' &\n")
            
        # Make the script file executable
        os.chmod(script_file.name, 0o755)
        subprocess.run(['open', '-a', 'Terminal', script_file.name])
    
    def process_messages(self):
        # Platform-specific command to open a new terminal window
        while self.keep_running:
            if not self.message_queue.empty():
                message = self.message_queue.get()
                self.display_messages_and_wait(message)
                sleep(1)
            else:
                sleep(0.1)
        
    def animate_typing(self, message, script_file, speed=0.02):
        for letter in message:
            # Directly use printf for each letter with proper escaping
            escaped_letter = letter.replace("'", "'\\''")  # Escape single quotes correctly
            script_file.write(f"printf '{escaped_letter}'; sleep {speed}; ") 
    
    def stop(self):
        self.keep_running = False
        self.thread.join()
    
    def is_messages_terminal_open(self):
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

    def wait_for_window_to_close(self, timeout=60):
        """Wait for the Terminal window with the specified title to close."""
        timeout = float(timeout)
        start_time = time()
        while time() - start_time < timeout:
            if not self.is_messages_terminal_open():
                animated_text = f"You have discnnected from {self.window_name}'s messenger service..."
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
    def __init__(self, window_name):
        super().__init__(window_name)
    
    def message_terminal_text_color(self):
        return TextColor.GREEN

class CorporationMessenger(MessageTerminal):
    def __init__(self, window_name):
        super().__init__(window_name)
    
    def message_terminal_text_color(self):
        return TextColor.RED