
import pyautogui as pyg 
import keyboard as kbd 
import time

string = input("Enter Here What you want to spammm... : \n")
for i in range(3,1):
    print(i)

def spammingBot(string) :
    while(True) :
        if(kbd.is_pressed('q')):
            break
        pyg.typewrite(string)
        pyg.press("enter")
        time.sleep(2)