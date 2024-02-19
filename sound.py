from time import sleep
import threading
from playsound import playsound

class Sound:
    MAC_OS_ERROR_1_SOUND = 'sounds/mac_os_error_1.wav'
    MAC_OS_ERROR_2_SOUND = 'sounds/mac_os_error_2.wav'
    MAC_OS_NOTIFICAITON_1_SOUND = 'sounds/mac_os_notification_1.wav'
    MAC_OS_NOTIFICATION_2_SOUND = 'sounds/mac_os_notification_2.wav'
    MAC_OS_OLD_SCHOOL_ERROR_SOUND = 'sounds/mac_os_old_school_error.wav'
    MAC_OS_STARTUP_CLASSIC_SOUND = 'sounds/mac_os_startup_classic.wav'
    MAC_OS_STARTUP_MODERN_SOUND = 'sounds/mac_os_startup_modern.wav'
    DIALING_PHONE_NUMBER = 'sounds/dialing_phone_number.wav'
    CONNECTING_TO_COMPUTER_OVER_MODEM_LONG = 'sounds/connecting_to_computer_over_modem_long.wav'
    CONNECTING_TO_COMPUTER_OVER_MODEM_SHORT = 'sounds/connecting_to_computer_over_modem_short.wav'
    DIAL_TONE = 'sounds/dial_tone.wav'
    DIGITAL_TYPING = 'sounds/digital_typing.wav'
    COMPLETE_NOTIFICATION = 'sounds/complete_notification.wav'
    HACKERS_ANIMATION = 'sounds/hackers_animation.wav'
    
    
    @staticmethod
    def play(sound_file: str = MAC_OS_STARTUP_MODERN_SOUND, loop: int = 1, pause: float = 0.0):
        def sound_thread():
            playsound(sound_file)
        for i in range(loop):
            threading.Thread(target=sound_thread).start()
            sleep(pause)
    
    @staticmethod
    def crash():
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

# Write code in main function below to tes tthis file on its own:
if __name__ == '__main__':
    def main():
        pass

    main()