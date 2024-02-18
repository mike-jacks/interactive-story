from utility import Utility
from ascii_animation import load_ascii_art_animation_from_json, play_ascii_animation
from animation import Animation
from sound import Sound
from time import sleep
from terminal import Terminal
import re, sys

animated_text = Animation.animated_text

def animate_text_with_sound(text_to_animate: str, static_text: str = "", end_text: str = "\n", sound_file: str = Sound.DIGITAL_TYPING, pause=0.083, delay_between_chars: float = 0.03, stop_event = None, continue_thread_after_stop_for = 0.000, loop_offset = 0, thread_stop_freeze = 0.5):
    animated_text_thread = animated_text(static_text=static_text, animated_text=text_to_animate, end_text=end_text, delay_between_chars=delay_between_chars, stop_event = stop_event, continue_thread_after_stop_for=continue_thread_after_stop_for)
    Sound.play(sound_file, loop=int((len(text_to_animate)*(delay_between_chars * 10)) + loop_offset), pause=pause)
    animated_text_thread.stop(thread_stop_freeze)
    
def update_messenger_and_display(messenger, msg_lst, animate: bool = False):
    messenger.enqueue_messages(msg_lst)
    if msg_lst not in messenger.messages:
        messenger.messages.append(msg_lst)
    messenger.display_messages_and_wait(animate=animate)
    sleep(2)
    messenger.wait_for_window_to_close()
    
def access_terminal(user_terminal: Terminal, incoming_message: bool, messeges: list = []):
    Utility.hide_cursor()
    if not user_terminal.active_user:
        animate_text_with_sound("Welcome to your user terminal", loop_offset=2,thread_stop_freeze=0.1)
        animate_text_with_sound("-----------------------------", loop_offset=2, thread_stop_freeze=0.1)
        user_terminal.prompt_for_login()
        Utility.clear_screen()
    else:
        animate_text_with_sound("Welcome to your user terminal", loop_offset=2,thread_stop_freeze=0.1)
        animate_text_with_sound("-----------------------------", loop_offset=2, thread_stop_freeze=0.1)
        animate_text_with_sound(f"Logged in as {user_terminal.active_user.username}!", loop_offset=2, thread_stop_freeze=0.1)
        sleep(1)
        Utility.clear_screen()
    while not user_terminal.exit_requested:
        Utility.show_cursor()
        if user_terminal.active_user:
            if incoming_message and messeges:
                Utility.hide_cursor()
                animate_text_with_sound("New message incoming from hacker", loop_offset=2,thread_stop_freeze=0.1)
                sleep(1)
                Utility.clear_screen()
                update_messenger_and_display(Terminal.messengers[0], messeges, animate=True)
                incoming_message = False
                Utility.show_cursor()
            action = input(f"{user_terminal.active_user.username}@{user_terminal.terminal_name}:{user_terminal.current_path}$ ")
            user_terminal.execute(action)
        else:
            user_terminal.prompt_for_login()
            Utility.clear_screen()
        if user_terminal.exit_requested:
            user_terminal.exit_requested = False
            break
    print("Quit out of terminal successfully!")

def prompt_to_reload_terminal():
    while True:
        user_input = input("Would you like to reload your terminal and login to the Gibson terminal to complete the mission? (yes/no): ")
        if re.match(r"yes|y", user_input):
            break
        elif re.match(r"no|n", user_input):
            sys.exit(0)
        else:
            print("Invalid input. Please enter 'yes|y' or 'no|n'.")

def main():
    Utility.clear_screen()
    Utility.hide_cursor()
    # Initialize Terminals
    user_terminal = Terminal(terminal_name="localhost", terminal_ip_address="127.0.0.1", is_user_terminal=True)
    gibson_terminal = Terminal(terminal_name="gibson", terminal_ip_address="18.127.11.23", terminal_username="admin", terminal_password="god")
    microsoft_terminal = Terminal(terminal_name="microsoft", terminal_ip_address="18.23.123.11", terminal_username="root", terminal_password="M$FT")
    apple_terminal = Terminal(terminal_name="apple", terminal_ip_address="182.124.12.132", terminal_username="apple", terminal_password="M@c1nt0sh")

    # Initialize Messengers
    hacker_messenger = Terminal.messengers[0]
    gibson_messenger = gibson_terminal.messenger
    microsoft_messenger = microsoft_terminal.messenger
    apple_messenger = apple_terminal.messenger
    
    
    # Add opening animated logo and display on screen
    hack_the_planet_animation = load_ascii_art_animation_from_json("./animation_images_json/hack_the_planet_animation.json")
    play_ascii_animation(hack_the_planet_animation, frames_per_second=24)
    Utility.clear_screen()
    
    # Opening text animation with sound
    text_to_animate = "Welcome to Hack The Planet!"
    animate_text_with_sound(text_to_animate, loop_offset=2)
    animate_text_with_sound("In just a moment you will be asked to create a login for your terminal.", loop_offset=5)
    animate_text_with_sound("Once logged into your terminal, you can type 'help' to get a list of commands available to you.", loop_offset=8)
    animate_text_with_sound("Good luck on your hacking adventure!", loop_offset=2)
    sleep(2)
    Utility.clear_screen()
    
    # Booting up system text animation
    loading_kernel_text_animation = animated_text(static_text="Loading Kernel", animated_text="...", end_text="Complete!\n", delay_between_chars=0.15, continue_thread_after_stop_for=3)
    loading_kernel_text_animation.stop(0.5)
    configuring_system_settings_text_animation = animated_text(static_text="Configuring System Settings", animated_text="...", end_text="Complete!\n", delay_between_chars=0.15, continue_thread_after_stop_for=3)
    configuring_system_settings_text_animation.stop(0.5)
    booting_up_system_text_animation = animated_text(static_text="Booting up system", animated_text="...", end_text="Complete!\n", delay_between_chars=0.15, continue_thread_after_stop_for=3)
    booting_up_system_text_animation.stop(0.5)
    Utility.clear_screen()
    Sound.play(Sound.MAC_OS_STARTUP_MODERN_SOUND)
    sleep(3)
    
    
    # Load mission 1:
    hacker_messages = [
        f"Hi {user_terminal.valid_users[0].username}!\n",
        "I'm a hacker and I hear you are a pretty\ngood hacker yourself!\n",
        "I need your help to modify files on the\nGibson terminal.\n",
        "For some reason I can't write or modify\nfiles on the Gibson terminal, only read\n",
        "I have placed a file in your Downloads\nfolder for you to gain access.\n",
        "Please change the password of the admin\nuser to 'hacked'.\n",
        "Once completed, please log out of your\nterminal and I will message you with further instructions.\n",
        "I am watching you...\n",
        "P.S. Once logged into a terminal type\n'help' to see a list of commands you can use in the terminal.\n",
        f"P.P.S. Just a reminder your username is:\n\"{user_terminal.valid_users[0].username}\"\nand your password is: \n\"{user_terminal.filesystem["/"]["etc"][".passwd"]}\"\nin case you forgot.\n",
    ]
    # # Display Hacker Messages to messenger terminal
    # update_messenger_and_display(hacker_messenger, hacker_messages, animate=True)
    
    # # Add gibson credential files to user filesystem
    # user_terminal._add_file_to_filesystem(f"/home/{user_terminal.valid_users[0].username}/Downloads", "gibson_credentials.txt",
    # f"""    
    # Gibson Terminal Credentials
    # ---------------------------
    # IP Address: {gibson_terminal.terminal_ip_address}
    # Username: {gibson_terminal.valid_users[0].username}
    # Password: {gibson_terminal.filesystem["/"]["etc"][".passwd"]}
    # ---------------------------
    # """)
    
    
    # Access user terminal
    
    access_terminal(user_terminal, incoming_message=True, messeges=hacker_messages)
    
    
    
    
if __name__ == "__main__":
    main()