import json
import glob, os
from types import UnionType
from utility import Utility
from text_color import TextColor
from ascii_animation import play_ascii_animation, load_ascii_art_animation_from_json
from time import sleep

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

    def __init__(self, terminal_name: str, terminal_ip_address: str, terminal_username = None, terminal_password = None) -> None:
        self.terminal_name = terminal_name
        self.terminal_ip_address = terminal_ip_address
        self.filesystem_filename = f"./filesystems/{terminal_name}_filesystem.json"
        self.filesystem_exists = os.path.exists(self.filesystem_filename)
        self.valid_users: list[User] = []
        self.active_user = None
        
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
            "cat": self.cat,
            "open": self.open_file,
            "rm": self.rm,
            "rmdir": self.rmdir,
            "ifconfig": self.ifconfig,
            "ssh": self.ssh,
            "setpasswd": self.set_password,
            #"messenger": self.mesenger,
            "help": self.terminal_help,
            "resetgame": self.reset_game,
            "exit": self.exit,
        }
    
    def prompt_for_login(self):
        print("Please log in.")
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        self.login_user(username, password)
        
    def prompt_for_create_user(self):
        print("You need to create a new user before being able to login.")
        username = input("Create username: ")
        password = input("Create password: ")
        self.create_user(username, password)
    
    def add_user(self, username: str, password: str) -> None:
        self.valid_users.append(User(username, password))
    
    def load_filesystem(self):
        try:
            with open(self.filesystem_filename) as file:
                return json.load(file)
        except FileNotFoundError:
            return self.create_new_filesystem() # Create a new filesystem and immediately use it if one does not exist
    
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
    
    def save_filesystem(self, filesystem=None):
        filesystem = filesystem or self.filesystem
        with open(self.filesystem_filename, "w") as file:
            json.dump(filesystem, file, indent=4)
    
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
                return True
        if not user_found:
            print("Login failed. Invalid username or password.")
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
        args = command.split()
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
            parts = self.current_path.strip("/").split("/") # Remove leading '/' and split
            for part in parts:
                if part in node:
                    node = node[part]
                else:
                    print(f"Directory '{part}' not found.")
                    return
        
        # List the contents of the current directory
        if isinstance(node, dict):
            for item in node:
                if not show_all and item.startswith("."):
                    continue # Skip hidden files and directories unles -a or -al flag is present
                if not isinstance(node[item], dict): # it's a file
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
    
    def touch(self, args):
        if not args:
            print("No file name specified")
            return
        filename = args[0]
        node = self.filesystem["/"]
        parts = self.current_path.strip("/").split("/")
        for part in parts:
            if part in node:
                node = node[part]
            else:
                print(f"Path '{'/'.join(parts)}' not found.")
                return
        if filename in node:
            print(f"File '{filename}' already exists.")
            return
        else:
            node[filename] = None 
    
    def cat(self, args):
        if not args:
            print("No file name specified")
            return
        filename = args[0]
        node = self.filesystem["/"]
        parts = self.current_path.strip("/").split("/")
        for part in parts:
            if part in node:
                node = node[part]
            else:
                print(f"Path '{'/'.join(parts)}' not found.")
                return
        if filename in node and isinstance(node[filename], str):
            print(rf"{node[filename]}")
        else:
            print(f"'{filename}' is not a readable file.")
    
    def open_file(self, args):
        if not args:
            print("No file name specified")
            return
        filename = args[0]
        node = self.filesystem["/"]
        parts = self.current_path.strip("/").split("/")
        for part in parts:
            if part in node:
                node = node[part]
            else:
                print(f"Path '{'/'.join(parts)}' not found.")
                return
        if filename in node and isinstance(node[filename], str):
            print(node[filename])
        elif filename in node and isinstance(node[filename], list):
            Utility.clear_screen()
            Utility.hide_cursor()
            play_ascii_animation(node[filename], frames_per_second=12, loop_num_times=-2)
            Utility.show_cursor()
        else:
            print(f"'{filename}' is not a readable file.")
    
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
        target_name = args[0]
        
        # Navigate to the target's parent directory
        node = self.filesystem["/"]
        parts = self.current_path.strip("/").split("/")
        for part in parts:
            if part in node:
                node = node[part]
            else:
                print(f"Path '{'/'.join(parts)}' not found.")
                return
        
        # Delete the target file or directory
        if target_name in node:
            if isinstance(node[target_name], dict) and not recursive:
                print(f"'{target_name}' is a directory. Use '-rf' to remove directories.")
                return
            else:
                del node[target_name]
                print(f"File '{target_name}' has been deleted.")
        else:
            print(f"File '{target_name}' not found.")
            
            
            
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
        dirname = args[0]

        # Start from the root or current_path and find the target directory's parent
        node = self.filesystem["/"]
        parts = self.current_path.strip("/").split("/")  # Adjust to navigate from root
        target_path = parts + [dirname] if self.current_path != "/" else [dirname]
        parent_path = target_path[:-1]
        parent_node = node

        # Navigate to the parent directory of the target
        for part in parent_path:
            if part in parent_node and isinstance(parent_node[part], dict):
                parent_node = parent_node[part]
            else:
                print(f"Directory '{'/'.join(parent_path)}' not found.")
                return

        # Now, parent_node is the parent directory of the target
        # delete_dir is adjusted to operate directly on the parent node
        def delete_dir(parent_node, dirname):
            if dirname in parent_node:
                if isinstance(parent_node[dirname], dict):  # It's a directory
                    if recursive or not parent_node[dirname]:  # Recursive or empty
                        del parent_node[dirname]  # Delete the directory
                        print(f"Directory '{dirname}' has been deleted.")
                    else:
                        print(f"Directory '{dirname}' is not empty.")
                else:
                    print(f"'{dirname}' is a file, not a directory.")
            else:
                print(f"Directory '{dirname}' not found.")

        # Call delete_dir with the parent node and the directory name to remove
        delete_dir(parent_node, dirname)
    
    def ssh(self, args):
        if not args:
            print("No ip address specified")
            return
        ip_address = args[0]
        target_terminal = next((t for t in Terminal.terminals if t.terminal_ip_address == ip_address), None)
        if not target_terminal:
            print(f"Terminal with IP address '{ip_address}' not found.")
            return
        if target_terminal:
            print(f"Connecting to {ip_address}...")
            sleep(1)
            print(f"Connected to {ip_address}.")
            username = input("Enter username: ")
            password = input("Enter password: ")

            target_terminal.ensure_password_file_exists()
            # Verify credentials
            user = next((u for u in target_terminal.valid_users if u.username == username), None)

            if not hasattr(target_terminal, 'current_path'):
                target_terminal.current_path = f"/home/{username}"
            
            # if not hasattr(target_terminal, 'active_user') and target_terminal.active_user is None:
            #     target_terminal.active_user = user
            
            target_terminal.login_user(user.username, user.password)
                
            if user:
                self.ensure_password_file_exists()
                if target_terminal.filesystem["/"]["etc"][".passwd"] == password:
                    print(f"Logged into {target_terminal.terminal_name} terminal as {username}.")
                    sleep(1)
                    while not target_terminal.exit_requested:
                        action = input(f"{target_terminal.active_user.username}@{target_terminal.terminal_name}:{target_terminal.current_path}$ ")
                        target_terminal.execute(action)
                        if target_terminal.exit_requested:
                            target_terminal.exit_requested = False
                            break
                    print(f"Quit out of {target_terminal.terminal_name} terminal successfully!")
                    return
                else:
                    print("Invalid username or password.")
                    print("Disconnecting from terminal...")
                    return
            else:
                print(f"Invalid username.")
                print("Disconnecting from terminal...")
                return
    
    def set_password(self, args):
        if not args:
            print("No password specified")
            return
        new_password = args[0]
        self.filesystem["/"]["etc"][".passwd"] = new_password
        self.active_user.password = new_password
        print("Password updated successfully.")
    
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
        print("cat - print file contents")
        print("open - open file")
        print("rm - remove file")
        print("rmdir - remove directory")
        print("ifconfig - get ip address")
        print("exit() - exit terminal")
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
    
    def exit(self, args=[]):
        print("Exiting terminal...")
        self.save_filesystem()
        sleep(1)
        self.exit_requested = True


Utility.clear_screen()
# Create a few terminals
user_terminal = Terminal(terminal_name="user_machine", terminal_ip_address="170.130.234.11")
gibson_terminal = Terminal(terminal_name="gibson", terminal_ip_address="18.112.29.87", terminal_username="admin", terminal_password="god")

def main():
    if not user_terminal.active_user:
        print("Welcome to the terminal.")
        user_terminal.prompt_for_login()
    
    # Main command loop
    while not user_terminal.exit_requested:
        if user_terminal.active_user:
            action = input(f"{user_terminal.active_user.username}@{user_terminal.terminal_name}:{user_terminal.current_path}$ ")
            user_terminal.execute(action)
        else:
            user_terminal.prompt_for_login()
        if user_terminal.exit_requested:
            break
    print("Quit out of terminal successfully!")

if __name__ == "__main__":
    main()
