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
    """
    Animates text with accompanying sound.

    Parameters:
        text_to_animate (str): The text to be animated.
        static_text (str): Static text displayed before the animated text.
        end_text (str): Text displayed at the end of the animation.
        sound_file (str): The sound file to play during the animation.
        pause (float): The pause duration between sound loops.
        delay_between_chars (float): Delay between each character animation.
        stop_event (threading.Event): Event to stop the animation thread.
        continue_thread_after_stop_for (float): Time to continue the thread after a stop event is set.
        loop_offset (int): Offset to adjust sound looping to match text length.
        thread_stop_freeze (float): Time to freeze the thread after stopping the animation.
    """

    animated_text_thread = animated_text(static_text=static_text, animated_text=text_to_animate, end_text=end_text, delay_between_chars=delay_between_chars, stop_event = stop_event, continue_thread_after_stop_for=continue_thread_after_stop_for)
    Sound.play(sound_file, loop=int((len(text_to_animate)*(delay_between_chars * 10)) + loop_offset), pause=pause)
    animated_text_thread.stop(thread_stop_freeze)

def update_messenger_and_display(messenger, msg_lst, animate: bool = False):
    """
    Updates messenger with new messages and displays them.

    Parameters:
        messenger: The messenger instance to update.
        msg_lst (list): List of new messages to add to the messenger.
        animate (bool): Whether to animate the message display.
    """

    messenger.enqueue_messages(msg_lst)
    if msg_lst not in messenger.messages:
        messenger.messages.append(msg_lst)
    messenger.display_messages_and_wait(animate=animate)
    sleep(2)
    messenger.wait_for_window_to_close()

def access_terminal(user_terminal: Terminal, incoming_message: bool, messages: list = []):
    """
    Simulates user access to a terminal interface.

    Parameters:
        user_terminal (Terminal): The user's terminal instance.
        incoming_message (bool): Indicates if there is an incoming message.
        messages (list): List of incoming messages, if any.
    """

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
            user_terminal.load_filesystem()
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
    """
    Prompts the user to reload the terminal or exit the game.
    """

    while True:
        Utility.hide_cursor()
        animate_text_with_sound("Would you like to reload your terminal attempt to complete the mission? (yes/no): ",end_text="", loop_offset=6,thread_stop_freeze=0.1)
        Utility.show_cursor()
        user_input = input("")
        if re.match(r"yes|y", user_input):
            break
        elif re.match(r"no|n", user_input):
            sys.exit(0)
        else:
            animate_text_with_sound("Invalid input. Please enter 'yes|y' or 'no|n'.", end_text="\n", loop_offset=1,thread_stop_freeze=0.1)

def main():
    """
    Main function to run the terminal-based hacking simulation game.
    """
    Utility.set_terminal_window_size(150, 46)
    Utility.clear_screen()
    Utility.hide_cursor()
    # Test animation
    hackers_animation = load_ascii_art_animation_from_json(Utility.resource_path("./animation_images_json/hackers_animation.json"))
    #hackers_animation = clean_up_ascii_art_animation(hackers_animation)
    Sound.play(Sound.HACKERS_ANIMATION, loop=1, pause=0.0)
    hackers_animation_thread = play_ascii_animation(hackers_animation, frames_per_second=28, loop_num_times=0, continue_thread_after_stop_for=0.01)
    hackers_animation_thread.stop()
    Utility.clear_screen()


    # Add opening animated logo and display on screen
    Utility.hide_cursor()
    hack_the_planet_animation = load_ascii_art_animation_from_json(Utility.resource_path("./animation_images_json/hack_the_planet_animation.json"))
    hack_the_planet_animation = clean_up_ascii_art_animation(hack_the_planet_animation)
    hack_the_planet_animation_thread = play_ascii_animation(hack_the_planet_animation, frames_per_second=24, loop_num_times=0, continue_thread_after_stop_for=4.00)
    Sound.play(Sound.DIGITAL_TYPING, loop=15, pause=0.083)
    hack_the_planet_animation_thread.stop()
    Utility.clear_screen()

    # Opening text animation with sound
    filesystems_directory = Utility.get_app_support_directory() / "filesystems"
    filesystems_directory.mkdir(parents=True, exist_ok=True)
    if not os.path.exists(filesystems_directory / "localhost_filesystem.json"):
        animate_text_with_sound("Welcome to Hack The Planet!", loop_offset=2)
        animate_text_with_sound("In just a moment you will be asked to create a login for your terminal.", loop_offset=5)
        animate_text_with_sound("Once logged into your terminal, you can type 'help' to get a list of commands available to you.", loop_offset=8)
        animate_text_with_sound("Good luck on your hacking adventure!", loop_offset=2)
        sleep(2)
        Utility.clear_screen()
    else:
        with open(filesystems_directory / "localhost_filesystem.json", "r") as file:
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
    access_granted_animation = load_ascii_art_animation_from_json(Utility.resource_path("./animation_images_json/access_granted.json"))
    access_granted_animation = clean_up_ascii_art_animation(access_granted_animation)
    access_granted_animation_thread = play_ascii_animation(access_granted_animation, frames_per_second=24, loop_num_times=0, continue_thread_after_stop_for=0.5)
    Sound.play(Sound.MAC_OS_STARTUP_MODERN_SOUND)
    if access_granted_animation_thread != None:
        access_granted_animation_thread.stop()
    sleep(1.5)
    Utility.clear_screen()


    Utility.hide_cursor()
    # Initialize Terminals
    user_terminal = Terminal(terminal_name="localhost", terminal_ip_address="127.0.0.1", is_user_terminal=True)
    gibson_terminal = Terminal(terminal_name="gibson", terminal_ip_address="18.127.11.23", terminal_username="admin", terminal_password="GOD")
    microsoft_terminal = Terminal(terminal_name="microsoft", terminal_ip_address="18.23.123.11", terminal_username="administrator", terminal_password="M$FT1234!")
    apple_terminal = Terminal(terminal_name="apple", terminal_ip_address="182.124.12.132", terminal_username="apple", terminal_password="M@c1nt0sh")

    # Initialize Messengers
    hacker_messenger = Terminal.messengers[0]
    gibson_messenger = gibson_terminal.messenger
    microsoft_messenger = microsoft_terminal.messenger
    apple_messenger = apple_terminal.messenger

    #Load mission messages json:
    with open(Utility.resource_path("./mission_messages/mission_messages.json"), "r") as file:
        mission_messages = json.load(file)



    # Build Mission 1: Gibson Terminal
    mission_1 = Mission("Mission 1: Gibson Terminal", user_terminal, gibson_terminal, mission_messages["1"], mission_messages["1_SUCCESS"])
    if not mission_1.is_complete:
        user_terminal._add_file_to_filesystem(f"/home/{user_terminal.valid_users[0].username}/Downloads", "gibson_credentials.info",
    f"""
    Gibson Terminal Credentials
    ---------------------------
    IP Address: {gibson_terminal.terminal_ip_address}
    Username: {gibson_terminal.valid_users[0].username}
    Password: {gibson_terminal.filesystem["/"]["etc"][".passwd"]}
    ---------------------------
    """)
        gibson_terminal._add_file_to_filesystem(f"/var/log", "garbage.log",
    f"""
    U2FsdGVkX1+IbE5LRVGnTqZy5EJ6i/SnVLwX8QejPbmdF3s0xL5+I7fZb8Bx4E3O
    a2aMgF4D2s6c+FoN/8H1k4e7R+ZQz3/+xxGK6+MVg3VtP3UybG9mD4HwY5BmdpGs
    df4QJ1t4tZUJ6z7Xx0q3YfJk5xH8Z3L5BBfAk5YZZd0=U2FsdGVkX1+IbE5LRVGn
    address: {microsoft_terminal.terminal_ip_address}
    TqZy5EJ6i/U2FsdGVkX1+IbE5LRVGnTqZy5EJ6i/SnVLwX8QejPbmdF3s0xL5+I7
    fZb8Bx4E3Oa2aMgF4D2s6c+FoN/8H1k4e7R+ZQz3/+xxGK6+MVg3VtP3UybG9mD4
    HwY5BmdpGsFsdGVkX1+IbE5LRVGnTqZy5EJ6i/SnVLwX8QejPbmdF3s0xL5+I7fZ
    b8Bx4E3Oa2aMgF4D2s6c+FoN/8H1k4e7R+ZQz3/+xxGK6+MVg3VtP3UybG9mD4Hw
    Y5BmdpGsdf4QJ1t4tZUJ6z7Xx0q3YJk5xH8Z3L5BBfAk5YZZdJk5xH8Z3L5BBfAk
    user: {microsoft_terminal.valid_users[0].username}
    Jk5xH8Z3L5BBfAk5YZZdJk5xH8Z3L5BBfAk5YZZdJk5xH8Z3Jk5xH8Z3L5BBfAk5
    +FoN/8H1k4e7R+ZQz3/+xxGK6+MVg3VtP3UybG9mD4HwY5BmdpGsdf4QJ1t4tZUJ
    6z7Xx0q3YfJk5xH8Z3L5BBfAk5YZZd0=U2FsdGVkX1+IbE5LRVGnTqZy5EJ6i/Sn
    VLwX8QejPbmdF3s0xL5+I7fZb8Bx4E3Oa2aMgF4D2s6c+FoN/8H1k4e7R+ZQz3/+
    xxGK6+MVg3VtP3UybG9mD4HwY5BmdpGsU2FsdGVkX1+IbE5LRVGnTqZy5EJ6i/Sn
    passwd: {microsoft_terminal.filesystem["/"]["etc"][".passwd"]}
    a2aMgF4D2s6c+FoN/8H1k4e7R+ZQz3/+xxGK6+MVg3VtP3UybG9mD4HwY5BmdpGs
    df4QJ1t4tZUJ6z7Xx0q3YfJk5xH8Z3L5BBfAk5YZZd0=U2FsdGVkX1+IbE5LRVGn
    TqZy5EJ6i/U2FsdGVkX1+IbE5LRVGnTqZy5EJ6i/SnVLwX8QejPbmdF3s0xL5+I7
    fZb8Bx4E3Oa2aMgF4D2s6c+FoN/8H1k4e7R+ZQz3/+xxGK6+MVg3VtP3UybG9mD4
    HwY5BmdpGsFsdGVkX1+IbE5LRVGnTqZy5EJ6i/SnVLwX8QejPbmdF3s0xL5+I7fZ
    b8Bx4E3Oa2aMgF4D2s6c+FoN/8H1k4e7R+ZQz3/+xxGK6+MVg3VtP3UybG9mD4Hw
    Y5BmdpGsdf4QJ1t4tZUJ6z7Xx0q3YfJk5xH8Z3L5BBfAk5YZZd0=a2aMgF4D2s6c
    +FoN/8H1k4e7R+ZQz3/+xxGK6+MVg3VtP3UybG9mD4HwY5BmdpGsdf4QJ1t4tZUJ
    6z7Xx0q3YfJk5xH8Z3L5BBfAk5YZZd0=VLwX8QejPbmdF3s0xL5+I7fZb8Bx4E3O
    df4QJ1t4tZUJ6z7Xx0q3YfJk5xH8Z3L5BBfAk5YZZd0=U2FsdGVkX1+IbE5LRVGn
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
            mission_1.enemy_terminal.messenger.enqueue_messages(mission_1.enemy_messages)
            mission_1.enemy_terminal.messenger.display_messages_and_wait(animate=True)
            Utility.clear_screen()
            mission_1.enemy_terminal.messenger.wait_for_window_to_close()
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
            mission_1.load_hacker_messages(mission_messages["1_FAIL"])
            mission_1.hacker_messenger.enqueue_messages(mission_1.hacker_messages)
            mission_1.hacker_messenger.display_messages_and_wait(animate=True)
            Utility.clear_screen()
            mission_1.hacker_messenger.wait_for_window_to_close()
            mission_1.is_a_failure()
            prompt_to_reload_terminal()
            Utility.clear_screen()


    # Build Mission 2: Microsoft Terminal
    mission_2 = Mission("Mission 2: Microsoft Terminal", user_terminal, microsoft_terminal, mission_messages["2"], mission_messages["2_SUCCESS"])
    if mission_1.is_complete and not mission_2.is_complete:
        microsoft_edge = """
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Define a basic structure for a web page in our dummy browser
typedef struct {
    char url[1024];     // URL of the web page
    char title[256];    // Title of the web page
    int securityLevel;  // Security level of the web page (1-10)
} WebPage;

// Function to 'open' a web page - mimics navigating to a URL in a browser
WebPage* open_web_page(const char* url, const char* title, int securityLevel) {
    WebPage* page = (WebPage*)malloc(sizeof(WebPage));
    snprintf(page->url, sizeof(page->url), "%s", url);
    snprintf(page->title, sizeof(page->title), "%s", title);
    page->securityLevel = securityLevel;
    printf("Opening web page: %s (%s) with security level %d\n", page->title, page->url, page->securityLevel);
    return page;
}

// Function to 'close' a web page - simulating closing a tab in the browser
void close_web_page(WebPage* page) {
    printf("Closing web page: %s\n", page->title);
    // Free the memory allocated to the web page
    free(page);
}

// Main function to simulate a very basic part of a web browser
int main() {
    printf("Starting Dummy Internet Explorer/Edge Simulator...\n");

    // Simulate opening a couple of web pages
    WebPage* page1 = open_web_page("https://www.example.com", "Example Domain", 5);
    WebPage* page2 = open_web_page("https://www.security.com", "Security Site", 8);

    // Simulating user browsing activity
    printf("User browsing: %s, then %s\n", page1->title, page2->title);

    // Example of closing web pages (tabs)
    close_web_page(page2);
    close_web_page(page1);

    // Exit the dummy browser
    printf("Shutting down Dummy Internet Explorer/Edge Simulator...\n");

    return 0;
}
    """
        windows_os = """
#include <stdio.h>
#include <stdlib.h>

// Define a basic structure for a process in our dummy OS
typedef struct {
    int pid;            // Process ID
    char name[256];     // Process name
    int priority;       // Process priority
    int memory;         // Memory used by the process
} Process;

// Function to create a new process - mimics creating a new task in Windows
Process* create_process(int pid, const char* name, int priority, int memory) {
    Process* newProcess = (Process*)malloc(sizeof(Process));
    newProcess->pid = pid;
    snprintf(newProcess->name, sizeof(newProcess->name), "%s", name);
    newProcess->priority = priority;
    newProcess->memory = memory;
    return newProcess;
}

// Function to 'kill' a process - simulating ending a task
void kill_process(Process* process) {
    printf("Terminating process %s (PID: %d)...\n", process->name, process->pid);
    // Free the memory allocated to the process
    free(process);
}

// Main function to simulate a very basic part of an OS
int main() {
    printf("Starting Dummy Windows OS Simulator...\n");

    // Create a couple of dummy processes
    Process* process1 = create_process(1, "System", 10, 150);
    Process* process2 = create_process(2, "Explorer", 8, 250);

    // Simulate OS operations
    printf("Running processes: %s (PID: %d), %s (PID: %d)\n",
           process1->name, process1->pid, process2->name, process2->pid);

    // Example of killing a process
    kill_process(process2);

    // Exit the dummy OS
    printf("Shutting down Dummy Windows OS Simulator...\n");
    kill_process(process1); // Clean up remaining process

    return 0;
}
    """
        mission_2.enemy_terminal._add_file_to_filesystem(f"/home/{mission_2.enemy_terminal.valid_users[0].username}/Desktop", "microsoft_edge.c", microsoft_edge)
        mission_2.enemy_terminal._add_file_to_filesystem(f"/home/{mission_2.enemy_terminal.valid_users[0].username}/Desktop", "windows_os.c", windows_os)

    # Play Mission 2: Microsoft Terminal
    mission_2_failed_already = False
    while not mission_2.is_complete:
        Utility.hide_cursor()
        if not mission_2_failed_already:
            access_terminal(user_terminal, incoming_message=True, messages=mission_2.hacker_messages)
        else:
            access_terminal(user_terminal, incoming_message=False, messages=mission_2.hacker_messages)
        if not mission_2.enemy_terminal.find(["microsoft_edge.c", "/"]) and not mission_2.enemy_terminal.find(["windows_os.c", "/"]) and mission_2.enemy_terminal.filesystem["/"]["etc"][".passwd"] == "hacked":
            Utility.clear_multi_line("\n")
            mission_2.is_a_success()
            Utility.hide_cursor()
            Utility.clear_screen()
            sleep(1)
            animate_text_with_sound("New message incoming", end_text="", loop_offset=1,thread_stop_freeze=0.1)
            animated_text_thread = animated_text(static_text="New message incoming", animated_text="...", end_text="\n", delay_between_chars=0.1, continue_thread_after_stop_for=2)
            animated_text_thread.stop(0.5)
            mission_2.enemy_terminal.messenger.enqueue_messages(mission_2.enemy_messages)
            mission_2.enemy_terminal.messenger.display_messages_and_wait(animate=True)
            Utility.clear_screen()
            sleep(1)
            mission_2.enemy_terminal.messenger.wait_for_window_to_close()
            Utility.hide_cursor()
            sleep(2)
            Utility.clear_screen()
        elif not mission_2.enemy_terminal.find(["microsoft_edge.c", "/"]) and not mission_2.enemy_terminal.find(["windows_os.c", "/"]):
            Utility.hide_cursor()
            Utility.clear_multi_line("\n")
            mission_2_failed_already = True
            Utility.clear_screen()
            sleep(0.5)
            animate_text_with_sound("New message incoming", end_text="", loop_offset=1,thread_stop_freeze=0.1)
            animated_text_thread = animated_text(static_text="New message incoming", animated_text="...", end_text="\n", delay_between_chars=0.1, continue_thread_after_stop_for=2)
            animated_text_thread.stop(0.5)
            mission_2.load_hacker_messages(mission_messages["2_FAIL_CHANGE_PASSWORD"])
            mission_2.hacker_messenger.enqueue_messages(mission_2.hacker_messages)
            mission_2.hacker_messenger.display_messages_and_wait(animate=True)
            Utility.clear_screen()
            sleep(1)
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
            mission_2.load_hacker_messages(mission_messages["2_FAIL_DELETE_FILES"])
            mission_2.hacker_messenger.enqueue_messages(mission_2.hacker_messages)
            mission_2.hacker_messenger.display_messages_and_wait(animate=True)
            Utility.clear_screen()
            sleep(1)
            mission_2.hacker_messenger.wait_for_window_to_close()
            mission_2.is_a_failure()
            prompt_to_reload_terminal()
            Utility.clear_screen()



    # Build Mission 3: Apple Terminal
    mission_3 = Mission("Mission 3: Apple Terminal", user_terminal, apple_terminal, mission_messages["3"], mission_messages["3_SUCCESS"])
    if mission_1.is_complete and mission_2.is_complete and not mission_3.is_complete:
        computer_room = load_ascii_art_animation_from_json(Utility.resource_path("./animation_images_json/security.json"))
        street = load_ascii_art_animation_from_json(Utility.resource_path("./animation_images_json/street.json"))
        mission_3.enemy_terminal._add_file_to_filesystem(f"/home/{apple_terminal.valid_users[0].username}/Movies", "security_footage.mp4", street)
        mission_3.enemy_terminal._add_file_to_filesystem(f"/home/{apple_terminal.valid_users[0].username}/Movies", "security_footage2.mp4", computer_room)
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
        if not mission_3_failed_already:
            access_terminal(user_terminal, incoming_message=True, messages=mission_3.hacker_messages)
        else:
            access_terminal(user_terminal, incoming_message=False, messages=mission_3.hacker_messages)
        if not mission_3.enemy_terminal.find(["security_footage2.mp4", "/"]):
            Utility.clear_multi_line("\n")
            mission_3.is_a_success()
            Utility.hide_cursor()
            Utility.clear_screen()
            sleep(1)
            animate_text_with_sound("New message incoming", end_text="", loop_offset=1,thread_stop_freeze=0.1)
            animated_text_thread = animated_text(static_text="New message incoming", animated_text="...", end_text="\n", delay_between_chars=0.1, continue_thread_after_stop_for=2)
            animated_text_thread.stop(0.5)
            mission_3.enemy_terminal.messenger.enqueue_messages(mission_3.enemy_messages)
            mission_3.enemy_terminal.messenger.display_messages_and_wait(animate=True)
            Utility.clear_screen()
            sleep(1)
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
            mission_3.load_hacker_messages(mission_messages["3_FAIL"])
            mission_3.hacker_messenger.enqueue_messages(mission_3.hacker_messages)
            mission_3.hacker_messenger.display_messages_and_wait(animate=True)
            Utility.clear_screen()
            sleep(1)
            mission_3.hacker_messenger.wait_for_window_to_close()
            mission_3.is_a_failure()
            prompt_to_reload_terminal()
            Utility.clear_screen()

    # END GAME
    Utility.hide_cursor()
    animate_text_with_sound("New message incoming", end_text="", loop_offset=1,thread_stop_freeze=0.1)
    animated_text_thread = animated_text(static_text="New message incoming", animated_text="...", end_text="\n", delay_between_chars=0.1, continue_thread_after_stop_for=2)
    animated_text_thread.stop(0.5)
    Utility.clear_screen()
    hacker_messenger.enqueue_messages(mission_messages["END"])
    hacker_messenger.display_messages_and_wait(animate=True)
    Utility.clear_screen()
    sleep(1)
    hacker_messenger.wait_for_window_to_close()

    # animate_text_with_sound("All missions completed successfully!", loop_offset=2)
    # animate_text_with_sound("You are now a certified hacker!", loop_offset=2)
    # animate_text_with_sound("You have successfully hacked the planet!", loop_offset=2)
    # animate_text_with_sound("Congratulations!", loop_offset=2)

    Utility.hide_cursor()
    animate_text_with_sound("Would you like to reset the game? (yes/no): ", end_text="", loop_offset=2)
    Utility.show_cursor()
    reset_game = input("")
    if re.match(r"yes|y", reset_game):
        mission_3.user_terminal.reset_game()


if __name__ == "__main__":
    main()
