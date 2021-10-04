"""
PROJECT NAME: AI Virtual Keyboard using OpenCV
SUBJECT: Digital Signal & Image Processing
MEMBERS:
    1) Irfan Shaikh (44)
    2) Prateek Sharma (47)
    3) Saurav Kumar (23)

"""

import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller, Key
from time import sleep
import cvzone
# cvzone is a computer vision package that makes its easy to run Image processing and AI functions.
# At the core it uses OpenCV and mediapipe libraries.


# creating a video capture object & giving id 0 for webcam
cap = cv2.VideoCapture(0)

# using hd resolution by setting propId for width 3 and height 4
cap.set(3, 1280)
cap.set(4, 720)


# for higher accuracy giving detection confidence 0.8 cause we don't want to randomly press any key
detector = HandDetector(detectionCon=0.8)
keys = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
]
finalText = ""
keyboard = Controller()


"""
Function to draw all buttons on the screen,

We are having a separate function to draw btn because we want to draw buttons each time 
frame changes so we have to draw again and again as we are using a webcam.

"""
def drawALL(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                          20, rt=0)

        # creating btns using opencv methods
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    # returning the most recent frame
    return img


# Button generator class
class Button:
    # we want to initialize the attributes (position, text) only once cause
    # there are not gonna change and should run only once
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []
for i in range(len(keys)):
    # enumerating to get the key as well as the counter value
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    # landmarklist and boundingboxinfo
    lmList, bboxInfo = detector.findPosition(img)
    img = drawALL(img, buttonList)

    # checking if hand is being detected or not
    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            # checking if the index finger is in the range of keyboard or not
            if x < lmList[8][0] < x+w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                l, _, _ = detector.findDistance(8, 12, img)
                print(l)

                # clear character
                # a, _, _ = detector.findDistance(4, 16, img)
                # print("backscape", a)
                #
                # if a < 20:
                #     keyboard.press(Key.backspace)
                #     sleep(0.15)

                # add space
                # f, _, _ = detector.findDistance(4, 20, img)
                # print(f)
                #
                # if f < 20:
                #     keyboard.press(Key.space)
                #     sleep(0.15)

                # when clicked
                if l < 30:
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    finalText += button.text
                    sleep(0.4)

    # displaying output
    cv2.rectangle(img, (50, 350), (900, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 425), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("Virtual Keyboard", img)
    cv2.waitKey(1)
