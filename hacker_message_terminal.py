import subprocess
import os
import queue
import threading
import tempfile
from time import sleep, time

class HackerMessageTerminal:
    
    
    def __init__(self, name):
        self.name = name
        self.message_queue = queue.Queue()
        self.process = None
        self.keep_running = True
        self.messages = []
        self.thread = threading.Thread(target=self.process_messages, daemon=True)
        self.thread.start()
    
    def enqueue_messages(self, messages):
        for message in messages:
            self.messages.append(message)
    
    def display_messages_and_wait(self):
        # Generate a script to display all messages and wait for an input.
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.sh') as script_file:
            script_file.write("#!/bin/zsh\n")
            script_file.write("clear\n")
            script_file.write(f'echo -n -e "\\033]0;{self.name}\\007"\n')
            for message in self.messages:
                script_file.write(f'echo "{message}"\n')
                script_file.write("sleep 1\n")
            # Wait for an input to proceed
            script_file.write('echo "Press enter to continue..."\n')
            script_file.write('read varname\n')
            
            # AppleScript to close the terminal window
            script_file.write(f"osascript -e 'tell application \"Terminal\" to close (every window whose name contains \"{self.name}\")' &\n")
            
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
        
    
    def stop(self):
        self.keep_running = False
        self.thread.join()
    
    
    @classmethod
    def is_messages_terminal_open(title):
        # Check if the window with given title is still open.
        script = f'''tell application "Terminal"
                        set windowList to every window whose name contains "{title}"
                        if (count of windowList) > 0 then
                            return true
                        else
                            return false
                        end if
                    end tell'''
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
        return "true" in result.stdout.strip()

    @classmethod
    def wait_for_window_to_close(title, timeout=60):
        """Wait for the Terminal window with the specified title to close."""
        start_time = time()
        while time() - start_time < timeout:
            if not HackerMessageTerminal.is_messages_terminal_open(title):
                print("Window closed, continuing...")
                return True
            sleep(1)  # Poll every second
        print("Timeout waiting for window to close.")
        return False