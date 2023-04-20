import cv2

IMAGE = cv2.imread('shape.jpg');
GREYSCALE = cv2.cvtColor(IMAGE, cv2.COLOR_BGR2GRAY)
h, w, channels = IMAGE.shape

PARAM, PARAM2 = cv2.threshold(GREYSCALE, 50, 255, 0)

CONTOURS, _ = cv2.findContours(PARAM2, 1, 1)

RECTANGLES = 0;
SQUARES = 0;

for cnt in CONTOURS:
   x1,y1 = cnt[0][0]
   approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
   if len(approx) == 4:
      x, y, w, h = cv2.boundingRect(cnt)
      ratio = float(w)/h
      if ratio >= 0.9 and ratio <= 1.1:
         IMAGE = cv2.drawContours(IMAGE, [cnt], -1, (0,255,0), 3)
         SQUARES = SQUARES + 1
      else:
         IMAGE = cv2.drawContours(IMAGE, [cnt], -1, (0,255,0), 3)
         RECTANGLES = RECTANGLES + 1

cv2.putText(IMAGE, 'Number of SQUARES: ' + str(SQUARES), (h+500, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
cv2.putText(IMAGE, 'Number of RECTANGLES: ' + str(RECTANGLES), (h+500, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

cv2.imshow("Shapes", IMAGE)
cv2.waitKey(0)
cv2.destroyAllWindows()