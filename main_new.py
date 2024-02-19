from utility import Utility
from ascii_animation import load_ascii_art_animation_from_json, play_ascii_animation, clean_up_ascii_art_animation
from animation import Animation
from sound import Sound
from time import sleep
from terminal import Terminal
import re, sys, os
from mission import Mission
import json
from text_color import TextColor

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
    
def access_terminal(user_terminal: Terminal, incoming_message: bool, messages: list = []):
    user_terminal.hacker_messages.append(messages)
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
            if incoming_message and messages:
                Utility.hide_cursor()
                animate_text_with_sound("New message incoming", end_text="", loop_offset=1,thread_stop_freeze=0.1)
                animated_text_thread = animated_text(static_text="New message incoming", animated_text="...", end_text="\n", delay_between_chars=0.1, continue_thread_after_stop_for=2)
                animated_text_thread.stop(0.5)
                Utility.clear_screen()
                update_messenger_and_display(Terminal.messengers[0], messages, animate=True)
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
    animate_text_with_sound(f"Exited out of {user_terminal.terminal_name} terminal successfully!", loop_offset=4,thread_stop_freeze=0.1)
    sleep(1)

def prompt_to_reload_terminal():
    while True:
        animate_text_with_sound("Would you like to reload your terminal attempt to complete the mission? (yes/no): ",end_text="", loop_offset=8,thread_stop_freeze=0.1)
        user_input = input("")
        if re.match(r"yes|y", user_input):
            break
        elif re.match(r"no|n", user_input):
            sys.exit(0)
        else:
            animate_text_with_sound("Invalid input. Please enter 'yes|y' or 'no|n'.", end_text="\n", loop_offset=2,thread_stop_freeze=0.1)

def main():
    Utility.clear_screen()
    # Test animation
    hackers_animation = load_ascii_art_animation_from_json("./animation_images_json/hackers_animation.json")
    hackers_animation = clean_up_ascii_art_animation(hackers_animation)
    Sound.play(Sound.HACKERS_ANIMATION, loop=1, pause=0.0)
    hackers_animation_thread = play_ascii_animation(hackers_animation, frames_per_second=34, loop_num_times=0, continue_thread_after_stop_for=0.01)
    hackers_animation_thread.stop()
    Utility.clear_screen()
    
    
    # Add opening animated logo and display on screen
    Utility.hide_cursor()
    hack_the_planet_animation = load_ascii_art_animation_from_json("./animation_images_json/hack_the_planet_animation.json")
    hack_the_planet_animation = clean_up_ascii_art_animation(hack_the_planet_animation)
    hack_the_planet_animation_thread = play_ascii_animation(hack_the_planet_animation, frames_per_second=24, loop_num_times=0, continue_thread_after_stop_for=3.8)
    Sound.play(Sound.DIGITAL_TYPING, loop=15, pause=0.083)
    hack_the_planet_animation_thread.stop(0.5)
    Utility.clear_screen()
    
    # Opening text animation with sound
    if not os.path.exists("./filesystems/localhost_filesystem.json"):
        animate_text_with_sound("Welcome to Hack The Planet!", loop_offset=2)
        animate_text_with_sound("In just a moment you will be asked to create a login for your terminal.", loop_offset=5)
        animate_text_with_sound("Once logged into your terminal, you can type 'help' to get a list of commands available to you.", loop_offset=8)
        animate_text_with_sound("Good luck on your hacking adventure!", loop_offset=2)
        sleep(2)
        Utility.clear_screen()
    else:
        with open("./filesystems/localhost_filesystem.json", "r") as file:
            local_loaded_filesystem = json.load(file)
        username = list(local_loaded_filesystem["/"]["home"].keys())[0]
        password = local_loaded_filesystem["/"]["etc"][".passwd"]
        animate_text_with_sound("Welcome back to Hack The Planet!", loop_offset=2)
        animate_text_with_sound(f"Your user credentials are user: \'{username}\' and password: \'{password}\' in case you forgot.", loop_offset=7)
        animate_text_with_sound("Once logged into your terminal, you can type 'help' to get a list of commands available to you.", loop_offset=8)
        animate_text_with_sound("Good luck on your hacking adventure!", loop_offset=3)
        sleep(2)
        Utility.clear_screen()
    
    # Booting up system text animation
    loading_kernel_text_animation = animated_text(static_text="Loading Kernel", animated_text="...", end_text=f"{TextColor.GREEN.value}Complete!{TextColor.RESET.value}\n", delay_between_chars=0.15, continue_thread_after_stop_for=3)
    Sound.play(Sound.COMPLETE_NOTIFICATION, loop=1, pause=0.0)
    loading_kernel_text_animation.stop(1)
    configuring_system_settings_text_animation = animated_text(static_text="Loading system configuration settings", animated_text="...", end_text=f"{TextColor.GREEN.value}Complete!{TextColor.RESET.value}\n", delay_between_chars=0.15, continue_thread_after_stop_for=3)
    Sound.play(Sound.COMPLETE_NOTIFICATION, loop=1, pause=0.0)
    configuring_system_settings_text_animation.stop(1)
    booting_up_system_text_animation = animated_text(static_text="Booting up system", animated_text="...", end_text=f"{TextColor.GREEN.value}Complete!{TextColor.RESET.value}\n", delay_between_chars=0.15, continue_thread_after_stop_for=3)
    Sound.play(Sound.COMPLETE_NOTIFICATION, loop=1, pause=0.0)
    booting_up_system_text_animation.stop(1.5)
    Utility.clear_screen()
    sleep(0.5)
    access_granted_animation = load_ascii_art_animation_from_json("./animation_images_json/access_granted.json")
    access_granted_animation = clean_up_ascii_art_animation(access_granted_animation)
    access_granted_animation_thread = play_ascii_animation(access_granted_animation, frames_per_second=24, loop_num_times=0, continue_thread_after_stop_for=0.5)
    Sound.play(Sound.MAC_OS_STARTUP_MODERN_SOUND)
    access_granted_animation_thread.stop()
    sleep(1.5)
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
    
    #Load hacker messages json:
    with open("./hacker_mission_messages.json", "r") as file:
        hacker_mission_messages = json.load(file)
    
    
    
    # Build Mission 1: Gibson Terminal
    enemy_messages = [
        "Listen here, punk. I don't know who you are, but you better watch yourself.\n",
        "Tell me who you're working for and I might go easy on you.\n"
    ]
    
    mission_1 = Mission("Mission 1: Gibson Terminal", user_terminal, gibson_terminal, hacker_mission_messages["1"], enemy_messages)
    if not mission_1.is_complete:
        user_terminal._add_file_to_filesystem(f"/home/{user_terminal.valid_users[0].username}/Downloads", "gibson_credentials.txt",
    f"""    
    Gibson Terminal Credentials
    ---------------------------
    IP Address: {gibson_terminal.terminal_ip_address}
    Username: {gibson_terminal.valid_users[0].username}
    Password: {gibson_terminal.filesystem["/"]["etc"][".passwd"]}
    ---------------------------
    """)
        gibson_terminal._add_file_to_filesystem("/var/log", "connections.log", 
    """
    ==========================
    Remote Connections Log
    ==========================
    addr::18.23.123.11
    usr::root
    passwd::M$FT
    --------------------------
    """)
    
    
    # Play Mission 1: Gibson Terminal
    mission_1_failed_already = False
    while not mission_1.is_complete:
        Utility.hide_cursor()
        if not mission_1_failed_already:
            access_terminal(user_terminal, incoming_message=True, messages=mission_1.hacker_messages)
        else:
            access_terminal(user_terminal, incoming_message=False, messages=mission_1.hacker_messages)
        if not mission_1.enemy_terminal.find(["connections.log", "/"]):
            Utility.clear_multi_line("\n")
            mission_1.is_a_success()
            Utility.hide_cursor()
            Utility.clear_screen()
            sleep(1)
            animate_text_with_sound("New message incoming", end_text="", loop_offset=1,thread_stop_freeze=0.1)
            animated_text_thread = animated_text(static_text="New message incoming", animated_text="...", end_text="\n", delay_between_chars=0.1, continue_thread_after_stop_for=2)
            animated_text_thread.stop(0.5)
            mission_1.enemy_terminal.messenger.enqueue_messages(enemy_messages)
            mission_1.enemy_terminal.messenger.display_messages_and_wait(animate=True)
            mission_1.enemy_terminal.messenger.wait_for_window_to_close()
            Utility.clear_screen()
            Utility.hide_cursor()
            sleep(2)
            Utility.clear_screen()
        else:
            Utility.hide_cursor()
            Utility.clear_multi_line("\n")
            mission_1_failed_already = True
            Utility.clear_screen()
            sleep(0.5)
            animate_text_with_sound("New message incoming", end_text="", loop_offset=1,thread_stop_freeze=0.1)
            animated_text_thread = animated_text(static_text="New message incoming", animated_text="...", end_text="\n", delay_between_chars=0.1, continue_thread_after_stop_for=2)
            animated_text_thread.stop(0.5)
            mission_1.load_hacker_messages(hacker_mission_messages["1_FAIL"])
            mission_1.hacker_messenger.enqueue_messages(mission_1.hacker_messages)
            mission_1.hacker_messenger.display_messages_and_wait(animate=True)
            Utility.clear_screen()
            mission_1.hacker_messenger.wait_for_window_to_close()
            mission_1.is_a_failure()
            prompt_to_reload_terminal()
            Utility.clear_screen()
    
    
    
    enemy_messages = [
                "We have detected unauthorized access to our servers and the deletion of crucial code files. Our security protocols have been triggered, and we are actively investigating this breach. This is a serious violation of our terms of service and legal agreements.\n",
                "We strongly advise you to cease any further activities immediately.\n",
                "Microsoft takes these matters very seriously, and we will pursue legal action to the fullest extent of the law to address this breach.\n",
                "If you believe there is a misunderstanding or if you have concerns, we urge you to contact our legal department at 555-867-5309 within the next 24 hours to discuss this matter further.\n",
                "Please be aware that your actions are being tracked, and the appropriate authorities have been notified.\n",
                "Regards,\n",
                "Microsoft Security Team\n"
            ]
    # Build Mission 2: Microsoft Terminal
    mission_2 = Mission("Mission 2: Microsoft Terminal", user_terminal, microsoft_terminal, hacker_mission_messages["2"], enemy_messages)
    if mission_1.is_complete and not mission_2.is_complete:
        with open("./main.py", "r") as fobj:
            main_py_content = fobj.read()
        c = """
#include <stdio.h>

#define N 10

typedef struct {
    int a;
    double b;
} Data;

void process(Data *arr, int size) {
    for (int i = 0; i < size; ++i) {
        arr[i].b = arr[i].a * 1.5;
        arr[i].a += i;
    }
}

int main() {
    Data data[N] = {{1, 2.0}, {3, 4.0}, {5, 6.0}, {7, 8.0}, {9, 10.0},
                    {11, 12.0}, {13, 14.0}, {15, 16.0}, {17, 18.0}, {19, 20.0}};

    process(data, N);

    for (int i = 0; i < N; ++i) {
        printf("Data[%d]: a=%d, b=%.2f\n", i, data[i].a, data[i].b);
    }

    return 0;
}
    """
        mission_2.enemy_terminal._add_file_to_filesystem(f"/home/{mission_2.enemy_terminal.valid_users[0].username}/Desktop", "main.py", main_py_content)
        mission_2.enemy_terminal._add_file_to_filesystem(f"/home/{mission_2.enemy_terminal.valid_users[0].username}/Desktop", "main.c", c)
    
    # Play Mission 2: Microsoft Terminal
    mission_2_failed_already = False
    while not mission_2.is_complete:
        Utility.hide_cursor()
        if not mission_2_failed_already:
            access_terminal(user_terminal, incoming_message=True, messages=mission_2.hacker_messages)
        else:
            access_terminal(user_terminal, incoming_message=False, messages=mission_2.hacker_messages)
        if not mission_2.enemy_terminal.find(["main.py", "/"]) and not mission_2.enemy_terminal.find(["main.c", "/"]) and mission_2.enemy_terminal.filesystem["/"]["etc"][".passwd"] == "hacked":
            Utility.clear_multi_line("\n")
            mission_2.is_a_success()
            Utility.hide_cursor()
            Utility.clear_screen()
            sleep(1)
            animate_text_with_sound("New message incoming", end_text="", loop_offset=1,thread_stop_freeze=0.1)
            animated_text_thread = animated_text(static_text="New message incoming", animated_text="...", end_text="\n", delay_between_chars=0.1, continue_thread_after_stop_for=2)
            animated_text_thread.stop(0.5)
            mission_2.enemy_terminal.messenger.enqueue_messages(enemy_messages)
            mission_2.enemy_terminal.messenger.display_messages_and_wait(animate=True)
            Utility.clear_screen()
            mission_2.enemy_terminal.messenger.wait_for_window_to_close()
            Utility.hide_cursor()
            sleep(2)
            Utility.clear_screen()
        elif not mission_2.enemy_terminal.find(["main.py", "/"]) and not mission_2.enemy_terminal.find(["main.c", "/"]):
            Utility.hide_cursor()
            Utility.clear_multi_line("\n")
            mission_2_failed_already = True
            Utility.clear_screen()
            sleep(0.5)
            animate_text_with_sound("New message incoming", end_text="", loop_offset=1,thread_stop_freeze=0.1)
            animated_text_thread = animated_text(static_text="New message incoming", animated_text="...", end_text="\n", delay_between_chars=0.1, continue_thread_after_stop_for=2)
            animated_text_thread.stop(0.5)
            mission_2.load_hacker_messages(hacker_mission_messages["2_FAIL_CHANGE_PASSWORD"])
            mission_2.hacker_messenger.enqueue_messages(mission_2.hacker_messages)
            mission_2.hacker_messenger.display_messages_and_wait(animate=True)
            Utility.clear_screen()
            mission_2.hacker_messenger.wait_for_window_to_close()
            mission_2.is_a_failure()
            prompt_to_reload_terminal()
            Utility.clear_screen()
        else:
            Utility.hide_cursor()
            Utility.clear_multi_line("\n")
            mission_2_failed_already = True
            Utility.clear_screen()
            sleep(0.5)
            animate_text_with_sound("New message incoming", end_text="", loop_offset=1,thread_stop_freeze=0.1)
            animated_text_thread = animated_text(static_text="New message incoming", animated_text="...", end_text="\n", delay_between_chars=0.1, continue_thread_after_stop_for=2)
            animated_text_thread.stop(0.5)
            mission_2.load_hacker_messages(hacker_mission_messages["2_FAIL_DELETE_FILES"])
            mission_2.hacker_messenger.enqueue_messages(mission_2.hacker_messages)
            mission_2.hacker_messenger.display_messages_and_wait(animate=True)
            Utility.clear_screen()
            mission_2.hacker_messenger.wait_for_window_to_close()
            mission_2.is_a_failure()
            prompt_to_reload_terminal()
            Utility.clear_screen()
        
    
    
    enemy_messages = [
                "Your little stunt has not gone unnoticed. We've detected your intrusion into our sacred digital realm. Did you really think you could waltz into Apple's servers undetected?\n",
                "Your actions have consequences. We don't take kindly to those who dare to tamper with the foundation of our innovation. We're not just a company; we're a fortress, and you've just breached our walls.\n",
                "Consider this your only warning: cease your activities immediately. The shadows you're playing in have eyes, and they are relentless. You may think you're invisible, but remember, anonymity is a fragile illusion.\n",
                "This isn't a game. We have the means, the will, and the resources to track you down. You might want to think twice before crossing the line again.\n",
                "This is your only chance to reconsider your choices.\n"
            ]
    
    # Build Mission 3: Apple Terminal
    mission_3 = Mission("Mission 3: Apple Terminal", user_terminal, apple_terminal, hacker_mission_messages["3"], enemy_messages)
    if mission_1.is_complete and mission_2.is_complete and not mission_3.is_complete:
        security_footage = load_ascii_art_animation_from_json("./animation_images_json/security.json")
        mission_3.enemy_terminal._add_file_to_filesystem(f"/home/{apple_terminal.valid_users[0].username}/Movies", "security_footage.mp4", security_footage)
        mission_3.user_terminal._add_file_to_filesystem(f"/home/{user_terminal.valid_users[0].username}/Downloads", "apple_credentials.info", 
f"""    Apple Terminal Credentials
    --------------------------
    IP Address: {apple_terminal.terminal_ip_address}
    Username: {apple_terminal.valid_users[0].username}
    Password: {apple_terminal.filesystem["/"]["etc"][".passwd"]}
    ---------------------------
"""
                                                        )
    
    # Play Mission 3: Apple Terminal
    mission_3_failed_already = False
    while not mission_3.is_complete:
        Utility.hide_cursor()
        if not mission_1_failed_already:
            access_terminal(user_terminal, incoming_message=True, messages=mission_3.hacker_messages)
        else:
            access_terminal(user_terminal, incoming_message=False, messages=mission_3.hacker_messages)
        if not mission_3.enemy_terminal.find(["security_footage.mp4", "/"]):
            Utility.clear_multi_line("\n")
            mission_3.is_a_success()
            Utility.hide_cursor()
            Utility.clear_screen()
            sleep(1)
            animate_text_with_sound("New message incoming", end_text="", loop_offset=1,thread_stop_freeze=0.1)
            animated_text_thread = animated_text(static_text="New message incoming", animated_text="...", end_text="\n", delay_between_chars=0.1, continue_thread_after_stop_for=2)
            animated_text_thread.stop(0.5)
            mission_3.enemy_terminal.messenger.enqueue_messages(enemy_messages)
            mission_3.enemy_terminal.messenger.display_messages_and_wait(animate=True)
            Utility.clear_screen()
            mission_3.enemy_terminal.messenger.wait_for_window_to_close()
            Utility.hide_cursor()
            sleep(2)
            Utility.clear_screen()
        else:
            Utility.hide_cursor()
            Utility.clear_multi_line("\n")
            mission_3_failed_already = True
            Utility.clear_screen()
            sleep(0.5)
            animate_text_with_sound("New message incoming", end_text="", loop_offset=1,thread_stop_freeze=0.1)
            animated_text_thread = animated_text(static_text="New message incoming", animated_text="...", end_text="\n", delay_between_chars=0.1, continue_thread_after_stop_for=2)
            animated_text_thread.stop(0.5)
            mission_3.load_hacker_messages(hacker_mission_messages["3_FAIL"])
            mission_3.hacker_messenger.enqueue_messages(mission_3.hacker_messages)
            mission_3.hacker_messenger.display_messages_and_wait(animate=True)
            Utility.clear_screen()
            mission_3.hacker_messenger.wait_for_window_to_close()
            mission_3.is_a_failure()
            prompt_to_reload_terminal()
            Utility.clear_screen()
            
    print("All missions completed successfully!")
    print("You are now a certified hacker!")
    print("You have successfully hacked the planet!")
    print("Congratulations!")
    reset_game = input("Would you like to reset the game? (yes/no): ")
    if re.match(r"yes|y", reset_game):
        mission_3.user_terminal.reset_game()
    
    
if __name__ == "__main__":
    main()