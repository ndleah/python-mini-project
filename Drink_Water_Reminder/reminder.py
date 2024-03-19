# It is water drinking notification remainder program. It will notify
# you to drink water after one hour by using notification panel of your operating system.

# import
import time
from plyer import notification

if __name__ == "__main__":
    while True:
        notification.notify(title='Drink Water Now!!!',
                            message="Your body is composed of about 60% water. The functions of these bodily fluids include digestion, absorption, circulation, creation of saliva, transportation of nutrients, and maintenance of body temperature.",
                            # app_icon="your_notification_icon_image.ico",
                            timeout=10)
        time.sleep(60*60)
# Finish