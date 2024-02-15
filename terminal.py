import json
from types import UnionType
from utility import Utility
from text_color import TextColor
from ascii_animation import play_ascii_animation, load_ascii_art_animation_from_json
from time import sleep

class Terminal:

    def __init__(self, fname):
        self.current_path = "/home"
        self.home = "/home"
        self.filesystem = self.load_filesystem(fname)
        self.commands = {
            "pwd": self.pwd,
            "ls": self.ls,
            "cd": self.cd,
            "mkdir": self.mkdir,
            "touch": self.touch,
            "cat": self.cat,
            "open": self.open,
            "rm": self.rm,
            "rmdir": self.rmdir,
            "exit()": self.exit,
        }
        self.username = None
        self.exit_requested = False

    def load_filesystem(self, filename):
        with open(filename) as json_file_object:
            return json.load(json_file_object)

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
        if args:
            print("pwd does not take any arguments")
            return
        print(self.current_path)

    def ls(self, args=[]):
        if args:
            print("ls does not take any arguments")
            return
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
                if node[item] is None:
                    print(f"{TextColor.WHITE.value}{item}{TextColor.RESET.value}", end=" ") # File printed to console
                else:
                    print(f"{TextColor.BLUE.value}{item}{TextColor.RESET.value}", end=" ") # Directory printed to console
        elif node is None:
            # The current node is a file, not a directory
            print("Current path is a file, not a directory")
        print("\n")
    
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
                if node[part] is None:
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
            self.current_path = self.home
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
    
    def open(self, args):
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
            play_ascii_animation(filename, frames_per_second=24, loop_num_times=1)
        else:
            print(f"'{filename}' is not a readable file.")
    
    def rm(self, args):
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
            if not isinstance(node[filename], dict): # Not a directory
                del node[filename]
                print(f"'{filename}' has been deleted.")
            else:
                print(f"'{filename}' is a directory, not a file. Cannot delete directories with rm.")
        else:
            print(f"File '{filename}' not found.")
    
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

    
    def exit(self, args=[]):
        print("Exiting terminal...")
        sleep(1)
        self.exit_requested = True
        
        

def main():
    Utility.clear_screen()
    terminal = Terminal("./filesystems/home.json")
    username = input("Username: ")
    while True:
        action = input(f"[{username}] {terminal.current_path} $ ")
        terminal.execute(action)
        if terminal.exit_requested:
            break
    print("Quit out of terminal successfully!")

if __name__ == "__main__":
    main()
