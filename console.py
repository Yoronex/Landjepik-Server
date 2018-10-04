import threading
import time


class Console(threading.Thread):
    app = None

    def __init__(self):
        print("Console started")
        while(True):
            self.readinput()

    def setcallback(self, app):
        self.app = app

    def listener(self):
        string = input("Hello! What is your name?")
        print(string)

    def readinput(self):
        while True:
            x = input("Type iets: ")
            print(x)
