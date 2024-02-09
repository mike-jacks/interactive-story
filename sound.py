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
    
    
    @staticmethod
    def play(sound_file: str = MAC_OS_STARTUP_MODERN_SOUND, num_of_times: int = 1, speed: float = 0.0):
        def sound_thread():
            playsound(sound_file)
        for i in range(num_of_times):
            threading.Thread(target=sound_thread).start()
            sleep(speed)
    
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