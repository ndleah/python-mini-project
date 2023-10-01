import cv2
import time
print("Press Space-bar to click Selfie")
print("Press Escape key to terminate the window")
time.sleep(5)
cam = cv2.VideoCapture(0)
cv2.namedWindow("Take selfie with python")
img=0
while True:
    ret, frame = cam.read()

    if not ret:
        print("Failed to grab frame") 
        break

    cv2.imshow("Take selfie with python",frame)
    k = cv2.waitKey(1)
    if k%256 == 27:
        print("Escape hit, closing the window")
        break
    if k%256 == 32:
        img_name = f"Selfie_{img}.jpg"
        cv2.imwrite(img_name,frame)
        print("Selfie taken!")
        img+=1
cam.release
cv2.destroyAllWindows()
