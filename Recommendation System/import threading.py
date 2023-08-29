import threading 
import time
class multithreading(threading.Thread):
    def __init__(self,name,delay):
        threading.Thread.__init__(self)
        self.x = name
        self.y = delay
    def run(self):
        for i in range(5):
            print(i,end="")
            print(self.x)
            time.sleep(self.y)
x = multithreading("aravind",3)
x.start()