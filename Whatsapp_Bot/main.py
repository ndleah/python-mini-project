import pywhatkit
from datetime import datetime

PHONE_NUMBER = input("Enter Phone Number: ")
MESSAGE = input("Enter Message: ")
HR = int(input("Enter Hour: "))     # 24 Hour Format
MIN = int(input("Enter Minutes:"))

pywhatkit.sendwhatmsg(PHONE_NUMBER, MESSAGE, HR, MIN)
