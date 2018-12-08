import numpy as np
import cv2


def color_detection(found_face):
    hsv = cv2.cvtColor(found_face, cv2.COLOR_BGR2HSV)
    # define the color
    lower_blue = np.array([85, 50, 50])
    upper_blue = np.array([130, 255, 255])
    # create a mask for the color
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    # bitwise mask and image
    res_blue = cv2.bitwise_and(found_face, found_face, mask=mask_blue)
    cv2.imshow('blue', res_blue)
    return


face_cascade = cv2.CascadeClassifier(
    'C:\\Users\Stephen\PycharmProjects\LookingForPeopleInVideo\models\haarcascade_frontalface_default.xml')
body_cascade = cv2.CascadeClassifier(
    'C:\\Users\Stephen\PycharmProjects\LookingForPeopleInVideo\models\haarcascade_upperbody.xml')
if __name__ == '__main__':
    # cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture('http://172.20.10.13:8000/stream.mjpg')
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    center_x = int(size[0]/2)
    center_y = int(size[1]/2)

while 1:

    face_center_y = center_y
    face_center_x = center_x
    ret, frame = cap.read()
    # frame = cv2.resize(frame, (340, 220))
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    # faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    faces = face_cascade.detectMultiScale(gray)
    # bodies = body_cascade.detectMultiScale(gray)
    x, y, w, h = 0, 0, 0, 0
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        face_center_x = int(round(x + w // 2))
        face_center_y = int(round(y + h // 2))

    # crop_face = frame[y-50:y + h + 50, x-50:x + w + 20]
    # print(crop_face)

    # if faces is not ():
    #    color_detection(crop_face)
    #    hist = cv2.calcHist(crop_face, [0], None, [256], [0, 256])

    cv2.arrowedLine(frame, (center_x, center_y), (face_center_x, face_center_y), (0, 0, 255), 1, 4)
    cv2.imshow('Frame', frame)
    difference_x = center_x - face_center_x
    difference_y = center_y - face_center_y
    print('Difference from Center of image to Center of Detected Face')
    print('X: ', difference_x, 'Y: ', difference_y)
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # wait for ESC key to exit
        cv2.destroyAllWindows()
        break
