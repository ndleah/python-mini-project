import cv2,time
from os import mkdir
import objc
import AppKit

# Create folder to save video footage
try:
    mkdir('footages')
except FileExistsError:
    pass

# Method to add minimize feature
def minimizeWindow():  
    objc.python_method(AppKit.NSRunningApplication.currentApplication().hide_)
    AppKit.NSRunningApplication.currentApplication().hide_(None)

# Video Camera
def cctv():
    video = cv2.VideoCapture(0)
    #Set new resolution of camera
    #video.set(cv2.CAP_PROP_FRAME_WIDTH,320)
    #video.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
    video.set(3,640)
    video.set(4,480)
    width = video.get(3)
    height = video.get(4)
    print("Video resolution is set to: ",width,'X',height)
    print("--Help:  1. press esc key to exit cctv\n2. press m to minimize window.")
   
    # Set video output
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    date_time = time.strftime("recording %H-%M -%d %m %y")#set current time as video name
    output = cv2.VideoWriter('footages/'+date_time+'.mp4',fourcc,20.0,(640,480))
   
    # Start recording
    while video.isOpened():
        check,frame = video.read()
        if check == True:
            frame = cv2.flip(frame,1)
            
            
            # Show time of recording 
            #t= time.strftime("%H:%M:%S   %d %m %y")
            t = time.ctime()
            cv2.rectangle(frame,(5,5,100,20),(255,255,255),cv2.FILLED)
            cv2.putText(frame,"Camera 1",(20,20),
                        cv2.FONT_HERSHEY_DUPLEX,0.5,(5,5,5),2)
            cv2.putText(frame,t,(420,460),
                        cv2.FONT_HERSHEY_DUPLEX,0.5,(5,5,5),1)
            
            
            cv2.imshow('CCTV camera',frame)
            output.write(frame)
            
            # Close window when user click esc button
            if cv2.waitKey(1) ==27:
                print("Video footage saved in current directory.\n Be safe & Secure")
                break

            # Call minimizeWindow method when user press m
            elif cv2.waitKey(1) ==ord('m'):
                minimizeWindow()
        else:
            print("Can't open this camera. select other or check its configuration.")
            break
    video.release()
    output.release()
    cv2.destroyAllWindows()

# Run the app
print("*"*80+"\n"+" "*30+"Welcome to ReconEye\n"+"*"*80)
ask = int(input('Do you want to Start cctv ?\n1. Yes\n2. No\n>>> '))
if ask ==1:
    cctv()
elif ask ==2:
    print("Be safe & secure!")
    exit