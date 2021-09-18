import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone

CAM_HEIGHT = 720
CAM_WIDTH = 1280

cap = cv2.VideoCapture(0)
cap.set(3,CAM_WIDTH)
cap.set(4,CAM_HEIGHT)
detector = HandDetector(detectionCon=0.8)

        
class Page():
    def __init__(self,name,buttons):
        self.name = name
        self.buttons = buttons

    def update(self,cursor,pageNum):
        for key in self.buttons:
            x1,y1,x2,y2 = self.buttons[key]
            #only consider buttons for updating pages
            if x2 != 'not a button':
                if x1<cursor[0]<x2 and y1<cursor[1]<y2:
                    cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),cv2.FILLED)
                    if key == "pay":
                        return 1
                    elif key == "help":
                        return 2
                    elif key == "remove":
                        return 3
                    elif key == "loyalty":
                        return 4
                    else:
                        return 0
        else:
            return pageNum


# PAGES
pagesDict = {
    "checkout":{
        "code":(800,50,975,200),
        "remove":(1000,50,1175,200),
        "loyalty":(800,225,975,375),
        "help":(1000,225,1175,375),
        "pay":(800,425,1175,675)
    },
    "pay":{
        "credit":(900,100,1150,250),
        "debit":(900,300,1150,450),
        "cancel":(130,500,430,650)
    },
    "help":{
        "Help is on the way":(100,50, 'not a button', False),
        "cancel":(130,500,430,650)
    },
    "remove":{
        "Please scan the item you would like to remove":(100,50, 'not a button', False),
        "cancel":(130,500,430,650)
    },
    "loyalty":{
        "Please scan your loyalty card":(100, 50, 'not a button', False),
        "cancel":(130,500,430,650)
    }   
}
pageNum = 0
pages = []
for key in pagesDict:
    pages.append(Page(key,pagesDict[key]))


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    page = pages[pageNum]

    for key in page.buttons:
        x1, y1, x2, y2 = page.buttons[key]
        #behaviour for buttons (in blue)
        if x2 != 'not a button':
            img = cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), -1)
            img = cv2.putText(img, key, ((x1+x2)//2-50, (y1+y2)//2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            #behaviour for text boxes with information (in magenta)
            cvzone.putTextRect(img, key, [x1, y1], 3, 4)

    
    if hands:
        lmList = hands[0]['lmList']
        cursor = lmList[8]
        length, info, img = detector.findDistance(lmList[8], lmList[12], img)
        if length < 60:
            pageNum = page.update(cursor, pageNum)
        

    cv2.imshow("Img", img)
    if cv2.waitKey(1) == ord('q'):
        break
