from time import sleep
import threading
from playsound import playsound

from utility import Utility

class Sound:
    """
    A class to manage and play sound files for various system and custom notifications.

    Attributes:
        Constants representing file paths to various sound files.
    """

    # Sound file paths
    MAC_OS_ERROR_1_SOUND = Utility.resource_path('sounds/mac_os_error_1.wav')
    MAC_OS_ERROR_2_SOUND = Utility.resource_path('sounds/mac_os_error_2.wav')
    MAC_OS_NOTIFICAITON_1_SOUND = Utility.resource_path('sounds/mac_os_notification_1.wav')
    MAC_OS_NOTIFICATION_2_SOUND = Utility.resource_path('sounds/mac_os_notification_2.wav')
    MAC_OS_OLD_SCHOOL_ERROR_SOUND = Utility.resource_path('sounds/mac_os_old_school_error.wav')
    MAC_OS_STARTUP_CLASSIC_SOUND = Utility.resource_path('sounds/mac_os_startup_classic.wav')
    MAC_OS_STARTUP_MODERN_SOUND = Utility.resource_path('sounds/mac_os_startup_modern.wav')
    DIALING_PHONE_NUMBER = Utility.resource_path('sounds/dialing_phone_number.wav')
    CONNECTING_TO_COMPUTER_OVER_MODEM_LONG = Utility.resource_path('sounds/connecting_to_computer_over_modem_long.wav')
    CONNECTING_TO_COMPUTER_OVER_MODEM_SHORT = Utility.resource_path('sounds/connecting_to_computer_over_modem_short.wav')
    DIAL_TONE = Utility.resource_path('sounds/dial_tone.wav')
    DIGITAL_TYPING = Utility.resource_path('sounds/digital_typing.wav')
    COMPLETE_NOTIFICATION = Utility.resource_path('sounds/complete_notification.wav')
    HACKERS_ANIMATION = Utility.resource_path('sounds/hackers_animation.wav')


    @staticmethod
    def play(sound_file: str = MAC_OS_STARTUP_MODERN_SOUND, loop: int = 1, pause: float = 0.0):
        """
        Plays the specified sound file a given number of times with a pause between each play.

        Parameters:
            sound_file (str): The path to the sound file to be played.
            loop (int): The number of times the sound file is played.
            pause (float): The duration (in seconds) to wait between each play.
        """
        def sound_thread():
            playsound(sound_file)
        for i in range(loop):
            threading.Thread(target=sound_thread).start()
            sleep(pause)

    @staticmethod
    def crash():
        """
        Simulates a system crash sound sequence by playing a series of error sounds and startup sounds.
        """
        Sound.play(Sound.MAC_OS_STARTUP_CLASSIC_SOUND)
        Sound.play(Sound.MAC_OS_ERROR_1_SOUND, 2, 0)
        Sound.play(Sound.MAC_OS_ERROR_2_SOUND, 2, 0)
        Sound.play(Sound.MAC_OS_OLD_SCHOOL_ERROR_SOUND, 2, 0)
        Sound.play(Sound.MAC_OS_ERROR_1_SOUND)
        Sound.play(Sound.MAC_OS_ERROR_2_SOUND)
        Sound.play(Sound.MAC_OS_OLD_SCHOOL_ERROR_SOUND)
        Sound.play(Sound.MAC_OS_ERROR_1_SOUND)
        Sound.play(Sound.MAC_OS_ERROR_2_SOUND)
        Sound.play(Sound.MAC_OS_OLD_SCHOOL_ERROR_SOUND)
        Sound.play(Sound.MAC_OS_STARTUP_MODERN_SOUND, 2, 0)
        Sound.play(Sound.MAC_OS_ERROR_1_SOUND)
        Sound.play(Sound.MAC_OS_ERROR_2_SOUND)
        Sound.play(Sound.MAC_OS_OLD_SCHOOL_ERROR_SOUND)
        Sound.play(Sound.MAC_OS_ERROR_1_SOUND)
        Sound.play(Sound.MAC_OS_ERROR_2_SOUND)
        Sound.play(Sound.MAC_OS_OLD_SCHOOL_ERROR_SOUND)
        Sound.play(Sound.MAC_OS_ERROR_1_SOUND)
        Sound.play(Sound.MAC_OS_ERROR_2_SOUND)
        Sound.play(Sound.MAC_OS_OLD_SCHOOL_ERROR_SOUND)
        Sound.play(Sound.MAC_OS_ERROR_1_SOUND)
        Sound.play(Sound.MAC_OS_ERROR_2_SOUND)
        Sound.play(Sound.MAC_OS_STARTUP_CLASSIC_SOUND, 100, 0.04)
        Sound.play(Sound.MAC_OS_OLD_SCHOOL_ERROR_SOUND)
        Sound.play(Sound.MAC_OS_ERROR_1_SOUND)
        Sound.play(Sound.MAC_OS_ERROR_2_SOUND)
        Sound.play(Sound.MAC_OS_OLD_SCHOOL_ERROR_SOUND)
        Sound.play(Sound.MAC_OS_ERROR_1_SOUND)
        Sound.play(Sound.MAC_OS_ERROR_2_SOUND)
        Sound.play(Sound.MAC_OS_OLD_SCHOOL_ERROR_SOUND)
        Sound.play(Sound.MAC_OS_ERROR_1_SOUND)
        Sound.play(Sound.MAC_OS_ERROR_2_SOUND)
        Sound.play(Sound.MAC_OS_OLD_SCHOOL_ERROR_SOUND)
        Sound.play(Sound.MAC_OS_ERROR_1_SOUND)
        Sound.play(Sound.MAC_OS_ERROR_2_SOUND)
        Sound.play(Sound.MAC_OS_OLD_SCHOOL_ERROR_SOUND)
        Sound.play(Sound.MAC_OS_ERROR_1_SOUND)
        Sound.play(Sound.MAC_OS_ERROR_2_SOUND)
        Sound.play(Sound.MAC_OS_OLD_SCHOOL_ERROR_SOUND)
        Sound.play(Sound.MAC_OS_ERROR_1_SOUND)
