import imutils
import cv2
import numpy as np


# define the lower and upper boundaries of the colors in the HSV color space
lower = {'red': (166, 84, 141), 'green': (66, 20, 20), 'blue': (97, 100, 117), 'yellow': (23, 59, 119),
         'orange': (20, 50, 80)}  # assign new item lower['blue'] = (93, 10, 0)
upper = {'red': (186, 255, 255), 'green': (86, 255, 255), 'blue': (117, 255, 255), 'yellow': (54, 255, 255),
         'orange': (23, 255, 255)}

# define standard colors for circle around the object
colors = {'red': (0, 0, 255), 'green': (0, 255, 0), 'blue': (255, 0, 0), 'yellow': (0, 255, 217),
          'orange': (0, 140, 255)}
# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('http://172.20.10.13:8000/stream.mjpg')
while True:
    # grab the current frame
    ret, frame = cap.read()
    if not ret:
        print('cant get the stream!')
        break
    # resize the frame, blur it, and convert it to the HSV color space
    frame = imutils.resize(frame, width=600, height=450)
    frame_center_x = 300
    frame_center_y = 225
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    # for each color in dictionary check object in frame
    for key, value in upper.items():
        # construct a mask for the color from dictionary`1, then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        kernel = np.ones((9, 9), np.uint8)
        mask = cv2.inRange(hsv, lower[key], upper[key])
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the radius meets a minimum size. Correct this value for your obect's size
            if radius > 2:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius), colors[key], 2)
                cv2.putText(frame, key + " ball", (int(x - radius), int(y - radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                            colors[key], 2)
                if key == 'yellow':# or key == 'green':
                    yellow_x = int(x)
                    yellow_y = int(y)
                    cv2.arrowedLine(frame, (frame_center_x, frame_center_y),(yellow_x,yellow_y),(255,0,0), 5, 0, 0, .2)
                    diff_x = yellow_x - frame_center_x
                    diff_y = yellow_y - frame_center_y
                    if diff_x > 30:
                        print('Go Right')
                    if diff_x < -30:
                        print('Go Left')
                    if abs(diff_x) < 30:
                        print('On Target!')

    # show the frame to our screen
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
cv2.destroyAllWindows()