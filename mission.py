from terminal import Terminal
from time import sleep
import re, sys

class Mission:
    """
    Represents a mission in the terminal-based hacking simulation game.

    Attributes:
        mission_id (str): Unique identifier for the mission.
        user_terminal (Terminal): The terminal object representing the player's terminal.
        enemy_terminal (Terminal): The terminal object representing the enemy's terminal.
        enemy_messenger: Messenger associated with the enemy terminal for sending messages.
        hacker_messenger: Messenger associated with the hacker (player's) terminal for sending messages.
        hacker_messages (list): Messages from the hacker to display during the mission.
        enemy_messages (list): Messages from the enemy to display during the mission.
        is_complete (bool): Status of the mission, True if completed successfully.
    """
    
    def __init__(self, mission_id, user_terminal: Terminal, enemy_terminal: Terminal, hacker_messages, enemy_messages):
        """
        Initializes a new instance of the Mission class.

        Parameters:
            mission_id (str): Unique identifier for the mission.
            user_terminal (Terminal): The player's terminal object.
            enemy_terminal (Terminal): The enemy's terminal object.
            hacker_messages (list): List of messages from the hacker.
            enemy_messages (list): List of messages from the enemy.
        """
        
        self.mission_id = mission_id
        self.user_terminal = user_terminal
        self.enemy_terminal = enemy_terminal
        self.enemy_messenger = self.enemy_terminal.messenger
        self.hacker_messenger = Terminal.messengers[0]
        self.hacker_messages = hacker_messages
        self.enemy_messages = enemy_messages
        self.is_complete = self.user_terminal.is_mission_completed(self.mission_id)
        self.user_terminal.update_mission_state(self.mission_id, self.is_complete)
        
    def load_hacker_messages(self, hacker_messages: list):
        """
        Loads new hacker messages for the mission.

        Parameters:
            hacker_messages (list): New hacker messages to load.
        """
        
        self.hacker_messages = hacker_messages
    
    def load_enemy_messages(self, enemy_messages: list):
        """
        Loads new enemy messages for the mission.

        Parameters:
            enemy_messages (list): New enemy messages to load.
        """
        
        self.enemy_messages = enemy_messages
    
    def is_a_success(self):
        """
        Marks the mission as successfully completed and updates the user terminal's mission state.
        """
        
        self.is_complete = True
        self.user_terminal.update_mission_state(self.mission_id, True)
    
    def is_a_failure(self):
        """
        Marks the mission as failed and updates the user terminal's mission state.
        """
        
        self.is_complete = False
        self.user_terminal.update_mission_state(self.mission_id, False)
    
    def get_is_complete(self):
        """
        Returns the completion status of the mission.

        Returns:
            bool: True if the mission is complete, False otherwise.
        """
        
        return self.is_complete
    
    def update_messenger_and_display(self, messenger, msg_lst, animate: bool = False):
        """
        Updates the messenger with new messages and displays them.

        Parameters:
            messenger: The messenger instance to update.
            msg_lst (list): New messages to add and display.
            animate (bool): Whether to animate the message display.
        """
        
        messenger.enqueue_messages(msg_lst)
        if msg_lst not in messenger.messages:
            messenger.messages.append(msg_lst)
        messenger.display_messages_and_wait(animate=animate)
        sleep(2)
        messenger.wait_for_window_to_close()
    
    def prompt_to_reload_terminal(self):
        """
        Prompts the user to reload the terminal and attempt to complete the mission again.
        """
        
        while True:
            user_input = input("Would you like to reload your terminal and attempt to complete the mission? (yes/no): ")
            if re.match(r"yes|y", user_input):
                break
            elif re.match(r"no|n", user_input):
                sys.exit(0)
            else:
                print("Invalid input. Please enter 'yes|y' or 'no|n'.")

    def add_file_to_user_terminal(self, file_destination: str, file_name: str, file_content: object):
        """
        Adds a file with specified content to the user terminal's filesystem.

        Parameters:
            file_destination (str): The destination directory in the filesystem.
            file_name (str): The name of the file to add.
            file_content (object): The content to write to the file.
        """
        
        self.user_terminal._add_file_to_filesystem(file_destination, file_name, file_content)