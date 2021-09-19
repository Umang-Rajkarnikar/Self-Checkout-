import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import pyautogui

CAM_HEIGHT = 720
CAM_WIDTH = 1280

cap = cv2.VideoCapture(0)
cap.set(3, CAM_WIDTH)
cap.set(4, CAM_HEIGHT)
detector = HandDetector(maxHands=1, detectionCon=0.8)


# PAGES
pagesDict = {
    "start": {
        "start": (0, 0, CAM_WIDTH, CAM_HEIGHT)
    },
    "checkout": {
        "remove": (1000, 50, 1175, 200),
        "loyalty": (800, 225, 975, 375),
        "help": (1000, 225, 1175, 375),
        "pay": (800, 425, 1175, 675),
        "code": (800, 50, 975, 200)
    },
    "pay": {
        "credit": (900, 100, 1150, 250),
        "debit": (900, 300, 1150, 450),
        "cancel": (900, 500, 1150, 650)
    },
    "help": {
        "Help is on the way": (100, 50, 'not a button', False),
        "cancel": (900, 500, 1150, 650)
    },
    "remove": {
        "Please scan the item you would like to remove": (50, 50, 'not a button', False),
        "cancel": (900, 500, 1150, 650)
    },
    "loyalty": {
        "Please scan your loyalty card": (100, 50, 'not a button', False),
        "cancel": (900, 500, 1150, 650)
    },
    "code": {
        "1": (80, 100, 280, 250),
        "2": (400, 100, 600, 250),
        "3": (720, 100, 920, 250),
        "enter": (1020, 100, 1220, 250),
        "4": (80, 300, 280, 450),
        "5": (400, 300, 600, 450),
        "6": (720, 300, 920, 450),
        "back": (1020, 300, 1220, 450),
        "7": (80, 500, 280, 650),
        "8": (400, 500, 600, 650),
        "9": (720, 500, 920, 650),
        "0": (1020, 500, 1220, 650)

    }
}
pageNum = 0
pages = []
pressed = False
bkey = None

class Page():
    def __init__(self, name, buttons):
        self.name = name
        self.buttons = buttons

    def update(self, cursor, pageNum, pressed, bkey):

        # if on start page, move to checkout page
        if not pageNum:
            pressed = False
            bkey = None
            return 1, pressed, bkey

        # if a button has been pressed, check for release
        elif pressed:
            release_length, release_info, release_img = detector.findDistance(lmList[8], lmList[12], img)
            # if button has been released, 
            if release_length > 60:
                print(bkey)
                if bkey == "pay":
                    pyautogui.click(x=140, y=590)
                    pageNum = 2
                elif bkey == "help":
                    pyautogui.click(x=140, y=490)
                    pageNum = 3
                elif bkey == "remove":
                    pyautogui.click(x=140, y=380)
                    pageNum = 4
                elif bkey == "loyalty":
                    pyautogui.click(x=140, y=200)
                    pageNum = 5
                elif bkey == "code":
                    pyautogui.click(x=140, y=270)
                    pageNum = 6
                else:
                    pageNum = 1
                    if bkey == "cancel":
                        pyautogui.click(x=940, y=58)

                pressed = False
                bkey = None
                return pageNum, pressed, bkey

        # check each button to see if it has been pressed
        for name in self.buttons:
            x1, y1, x2, y2 = self.buttons[name]
            # only consider buttons for updating pages
            if x2 != 'not a button':
                # if button has been pressed, turn it green, save the button name and set button pressed status to true
                if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)
                    bkey = name
                    pressed = True
                    
        return pageNum, pressed, bkey



for key in pagesDict:
    pages.append(Page(key, pagesDict[key]))

while cap.isOpened:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    page = pages[pageNum]

    for key in page.buttons:
        x1, y1, x2, y2 = page.buttons[key]
        # behaviour for buttons (in blue)
        if x2 != 'not a button':
            img = cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), -1)
            img = cv2.putText(img, key, ((x1 + x2) // 2 - 50, (y1 + y2) // 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                              2)
        else:
            # behaviour for text boxes with information (in magenta)
            cvzone.putTextRect(img, key, [x1, y1], 3, 4)

    if hands:
        lmList = hands[0]['lmList']
        cursor = lmList[8]

        # Palm Gesture to Start Checkout
        if pageNum == 0:
            pairs = [(5, 8), (9, 12), (13, 16), (17, 20), (1, 4), (0, 9)]
            lengths = []
            for pair in pairs:
                length, info, img = detector.findDistance(lmList[pair[0]], lmList[pair[1]], img)
                lengths.append(length)

            if all(length>100 for length in lengths):
                pageNum, pressed, bkey = page.update(cursor, pageNum, pressed, bkey)
                pyautogui.click(x=950, y=50)

        # Click Gesture
        else:
            length, info, img = detector.findDistance(lmList[8], lmList[12], img)
            if length < 60:
                pageNum, pressed, bkey = page.update(cursor, pageNum, pressed, bkey)
            elif pressed:
                pageNum, pressed, bkey = page.update(cursor, pageNum, pressed, bkey)

    cv2.imshow("Img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
