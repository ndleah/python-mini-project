#importin the packages
import cv2
import pyautogui
import numpy as np

#Set the parameters
screen_width, screen_height = pyautogui.size()
resolution = (screen_width, screen_height)
fps = 30
rec_time = 5;
opname = "Sample.mp4"

#Initialise parameters for the VideoWriter class 
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(opname, fourcc, fps, resolution)

#Extract the frames and display them at the specified rate
for _ in range(int(rec_time* fps)):
    x = pyautogui.screenshot()
    frame = np.array(x)
    frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
    out.write(frame)

End the Screen recording and save the video
out.release();
