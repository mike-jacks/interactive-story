from sound import Sound
from animation import Animation
from utility import Utility
from text_color import TextColor
from ascii_animation import play_ascii_animation, load_ascii_art_animation_from_json, clean_up_ascii_art_animation
from time import sleep
import re, sys
from messenger_terminal import MessageTerminal, HackerMessenger, CorporationMessenger
from terminal import Terminal


def add_and_display_messages_from_hacker_messenger(hacker_messages: list, animate: bool = False):
    hacker_messenger = Terminal.messengers[0]
    hacker_messenger.enqueue_messages(hacker_messages)
    if hacker_messages not in Terminal.hacker_messages:
        Terminal.hacker_messages.append(hacker_messages)
    hacker_messenger.display_messages_and_wait(animate=True)
    sleep(2)
    hacker_messenger.wait_for_window_to_close()

def access_terminal(user_terminal: Terminal):
    if not user_terminal.active_user:
            print(f"Welcome to {user_terminal.terminal_name} terminal.")
            user_terminal.prompt_for_login()
    else:
        print(f"Auto-login for {user_terminal.active_user.username}!")
    while not user_terminal.exit_requested:
        if user_terminal.active_user:
            action = input(f"{user_terminal.active_user.username}@{user_terminal.terminal_name}:{user_terminal.current_path}$ ")
            user_terminal.execute(action)
        else:
            user_terminal.prompt_for_login()
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
    # Clear Screen
    Utility.clear_screen()
    
    # Initialize Terminals
    user_terminal = Terminal(terminal_name="localhost", terminal_ip_address="127.0.0.1")
    gibson_terminal = Terminal(terminal_name="gibson", terminal_ip_address="18.127.11.23", terminal_username="admin", terminal_password="god")
    microsoft_terminal = Terminal(terminal_name="microsoft", terminal_ip_address="18.23.123.11", terminal_username="root", terminal_password="M$FT")
    apple_terminal = Terminal(terminal_name="apple", terminal_ip_address="182.124.12.132", terminal_username="apple", terminal_password="M@c1nt0sh")
    
    # Initialize Messengers
    hacker_messenger = Terminal.messengers[0]
    gibson_messenger = gibson_terminal.messenger
    microsoft_messenger = microsoft_terminal.messenger
    apple_messenger = apple_terminal.messenger
    
    # # Hacker Message 1:
    # hacker_messages = [
    #     f"Hi {user_terminal.valid_users[0].username}!\n",
    #     "I'm a hacker and I hear you are a pretty\ngood hacker yourself!\n",
    #     "I need your help to modify files on the\nGibson terminal.\n",
    #     "For some reason I can't write or modify\nfiles on the Gibson terminal, only read\n",
    #     "I have placed a file in your Downloads\nfolder for you to gain access.\n",
    #     "Please change the password of the admin\nuser to 'hacked'.\n",
    #     "Once completed, please log out of your\nterminal and I will message you with further instructions.\n",
    #     "I am watching you...\n",
    #     "P.S. Once logged into a terminal type\n'help' to see a list of commands you can use in the terminal.\n",
    #     f"P.P.S. Just a reminder your username is:\n\"{user_terminal.valid_users[0].username}\"\nand your password is: \n\"{user_terminal.filesystem["/"]["etc"][".passwd"]}\"\nin case you forgot.\n",
    # ]
    # # Display Hacker Messages to messenger terminal
    # add_and_display_messages_from_hacker_messenger(hacker_messages, animate=True)
    
    # Add gibson credential files to user filesystem
    user_terminal._add_file_to_filesystem(f"/home/{user_terminal.valid_users[0].username}/Downloads", "gibson_credentials.txt",
    f"""    
    Gibson Terminal Credentials
    ---------------------------
    IP Address: {gibson_terminal.terminal_ip_address}
    Username: {gibson_terminal.valid_users[0].username}
    Password: {gibson_terminal.filesystem["/"]["etc"][".passwd"]}
    ---------------------------
    """)
    
    # Start Game
    
    # Mission 1
    mission_1_completed = False
    while not mission_1_completed:
        access_terminal(user_terminal)
        if gibson_terminal.filesystem["/"]["etc"][".passwd"] == "hacked":
            mission_1_completed = True
        else:
            hacker_messages = [
                "I can see you have not changed the password to \"hacked\"",
                f"The password currently is \"{gibson_terminal.filesystem["/"]["etc"][".passwd"]}\"",
                "You have not completed the mission yet.",
                "Please reload your terminal and login to the Gibson terminal to complete the mission.",
                "Please complete the mission and then log out of your terminal."
            ]
            add_and_display_messages_from_hacker_messenger(hacker_messages, animate=True)
            prompt_to_reload_terminal()
    user_terminal.active_user = None
        
    # Hacker Message 2:
    hacker_messages = [
        f"Hi {user_terminal.valid_users[0].username}!",
        "I see you have completed the mission.",
        "I have sent you a file with the ip address and login credentials for the Microsoft terminal.",
        "Please ssh into the Microsoft terminal and change the password of the root user to 'hacked'.",
        "Once completed, please log out of your terminal and I will message you with further instructions.",
        "I am watching you...",
    ]
    # Display Hacker Messages to messenger terminal
    add_and_display_messages_from_hacker_messenger(hacker_messages, animate=True)
    
    
    # Mission 2
    mission_2_completed = False
    while not mission_2_completed:
        access_terminal(user_terminal)
        if microsoft_terminal.filesystem["/"]["etc"][".passwd"] == "hacked":
            mission_2_completed = True
        else:
            hacker_messages = [
                "I can see you have not changed the password to \"hacked\"",
                f"The password currently is \"{microsoft_terminal.filesystem["/"]["etc"][".passwd"]}\"",
                "You have not completed the mission yet.",
                "Please reload your terminal and login to the Gibson terminal to complete the mission.",
                "Please complete the mission and then log out of your terminal."
            ]
            add_and_display_messages_from_hacker_messenger(hacker_messages, animate=True)
            prompt_to_reload_terminal()
    
    
    
    
    
    
    # Utility.hide_cursor()
    # dialing_phone_num_text_animation = Animation.animated_text("Dialing phone number", end_text="Complete!\n", static_text_color= TextColor.RAINBOW, animated_text_color= TextColor.RAINBOW, end_text_color= TextColor.RAINBOW, delay_between_chars= 0.2, continue_thread_after_stop_for= 1)
    # Sound.play(Sound.DIAL_TONE, pause= 1)
    # Sound.play(Sound.DIALING_PHONE_NUMBER, pause = 2.4)
    # dialing_phone_num_text_animation.stop(wait_before_continueing_after_thread_stop_for= 1)
    # connect_to_computer_text_animation = Animation.animated_text("Connecting to computer over modem", end_text="Complete!\n", static_text_color= TextColor.random(), animated_text_color= TextColor.random(), end_text_color=TextColor.random(), delay_between_chars= 0.2, continue_thread_after_stop_for= 1)
    # Sound.play(Sound.CONNECTING_TO_COMPUTER_OVER_MODEM_SHORT, pause = 9)
    # connect_to_computer_text_animation.stop(wait_before_continueing_after_thread_stop_for= 1)
    # booting_up_computer_text_animation = Animation.animated_text("Booting up computer", end_text="Complete!\n", delay_between_chars= 0.2, continue_thread_after_stop_for=3)
    # Sound.play(Sound.MAC_OS_STARTUP_MODERN_SOUND, pause= 5)
    # booting_up_computer_text_animation.stop(wait_before_continueing_after_thread_stop_for= 1)
    # print("Computer booted up!")
    # print_animated_message1 = Animation.animated_text(static_text="", animated_text="I can also print animated messages like this one! Depending on how long I hold it for, I can animated it more than once!", end_text="\n", delay_between_chars= 0.02, continue_thread_after_stop_for= 1)
    # print_animated_message1.stop(wait_before_continueing_after_thread_stop_for= 2)
    # print_animated_message2 = Animation.animated_text(static_text="", animated_text="I can print fast,", delay_between_chars= 0.05, continue_thread_after_stop_for= 0.1)
    # print_animated_message2.stop(0.01)
    # print_animated_message3 = Animation.animated_text(static_text="I can print fast,", animated_text=" or I can print slow,", delay_between_chars= 0.2, continue_thread_after_stop_for= 0.1)
    # print_animated_message3.stop(0.01)
    # print_animated_message4 = Animation.animated_text(static_text="I can print fast, or I can print slow,", animated_text=" or I can print very slow!", end_text="\n", delay_between_chars= 0.4, continue_thread_after_stop_for= 1)
    # print_animated_message4.stop(0.01)

    # simpson_bush_animation = load_ascii_art_animation_from_json("animation_images_json/simpson_bush.json")
    # play_ascii_animation(simpson_bush_animation, frames_per_second=12, loop_num_times= -2, continue_thread_after_stop_for= 2)
    # print("Done!")
    # sleep(5)
    # Utility.clear_screen()
    # simpson_bush_animation_playing = play_ascii_animation(simpson_bush_animation, frames_per_second=12, loop_num_times= 0, continue_thread_after_stop_for= 2)
    # sleep(20)
    # simpson_bush_animation_playing.stop(2)
    # print("Done!")
    # Utility.clear_screen()
    # dog1 = load_ascii_art_animation_from_json("image_json/dog1.json")
    # dog2 = load_ascii_art_animation_from_json("image_json/dog2.json")
    # dog3 = load_ascii_art_animation_from_json("image_json/dog3.json")
    # dog4 = load_ascii_art_animation_from_json("image_json/dog4.json")
    # dog5 = load_ascii_art_animation_from_json("image_json/dog5.json")
    # hack_the_planet = load_ascii_art_animation_from_json("image_json/hack_the_planet.json")
    # print()
    # play_ascii_animation(dog1, frames_per_second=1)
    # print()
    # play_ascii_animation(dog2, frames_per_second=1)
    # print()
    # play_ascii_animation(dog3, frames_per_second=1)
    # print()
    # play_ascii_animation(dog4, frames_per_second=1)
    # print()
    # play_ascii_animation(dog5, frames_per_second=1)
    # print()
    # print("Done!")
    # print()
    # play_ascii_animation(hack_the_planet, frames_per_second=1)
    
    # Utility.clear_screen()
    # Utility.hide_cursor()
    # hack_the_planet_animation = load_ascii_art_animation_from_json("animation_images_json/hack_the_planet_animation.json")
    # hack_the_planet_animation = clean_up_ascii_art_animation(hack_the_planet_animation)
    # hack_the_planet_thread = play_ascii_animation(hack_the_planet_animation, frames_per_second=24, loop_num_times= 0, continue_thread_after_stop_for= 2)
    # hack_the_planet_thread.stop(2)
    # play_ascii_animation(hack_the_planet_animation, frames_per_second=24, loop_num_times= -4)

if __name__ == '__main__':
    main()