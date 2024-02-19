import json
import glob, os
from utility import Utility
from text_color import TextColor
from ascii_animation import play_ascii_animation, load_ascii_art_animation_from_json
from time import sleep, time
from messenger_terminal import HackerMessenger, CorporationMessenger, MessageTerminal
from animation import Animation
from sound import Sound

class User:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
    
    def __repr__(self) -> str:
        return f"User: {self.username})"
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, User) and self.username == other.username and self.password == other.password

class Terminal:
    terminals: list['Terminal'] = []
    messengers: list[MessageTerminal] = [HackerMessenger("Hacker")]
    hacker_messages: list[list[str]] = [[]]

    def __init__(self, terminal_name: str, terminal_ip_address: str, terminal_username = None, terminal_password = None, is_user_terminal = False) -> None:
        self.terminal_name = terminal_name
        self.terminal_ip_address = terminal_ip_address
        self.filesystem_filename = f"./filesystems/{terminal_name}_filesystem.json"
        self.filesystem_exists = os.path.exists(self.filesystem_filename)
        self.valid_users: list[User] = []
        self.active_user = None
        self.messenger = CorporationMessenger(terminal_name)
        self.messenger_messages: list[list[str]] = [[]]
        self.in_ssh_session = False
        self.is_user_terminal = is_user_terminal
        Terminal.messengers.append(self.messenger)
        
        if self.filesystem_exists:
            self.filesystem = self.load_filesystem()
            self.ensure_password_file_exists()
            self.valid_users = self.load_valid_users()
            terminal_password = self.filesystem["/"]["etc"][".passwd"]
            if terminal_username and terminal_password:
                self.login_user(terminal_username, terminal_password)
        else:
            if terminal_username and terminal_password:
                # Use provided credentials to create a new user and filesystem
                self.create_user(terminal_username, terminal_password)
            else:
                # No filesystem exists, prompt to create a new user
                self.prompt_for_create_user()
        # self.messeges = [[str]]
        # self.new_message = False
        Terminal.terminals.append(self)
        self.exit_requested = False
        self.commands = self.get_commands()
    
    def ensure_password_file_exists(self):
        # Ensure the "etc" directory exists
        if "etc" not in self.filesystem["/"]:
            self.filesystem["/"]["etc"] = {}
        
        # Check if the password file exists: if not, create it with a user asked password:
        if ".passwd" not in self.filesystem["/"]["etc"]:
            self.filesystem["/"]["etc"][".passwd"] = ""
            self.save_filesystem()
    
    
    def get_commands(self):
        return {
            "pwd": self.pwd,
            "ls": self.ls,
            "cd": self.cd,
            "mkdir": self.mkdir,
            "touch": self.touch,
            "unzip": self.unzip,
            "echo": self.echo,
            "find": self.find,
            "cat": self.cat,
            "open": self.open_file,
            "rm": self.rm,
            "rmdir": self.rmdir,
            "ifconfig": self.ifconfig,
            "ssh": self.ssh,
            "download": self.download,
            "setpasswd": self.set_password,
            "messenger": self.messenger_window,
            "clear": self.clear_screen,
            "help": self.terminal_help,
            "resetgame": self.reset_game,
            "exit": self.exit,
        }
    
    def messenger_window(self, args=[]):
        # display hacker messenger window with the last item in the messages list
        if self.hacker_messages:
            login_text_thread = Animation.animated_text(static_text="Launching messenger service", animated_text="...", end_text="\n", delay_between_chars=0.3, continue_thread_after_stop_for=2)
            login_text_thread.stop(0.5)
            Utility.clear_screen()
            hacker_terminal = Terminal.messengers[0]
            hacker_terminal.enqueue_messages(self.hacker_messages[-1])
            hacker_terminal.display_messages_and_wait()
            sleep(2)
            hacker_terminal.wait_for_window_to_close()
    
    def prompt_for_login(self):
        Utility.hide_cursor()
        animated_text = "Please log in."
        login_text_thread = Animation.animated_text(static_text="", animated_text=animated_text, end_text="\n", delay_between_chars=0.03)
        Sound.play(Sound.DIGITAL_TYPING, loop=int((len(animated_text)*0.03*10)), pause=0.083)
        login_text_thread.stop(0.5)
        Utility.show_cursor()
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        self.login_user(username, password)
        
    def prompt_for_create_user(self):
        Utility.hide_cursor()
        animated_text = "You need to create a new user before being able to login."
        create_new_user_text_thread = Animation.animated_text(static_text="", animated_text=animated_text, end_text="\n", delay_between_chars=0.03)
        Sound.play(Sound.DIGITAL_TYPING, loop=int((len(animated_text)*0.03*10)+4), pause=0.083)
        create_new_user_text_thread.stop(0.5)
        Utility.show_cursor()
        username = input("Create username: ")
        password = input("Create password: ")
        self.create_user(username, password)
        Utility.clear_screen()
    
    def add_user(self, username: str, password: str) -> None:
        self.valid_users.append(User(username, password))
    
    def load_filesystem(self):
        try:
            with open(self.filesystem_filename) as file:
                return json.load(file)
        except FileNotFoundError:
            return self.create_new_filesystem() # Create a new filesystem and immediately use it if one does not exist
    
    def save_filesystem(self, filesystem=None):
        filesystem = filesystem or self.filesystem
        
        # Check if the filesystems directory exists, create it if not
        if not os.path.exists("./filesystems"):
            os.makedirs("./filesystems")
        with open(self.filesystem_filename, "w") as file:
            json.dump(filesystem, file, indent=4)
            
    def create_new_filesystem(self):
        base_structure = {
            "/": {
                "home": {},
                "etc": {
                    ".passwd": ""
                    },
                "var": {},
                "tmp": {},
                "bin": {
                    "pwd":None,
                    "ls":None,
                    "cd":None,
                    "mkdir":None,
                    "touch":None,
                    "cat":None,
                    "open":None,
                    "rm":None,
                    "rmdir":None,
                    "ifconfig":None,
                    "ssh":None,
                    "help":None,
                    "resetgame":None,
                    "exit":None
                    },
                "dev": {},
                "lib": {},
                "mnt": {},
                "opt": {},
                "proc": {},
                "root": {},
                "sbin": {},
                "srv": {},
                "sys": {},
                "usr": {}
                }
            }
        return base_structure
    
    def load_valid_users(self):
        valid_users = []
        home_dirs = self.filesystem.get("/", {}).get("home", {})
        for username, _ in home_dirs.items():
            password_file_path = f"/etc/.passwd"
            password = self.get_file_content(password_file_path)
            if password is not None:
                valid_users.append(User(username, password))
        return valid_users
    
    def get_file_content(self, file_path):
        parts = file_path.strip("/").split("/")
        node = self.filesystem["/"]
        for part in parts:
            if part in node:
                node = node[part]
            else:
                return None #File not found
        return node

    def login_user(self, username, password):
        user_found = False
        for user in self.valid_users:
            if user.username == username and user.password == password:
                self.active_user = user
                self.current_path = f"/home/{self.active_user.username}"
                user_found = True
                if self.is_user_terminal:
                    Utility.hide_cursor()
                    Utility.clear_screen()
                    animated_text = f"Logged in as {user.username}!"
                    logged_in_as_text_thread = Animation.animated_text(static_text="", animated_text=animated_text, end_text="\n", delay_between_chars=0.03)
                    Sound.play(Sound.DIGITAL_TYPING, loop=int((len(animated_text)*0.03*10)+2), pause=0.083)
                    logged_in_as_text_thread.stop(0.5)
                    sleep(1)
                return True
        if not user_found:
            Utility.hide_cursor()
            animated_text = "Login failed. Invalid username or password."
            create_new_user_text_thread = Animation.animated_text(static_text="", animated_text=animated_text, end_text="\n", delay_between_chars=0.03)
            Sound.play(Sound.DIGITAL_TYPING, loop=int((len(animated_text)*0.03*10)+4), pause=0.083)
            create_new_user_text_thread.stop(0.5)
            self.active_user = None
            return False
        return user_found
    
    def create_user(self, username, password):
        if any(user.username == username for user in self.valid_users):
            print(f"User '{username}' already exists. Please login.")
            return False
        
        # Create and add the new user
        user = User(username, password)
        self.valid_users.append(user)
        
        # Initialize filesystem if it does not exist
        if not self.filesystem_exists:
            self.filesystem = self.create_new_filesystem()
            
        # Ensure the etc directory and password file exist before creating a user:
        self.ensure_password_file_exists()
        # Update the password file with the new user's password
        self.filesystem["/"]["etc"][".passwd"] = password
        
        # Create home directory for the new user 
        self.create_user_home_directory(username)
        
        # Set the newly created user as the active user
        self.active_user = user
        self.current_path = f"/home/{self.active_user.username}"
        
        # Save the updated filesystem
        self.save_filesystem()
        return True
    
    def create_user_home_directory(self, username):
        # Ensure the "home" directory exists
        if "home" not in self.filesystem["/"]:
            self.filesystem["/"]["home"] = {}
            
        # Create the new user's home directories
        base_dirs = ["Desktop", "Documents", "Downloads", "Movies", "Music", "Pictures"]
        user_home = {dir_name: {} for dir_name in base_dirs}
        self.filesystem["/"]["home"][username] = user_home
        self.save_filesystem()

    def execute(self, command):
        trimmed_command = command.strip()
        if not trimmed_command:
            return
        args = trimmed_command.split()
        action = args[0]
        try:
            if action in self.commands:
                self.commands[action](args[1:] if len(args) > 1 else [])
            else:
                print("Command not found")
        except Exception as e:
            print(f"Error executing command: {e}")

    def pwd(self, args=[]):
        if not self.active_user:
            print("Error: No active session. Please log in.")
            return
        if args:
            print("pwd does not take any arguments")
            return
        print(self.current_path)

    def ls(self, args=[]):
        show_all = '-a' in args or '-al' in args # Check if '-a' or '-al' flag is present in command arguments
        
        # Start from the root of the filesystem
        node = self.filesystem["/"]
        
        # If not in the root directory, navigate to the current directory
        if self.current_path != "/":
            parts = self.current_path.strip("/").split("/")  # Remove leading '/' and split
            for part in parts:
                if part and part in node:  # Check each part of the path exists in the filesystem
                    node = node[part]
                else:
                    print(f"Directory '{part}' not found.")
                    return
        
        # List the contents of the current directory
        if isinstance(node, dict):
            for item in node:
                if not show_all and item.startswith("."):
                    continue # Skip hidden files and directories unles -a or -al flag is present
                elif item.endswith(".zip"):
                    print(f"{TextColor.YELLOW.value}{item}{TextColor.RESET.value}", end=" ")
                elif not isinstance(node[item], dict): # it's a file
                    print(f"{TextColor.WHITE.value}{item}{TextColor.RESET.value}", end=" ") # File printed to console
                else: # it's a directory
                    print(f"{TextColor.BLUE.value}{item}{TextColor.RESET.value}", end=" ") # Directory printed to console
        elif node is None:
            # The current node is a file, not a directory
            print("Current path is a file, not a directory")
        print("\n") # Print a newline after listing the contents
    
    def navigate_to(self, new_path):
        # Normalize the new path for absolute paths or construct one for relative paths
        if not new_path.startswith("/"):
            # For relative paths, append the new path to the current_path
            new_path = (self.current_path if self.current_path.endswith("/") else self.current_path + "/") + new_path
        
        # Split the path into parts, ignoring empty strings that result from consecutive slashes
        parts = list(filter(None, new_path.split("/")))
        
        # Start from the root of the filesystem and initialize an empty path to build upon
        node = self.filesystem["/"]
        temp_path = "/"
        
        for part in parts:
            # For each part of the path, try to navigate down the filesystem hierarchy
            if part in node:
                if not isinstance(node[part], dict):
                    print(f"{part}' is a file, not a directory.")
                    return
                node = node[part]
                temp_path += ("" if temp_path.endswith("/") else "/") + part
            else:
                print(f"Directory '{part}' not found.")
                return
        
        # Update the current path if navigation was successful
        # Remove the trailing slash for consistency except for the root directory
        self.current_path = temp_path
    
    def cd(self, args):
        if not args:
            print("No directory specified")
            return
        
        new_path = args[0]
        if new_path == "..":
            # Move up to the parent directory, but not above the root directory
            if self.current_path != "/":
                self.current_path = "/".join(self.current_path.rstrip("/").split("/")[:-1])
                self.current_path = self.current_path if self.current_path else "/"
        elif new_path == "~":
            # Reset to home directory
            self.current_path = f"/home/{self.active_user.username}" if self.active_user else "/home"
        else:
            self.navigate_to(new_path)

    def mkdir(self, args):
        if not args:
            print("No directory name specified")
            return
        new_dir = args[0]
        node = self.filesystem["/"]
        parts = self.current_path.strip("/").split("/")
        for part in parts:
            if part in node:
                node = node[part]
            else:
                print(f"Path '{'/'.join(parts)}' not found.")
        if new_dir in node:
            print(f"Directory '{new_dir}' already exists.")
            return
        elif self.current_path == "/home":
            print(f"Cannot create directory in {self.current_path.lstrip("/")} directory. This is a protected directory.")
        else:
            node[new_dir] = {}
        self.save_filesystem()
    
    def touch(self, args):
        if not args:
            print("No file name specified")
            return
        file_path = args[0]

        # Determine if the path is absolute or relative
        if file_path.startswith("/"):
            # Absolute path
            full_path = file_path.strip("/")
        else:
            # Relative path: combine current path
            full_path = os.path.join(self.current_path, file_path).strip("/")
        
        # Split the full path into parts and traverse the filesystem
        dir_path, filename = os.path.split(full_path)
        
        # Get the node for the directory containing the file
        dir_node = self._get_node_by_path(dir_path)
        if dir_node is None:
            print(f"Path '{dir_path}' not found.")
            return
        if not isinstance(dir_node, dict):
            print(f"Path '{dir_path}' is not a directory.")
            return
        
        # Check if the file exists and if its content is different
        if filename in dir_node:
            if isinstance(dir_node[filename], dict):
                print(f"'{filename}' is an existing directory.")
            else:
                print(f"File '{filename}' already exists.")
        else:
            dir_node[filename] = None
            print(f"File '{filename}' created successfully.")
        self.save_filesystem()
    
    def cat(self, args):
        if not args:
            print("Usage: cat <filename or path>")
            return
        
        filename = args[0]
        # Determine the full path to the file
        if filename.startswith("/"):
            parts = filename.strip("/").split("/")
            file_name = parts.pop()
            node = self.filesystem["/"]
        else:
            # Relative path
            parts = (self.current_path.strip("/") + "/" + filename).strip("/").split("/")
            file_name = parts.pop()
            node = self.filesystem["/"]
        
        # Split the full path into parts and traverse the filesystem
        for part in parts:
            if part in "":
                continue # Skip empty parts from consecutive slashes
            if part in node:
                node = node[part]
            else:
                print(f"Path '{'/'.join(parts)}' not found.")
                return
        
        # Check if the file exists and print its content
        if file_name in node and file_name.endswith(".zip"):
            print(f"'{file_name}' is a zipped directory. Use 'unzip' to extract its contents.")
        elif file_name in node and isinstance(node[file_name], str) and node[file_name]:
            print(rf"{node[file_name]}")
        elif file_name in node and isinstance(node[file_name], str) and not node[file_name]:
            print(f"{file_name} is not a readable file.")
        elif file_name in node and isinstance(node[file_name], list):
            print(f"'{file_name}' is a movie. Try using open instead.")
        elif file_name in node and isinstance(node[file_name], dict):
            print(f"{file_name} is a directory.")
        else:
            print(f"File '{file_name}' not found.")
    
    def open_file(self, args):
        if not args:
            print("No file name specified")
            return

        filename = args[0]
        # Determine the full path to the file
        if filename.startswith("/"):
            parts = filename.strip("/").split("/")
            file_name = parts.pop()
            node = self.filesystem["/"]
        else:
            # Relative path
            parts = (self.current_path.strip("/") + "/" + filename).strip("/").split("/")
            file_name = parts.pop()
            node = self.filesystem["/"]
        
        # Split the full path into parts and traverse the filesystem
        for part in parts:
            if part in "":
                continue # Skip empty parts from consecutive slashes
            if part in node:
                node = node[part]
            else:
                print(f"Path '{'/'.join(parts)}' not found.")
                return
        if file_name in node and file_name.endswith(".zip"):
            print(f"'{file_name}' is a zipped directory. Use 'unzip' to extract its contents.")
        elif file_name in node and isinstance(node[file_name], str):
            print(node[file_name])
        elif file_name in node and isinstance(node[file_name], list):
            Utility.clear_screen()
            Utility.hide_cursor()
            play_ascii_animation(node[file_name], frames_per_second=12, loop_num_times=-2)
            Utility.show_cursor()
        elif file_name in node and isinstance(node[file_name], dict):
            print(f"{file_name} is a directory.")
        elif file_name in node and isinstance(node[file_name], None):
            print(f"'{file_name}' is not a readable file.")
        else:
            print(f"File '{file_name}' not found.")
    
    def rm(self, args):
        if not args:
            print("No file name specified")
            return
        
        # Check for '-r' or '-rf' flag for recursive deltion
        recursive = '-r' in args or '-rf' in args
        # Remove the flag from the args list if present
        args = [arg for arg in args if arg not in ['-r', '-rf']]
        if not args:
            print("No file name specified after flags.")
            return
        file_path = args[0]
        
        full_path = os.path.join(self.current_path, file_path) if not file_path.startswith('/') else file_path
        parts = full_path.strip('/').split('/')
        filename = parts.pop()
        parent_path = '/'.join(parts)
        parent_node = self._get_node_by_path(parent_path)

        if parent_node is None:
            print(f"Path '{parent_path}' not found.")
            return 
            
        # Delete the target file or directory
        if filename in parent_node:
            if filename in parent_node and filename.endswith(".zip"):
                del parent_node[filename]
                print(f"File '{filename}' has been deleted.")
            elif isinstance(parent_node[filename], dict) and not recursive:
                print(f"'{filename}' is a directory. Use '-rf' to remove directories.")
            else:
                del parent_node[filename]
                print(f"File '{filename}' has been deleted.")
        else:
            print(f"File '{filename}' not found.")
        self.save_filesystem()
            
            
            
    def rmdir(self, args):
        if not args:
            print("No directory name specified")
            return
        
        # Check for '-r' or '-rf' flag
        recursive = '-r' in args or '-rf' in args
        # Remove the flag from the args list if present
        args = [arg for arg in args if arg not in ['-r', '-rf']]
        if not args:
            print("No directory name specified after flags.")
            return
        dir_path = args[0]

        full_path = os.path.join(self.current_path, dir_path) if not dir_path.startswith('/') else dir_path
        parts = full_path.strip('/').split('/')
        dirname = parts.pop()
        parent_path = '/'.join(parts)
        parent_node = self._get_node_by_path(parent_path)

        if parent_node is None:
            print(f"Path '{parent_path}' not found.")
            return

        
        if dirname in parent_node:
            if isinstance(parent_node[dirname], dict):  # It's a directory
                if recursive or not parent_node[dirname]:  # Recursive or empty
                    del parent_node[dirname]  # Delete the directory
                    print(f"Directory '{dirname}' has been deleted.")
                else:
                    print(f"Directory '{dirname}' is not empty. Use '-rf' to remove non-empty directories.")
            else:
                print(f"'{dirname}' is a file, not a directory. Use 'rm' to remove files.")
        else:
            print(f"Directory '{dirname}' not found.")
        self.save_filesystem()
    
    def ssh(self, args):
        Utility.hide_cursor()
        if not args:
            print("No ip address specified")
            return
        ip_address = args[0]
        target_terminal = next((t for t in Terminal.terminals if t.terminal_ip_address == ip_address), None)
        if not target_terminal:
            connecting_to_ip_text_thread = Animation.animated_text(static_text=f"Connecting to {ip_address}", animated_text=f"...", end_text="No Response\n", delay_between_chars=0.2, continue_thread_after_stop_for=0.1)
            Sound.play(Sound.CONNECTING_TO_COMPUTER_OVER_MODEM_SHORT, pause = 9)
            connecting_to_ip_text_thread.stop(1)
            animated_text = f"Terminal with IP address '{ip_address}' not found."
            ip_address_not_found_text_thread = Animation.animated_text(static_text="", animated_text=animated_text, end_text="\n", delay_between_chars=0.03)
            Sound.play(Sound.DIGITAL_TYPING, loop=int((len(animated_text)*0.03*10)+4), pause=0.083)
            ip_address_not_found_text_thread.stop(0.5)
            return
        if target_terminal:
            connecting_to_ip_text_thread = Animation.animated_text(static_text=f"Connecting to {ip_address}", animated_text=f"...", end_text="Connected\n", delay_between_chars=0.2, continue_thread_after_stop_for=0.1)
            Sound.play(Sound.CONNECTING_TO_COMPUTER_OVER_MODEM_SHORT, pause = 9)
            connecting_to_ip_text_thread.stop(1)
            Utility.show_cursor()
            username = input("Enter username: ")
            
            target_terminal.ensure_password_file_exists()

            user = next((u for u in target_terminal.valid_users if u.username == username), None)
            
            if user:
                # Set the active user and current path
                target_terminal.active_user = user
                target_terminal.current_path = f"/home/{username}"
                password = input("Enter password: ")
                if target_terminal.filesystem["/"]["etc"][".passwd"] == password:
                    Utility.hide_cursor()
                    target_terminal.in_ssh_session = True
                    animated_text = f"Logged into {target_terminal.terminal_name} terminal as {username}."
                    logged_in_text_thread = Animation.animated_text(static_text="", animated_text=animated_text, end_text="\n", delay_between_chars=0.03)
                    Sound.play(Sound.DIGITAL_TYPING, loop=int((len(animated_text)*0.03*10)+3), pause=0.083)
                    logged_in_text_thread.stop(0.5)
                    sleep(1)
                    Utility.clear_screen()
                    while not target_terminal.exit_requested:
                        Utility.show_cursor()
                        action = input(f"{target_terminal.active_user.username}@{target_terminal.terminal_name}:{target_terminal.current_path}$ ")
                        target_terminal.execute(action)
                        if target_terminal.exit_requested:
                            target_terminal.exit_requested = False
                            break
                    Utility.hide_cursor()
                    self._animate_typing_text_with_sound(f"Exited out of {target_terminal.terminal_name} terminal successfully!")
                    sleep(0.5)
                    Utility.clear_screen()
                    Utility.show_cursor()
                    target_terminal.in_ssh_session = False
                    return
                else:
                    print("Invalid username or password.")
                    print("Disconnecting from terminal...")
                    return
            else:
                print(f"Invalid username.")
                print("Disconnecting from terminal...")
                return
    
    def _get_node_by_path(self, path):

        node = self.filesystem["/"]
        parts = path.strip('/').split('/')
        for part in parts:
            if part in node:
                node = node[part]
            else:
                return None  # Path not found
        return node

        
    def download(self, args=[]):
        # Check if currently SSH'd into another terminal
        if not self.in_ssh_session:  # Assuming 'ssh_active' is a boolean indicating SSH session
            print("Download command can only be used when SSH'd into another terminal.")
            return
        
        if not args:
            print("Usage: download <filename or directory>")
            return
        
        target_path = args[0]
        # Call the method to start the download process
        self._start_download(target_path)
        self.save_filesystem()
        Terminal.terminals[0].save_filesystem()

    
    def _start_download(self, target_path):
        # Normalize path and find file or directory in the remote filesystem
        if not target_path.startswith("/"):
            # Relative path: combine with current_path
            full_path = os.path.join(self.current_path, target_path).strip("/")
        else:
            # Absolute path: start from root
            full_path = target_path.strip("/")
        
        node = self.filesystem["/"]  # Start from the root of the filesystem
        parts = full_path.split("/")
        filename = parts.pop()
        # If full_path was absolute, parts[0] will be an empty string; skip in loop
        for part in parts:
            if part:  # Skip empty strings, which occur if path starts with '/'
                if part in node:
                    node = node[part]
                else:
                    print(f"Path '{'/'.join(parts[:parts.index(part)+1])}' not found.")
                    return

        # At this point, 'node' should be the item (file or directory) to download
        item_name = filename
        if isinstance(node[item_name], dict):  # It's a directory
            self._zip_and_download_directory(item_name, node[item_name])
        else:  # It's a file
            self._download_file(item_name, node[item_name])


    
    def _zip_and_download_directory(self, directory_name, directory):
        user_terminal = next((t for t in Terminal.terminals if t.is_user_terminal), None)
        user_terminal_username = user_terminal.valid_users[0].username
        if user_terminal:
            # Handle potential naming conflicts
            base_name = directory_name
            zip_name = f"{base_name}.zip"
            counter = 1
            while zip_name in user_terminal.filesystem["/"]["home"][user_terminal_username]["Downloads"]:
                zip_name = f"{base_name}_{counter}.zip"
                counter += 1
            
            # Simulate zipping by copying the directory under a new '.zip' name
            user_terminal.filesystem["/"]["home"][user_terminal_username]["Downloads"][zip_name] = directory
            print(f"Directory '{directory_name}' has been downloaded and zipped as '{zip_name}'.")
            user_terminal.save_filesystem()
            
    
    def _download_file(self, file_name, content):
        user_terminal = next((t for t in Terminal.terminals if t.is_user_terminal), None)
        user_terminal_username = user_terminal.valid_users[0].username
        if user_terminal:
            user_terminal.filesystem["/"]["home"][user_terminal_username]["Downloads"][file_name] = content
            print(f"File '{file_name}' has been downloaded.")
            user_terminal.save_filesystem()
    
    def unzip(self, args=[]):
        if not args:
            print("Usage: unzip <file_name.zip>")
            return

        zip_path = args[0]
        # Handle both absolute and relative paths
        if not zip_path.startswith("/"):
            # It's a relative path; build the full path
            full_zip_path = os.path.join(self.current_path, zip_path)
        else:
            # It's an absolute path
            full_zip_path = zip_path

        # Normalize path (remove redundant slashes)
        full_zip_path = os.path.normpath(full_zip_path)
        # Split the path to get directory path and zip file name
        dir_path, zip_name = os.path.split(full_zip_path)

        if not zip_name.endswith('.zip'):
            print("Error: The file is not a .zip file.")
            return

        # Get the node for the directory containing the zip file
        dir_node = self._get_node_by_path(dir_path)
        if dir_node is None or zip_name not in dir_node:
            print(f"Error: '{zip_path}' not found.")
            return

        # Create new directory name by removing '.zip' extension
        new_dir_name = zip_name[:-4]
        counter = 1
        while new_dir_name in dir_node:
            new_dir_name = f"{zip_name[:-4]}_{counter}"
            counter += 1

        # 'Unzipping': Check if the zip file contains directory structure
        if isinstance(dir_node[zip_name], dict):
            # Create a new directory next to the zip file with the same contents
            dir_node[new_dir_name] = dir_node[zip_name].copy()  # Make a copy of the directory content
            print(f"'{zip_name}' has been unzipped to '{new_dir_name}' in directory '{dir_path}'.")
        else:
            dir_node[new_dir_name] = {}  # Make an empty directory
            print(f"'{zip_name}' has been unzipped to '{new_dir_name}' in directory '{dir_path}'.")
        self.save_filesystem()


    
    def set_password(self, args):
        if not args:
            print("No password specified")
            return
        new_password = args[0]
        self.filesystem["/"]["etc"][".passwd"] = new_password
        self.active_user.password = new_password
        print("Password updated successfully.")
        self.save_filesystem()
    
    def ifconfig(self, args=[]):
        print(f"IP Address: {self.terminal_ip_address}")
    
    def terminal_help(self, args=[]):
        print()
        print("Commands:\n")
        print("pwd - print working directory")
        print("ls - list directory contents")
        print("cd - change directory")
        print("mkdir - make directory")
        print("touch - create file")
        print("unzip - unzip file")
        print("echo - write to file")
        print("cat - print file contents")
        print("open - open file")
        print("rm - remove file")
        print("rmdir - remove directory")
        print("ifconfig - get ip address")
        print("ssh - connect to another terminal")
        print("download - download file or directory from ssh")
        print("setpasswd - set password")
        print("messenger - open hacker messenger window")
        print("clear - clear the terminal screen")
        print("help - display this help message")
        print("resetgame - reset the game")
        print("exit - exit active terminal")
        print()

    def reset_game(self, args=[]):
        while True:
            confirmation = input("Are you sure you want to reset the game? This will delete all saved data. (y/n): ")
            if confirmation.lower() in ["y", "n", "yes", "no"]:
                break
            else:
                print("Invalid choice. Please enter 'y' or 'n'.")
        if confirmation.lower() in ["y", "yes"]:
            try:
                json_files = glob.glob("./filesystems/*.json")
                for f in json_files:
                    os.remove(f)
                print("Game reset successfully. Exiting game.")
            except Exception as e:
                print(f"Error resetting game: {e}")
            finally:
                self.exit_requested = True
        else:
            print("Game reset cancelled.")
    
    def _add_file_to_filesystem(self, path: str, filename: str, content=None):
        """
        Adds a file to the specified path in the filesystem. If the path does not exist, it is created.
        
        Args:
        - path (str): The path to add the file to, relative to the root of the filesystem.
        - filename (str): The name of the file to add.
        - content (str, optional): The content of the file. Defaults to None.
        """
        # Ensure the path starts with a slash for consistency
        if not path.startswith("/"):
            path = "/" + path

        parts = path.strip("/").split("/")  # Split the path into parts
        node = self.filesystem["/"]  # Start from the root
        
        # Traverse the path, creating directories as needed
        for part in parts:
            if part not in node:
                node[part] = {}  # Create a new directory if it does not exist
            node = node[part]  # Move down to the next level in the path
        
        # Check if the file exists and if its content is different
        if filename in node:
            if node[filename] == content:
                # The file exists with the same content; do nothing
                return
            else:
                # The file exists but with different content; update it
                node[filename] = content
        else:
            # The file does not exist; add it
            node[filename] = content if content is not None else None

        # Save the updated filesystem
        self.save_filesystem()
    
    def echo(self, args):
        if not args or ">" not in args and ">>" not in args:
            print("Usage: echo \"text\" > filename.txt or echo \"text\" >> filename.txt")
            return
        
        # Join args back to a string and split by redirection operator
        args_str = " ".join(args)
        if ">>" in args_str:
            text, filename = args_str.split(" >> ", 1)
            mode = "append"
        else:
            text, filename = args_str.split(" > ", 1)
            mode = "overwrite"

        # Remove leading and trailing quotes from text
        text = text.strip("\"")

        # Handle file writing or appending
        if mode == "overwrite":
            self._add_file_to_filesystem(self.current_path, filename, text)
        elif mode == "append":
            self._append_to_file(self.current_path, filename, text)
    
    def find(self, args=[]):
        # Check if there are no arguments or the first argument is only '-a' or '-al' without a filename
        if not args or (args[0] == '-a' and len(args) == 1) or (args[0] == '-al' and len(args) == 1):
            print("Usage: find [-a] <filename> [path]")
            return
        
        show_hidden = False
        if args[0] == "-a" or args[0] == "-al":
            show_hidden = True
            args.pop(0)  # Remove the flag from the arguments
            
        if not args or args[0] == "":
            print("Missing filename argument.")
            
        search_term = args[0]
        start_path = self.current_path
        
        # Check if a path argument is given
        if len(args) > 1:
            # Check if the provided path is absolute or relative
            if args[1].startswith('/'):
                start_path = args[1]
            else:
                # If the path is not absolute, construct it relative to the current directory
                start_path = os.path.join(self.current_path, args[1]).replace("//", "/")
        
        def _search_directory(directory, term, show_hidden, path):
            found_items = []
            for item, content in directory.items():
                # Construct the full path of the item
                item_path = os.path.join(path, item).replace("//", "/")
                # Check if the item is a directory or a file
                if isinstance(content, dict): # it's a directory
                    if (show_hidden or not item.startswith(".")) and term in item:
                        found_items.append(item_path + '/')
                    # Recursively search in the directory
                    found_items += _search_directory(content, term, show_hidden, item_path)
                else:   # File
                    if (show_hidden or not item.startswith(".")) and term in item:
                        found_items.append(item_path)
            return found_items
    
        # Convert start_path to directory structures
        parts = start_path.strip("/").split("/")
        node = self.filesystem["/"]
        for part in parts:
            if part: # avoid empty strings
                try:
                    node = node[part]
                except KeyError:
                    print(f"Path '{start_path}' not found.")
                    return
        
        # Perform the search
        found_paths = _search_directory(node, search_term, show_hidden, start_path)
        if found_paths:
            for path in found_paths:
                print(path)
            print()
            return True
        else:
            print(f"No matches found for {search_term}\n")
            return False
                        
                        
    def _append_to_file(self, path, filename, content):
        """Appends content to a file, creating the file if it doesn't exist."""
        # Ensure path consistency and load or create the filesystem
        full_path = os.path.join(path, filename).strip("/")
        parts = full_path.split("/")
        file_name = parts.pop()  # Remove the file name from the path
        node = self.filesystem["/"]
        
        # Traverse or create the path
        for part in parts:
            if part not in node:
                node[part] = {}
            node = node[part]
        
        # Append to the file
        if file_name in node:
            node[file_name] += "\n" + content  # Start content on a new line
        else:
            node[file_name] = content
        
        self.save_filesystem()

    def clear_screen(self, args=[]):
        Utility.clear_screen()
    
    def exit(self, args=[]):
        self._animate_typing_text_with_sound("Exiting terminal", end_text="", delay_between_chars=0.03, loop_offset=1)
        text_animation_thread = Animation.animated_text(static_text="Exiting terminal", animated_text="...", end_text="\n", delay_between_chars=0.1, continue_thread_after_stop_for=1)
        text_animation_thread.stop(0.01)
        self.save_filesystem()
        sleep(1)
        self.exit_requested = True
    
    def _animate_typing_text_with_sound(self, text, end_text = "\n", delay_between_chars=0.03, loop_offset = 0):
        Utility.hide_cursor()
        animated_text_thread = Animation.animated_text(static_text="", animated_text=text, end_text=end_text, delay_between_chars=delay_between_chars, continue_thread_after_stop_for=0)
        Sound.play(Sound.DIGITAL_TYPING, loop=int((len(text)*0.03*10) + loop_offset), pause=0.083)
        animated_text_thread.stop(0.0)
    
    def update_mission_state(self, mission_id, completed: bool):
        # Special directory name that is hidden from the user
        hidden_dir = ".game_states"
        if hidden_dir not in self.filesystem["/"]:
            self.filesystem["/"][hidden_dir] = {}
        
        # Update the mission state
        self.filesystem["/"][hidden_dir][mission_id] = completed
        self.save_filesystem()
    
    def is_mission_completed(self, mission_id):
        # Special directory name that is hidden from the user
        hidden_dir = ".game_states"
        if hidden_dir in self.filesystem["/"]:
            return self.filesystem["/"][hidden_dir].get(mission_id, False)
        return False
        


def main():
    pass

if __name__ == "__main__":
    main()
