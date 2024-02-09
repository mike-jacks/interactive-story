from time import sleep
import threading
from playsound import playsound

class Sound:
    @staticmethod
    def play():
        print("Playing sound")
    
    @staticmethod
    def stop():
        print("Stopping sound")
    
    @staticmethod
    def loop(num_of_times: float):
        print("Looping sound")
    