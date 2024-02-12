from sound import Sound
from animation import Animation
from utility import Utility

def main():
    Utility.clear_screen()
    Utility.hide_cursor()
    dialing_phone_num_text_animation = Animation.text_animating_after_static_text("Dialing phone number", end_text="Complete!\n", delay_animation= 0.2, hold_thread_for= 1)
    Sound.play(Sound.DIAL_TONE, pause= 1)
    Sound.play(Sound.DIALING_PHONE_NUMBER, pause = 2.4)
    dialing_phone_num_text_animation.stop(hold_thread_for= 1)
    connect_to_computer_text_animation = Animation.text_animating_after_static_text("Connecting to computer over modem", end_text="Complete!\n", delay_animation= 0.2, hold_thread_for= 1)
    Sound.play(Sound.CONNECTING_TO_COMPUTER_OVER_MODEM_SHORT, pause = 9)
    connect_to_computer_text_animation.stop(hold_thread_for= 1)
    booting_up_computer_text_animation = Animation.text_animating_after_static_text("Booting up computer", end_text="Complete!\n", delay_animation= 0.2, hold_thread_for=3)
    Sound.play(Sound.MAC_OS_STARTUP_MODERN_SOUND, pause= 5)
    booting_up_computer_text_animation.stop(hold_thread_for= 1)
    print("Computer booted up!")
    print_animated_message1 = Animation.text_animating_after_static_text(static_text="", animated_text="I can also print animated messages like this one! Depending on how long I hold it for, I can animated it more than once!", end_text="\n", delay_animation= 0.02, hold_thread_for= 1)
    print_animated_message1.stop(hold_thread_for= 2)
    print_animated_message2 = Animation.text_animating_after_static_text(static_text="", animated_text="I can print fast,", delay_animation= 0.05, hold_thread_for= 0.1)
    print_animated_message2.stop(0.01)
    print_animated_message3 = Animation.text_animating_after_static_text(static_text="I can print fast,", animated_text=" or I can print slow,", delay_animation= 0.2, hold_thread_for= 0.1)
    print_animated_message3.stop(0.01)
    print_animated_message4 = Animation.text_animating_after_static_text(static_text="I can print fast, or I can print slow,", animated_text=" or I can print very slow!", end_text="\n", delay_animation= 0.4, hold_thread_for= 1)
    print_animated_message4.stop(0.01)
    
    
    

if __name__ == '__main__':
    main()