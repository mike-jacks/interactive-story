from terminal import Terminal
from time import sleep
import re, sys

class Mission:
    def __init__(self, mission_id, enemy_terminal):
        self.name = mission_id
        self.enemy_terminal = enemy_terminal
        self.user_terminal = Terminal.terminals[0]
        self.enemy_messenger = self.enemy_terminal.messenger
        self.hacker_messenger = Terminal.messengers[0]
        self.hacker_messeges = Terminal.hacker_messages
        
    def load_hacker_messages(self, hacker_messages: list):
        pass
    
    def load_enemy_messages(self, enemy_messages: list):
        pass
    
    def completed(self):
        self.user_terminal.update_mission_state(self.name, True)
    
    def not_completed(self):
        self.user_terminal.update_mission_state(self.name, False)
    
    def is_complete(self):
        return self.user_terminal.mission_state[self.name]
    
    def update_messenger_and_display(self, messenger, msg_lst, animate: bool = False):
        messenger.enqueue_messages(msg_lst)
        if msg_lst not in messenger.messages:
            messenger.messages.append(msg_lst)
        messenger.display_messages_and_wait(animate=animate)
        sleep(2)
        messenger.wait_for_window_to_close()
    
    # def access_user_terminal(self):
    #     if not self.user_terminal.active_user:
    #             print(f"Welcome to {self.user_terminal.terminal_name} terminal.")
    #             self.user_terminal.prompt_for_login()
    #     else:
    #         print(f"Auto-login for {self.user_terminal.active_user.username}!")
    #     while not self.user_terminal.exit_requested:
    #         if self.user_terminal.active_user:
    #             action = input(f"{self.user_terminal.active_user.username}@{self.user_terminal.terminal_name}:{self.user_terminal.current_path}$ ")
    #             self.user_terminal.execute(action)
    #         else:
    #             self.user_terminal.prompt_for_login()
    #         if self.user_terminal.exit_requested:
    #             self.user_terminal.exit_requested = False
    #             break
    #     print("Quit out of terminal successfully!")

    def prompt_to_reload_terminal(self):
        while True:
            user_input = input("Would you like to reload your terminal and attempt to complete the mission? (yes/no): ")
            if re.match(r"yes|y", user_input):
                break
            elif re.match(r"no|n", user_input):
                sys.exit(0)
            else:
                print("Invalid input. Please enter 'yes|y' or 'no|n'.")

    def add_file_to_user_terminal(self, file_destination: str, file_name: str, file_content: object):
        self.user_terminal._add_file_to_filesystem(file_destination, file_name, file_content)
    
    def __str__(self):
        pass