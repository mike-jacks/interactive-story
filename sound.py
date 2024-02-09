from time import sleep
import threading
from playsound import playsound

MAC_OS_ERROR_1_SOUND = 'sounds/mac_os_error_1.wav'
MAC_OS_ERROR_2_SOUND = 'sounds/mac_os_error_2.wav'
MAC_OS_NOTIFICAITON_1_SOUND = 'sounds/mac_os_notification_1.wav'
MAC_OS_NOTIFICATION_2_SOUND = 'sounds/mac_os_notification_2.wav'
MAC_OS_OLD_SCHOOL_ERROR_SOUND = 'sounds/mac_os_old_school_error.wav'
MAC_OS_STARTUP_CLASSIC_SOUND = 'sounds/mac_os_startup_classic.wav'
MAC_OS_STARTUP_MODERN_SOUND = 'sounds/mac_os_startup_modern.wav'

class Sound:
    @staticmethod
    def play(sound_file: str):
        def sound_thread():
            playsound(sound_file)
        threading.Thread(target=sound_thread).start()
    
    @staticmethod
    def stop():
        print("Stopping sound")
    
    @staticmethod
    def loop(num_of_times: float):
        print("Looping sound")
    
    