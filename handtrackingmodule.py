import cv2
import mediapipe as mp
import time
import math


class handDetector():
    def __init__(self, mode=False,maxHands=2,detectioncon=0.5,trackcon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectioncon=detectioncon
        self.trackcon=trackcon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.detectioncon,self.trackcon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds =[4, 8, 12, 16, 20]






    def findHand(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(imgRGB)


        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handlms, self.mpHands.HAND_CONNECTIONS)



        return img

    def findposition(self,img,handno=0,draw=True):
        xlist=[]
        ylist=[]
        bbox=[]

        self.lmList = []
        if self.results.multi_hand_landmarks:
            myhand=self.results.multi_hand_landmarks[handno]
            for id, lm in enumerate(myhand.landmark):

                    # print(id,lm)
                     h, w, c = img.shape
                     cx, cy = int(lm.x * w), int(lm.y * h)
                     #print(cx,cy)
                     xlist.append(cx)
                     ylist.append(cy)

                     #print(id, cx, cy)
                     self.lmList.append([id, cx, cy])
                     if draw:
                         cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            # xmin,xmax=min(xlist),max(xlist)
            # ymin,ymax=min(ylist),max(ylist)
            # bbox = xmin,ymin,xmax,ymax

            # if draw:
            #         cv2.rectangle(img, (bbox[0]-20, bbox[1]-20),
            #                       (bbox[2]+20, bbox[3]+20), (0, 255, 0), 2)
        return self.lmList#,bbox

    # def findDistance(self,p1,p2,img,draw=True):
    #     x1, y1 = self.lmList[p1][1], self.lmList[p1][2]
    #     x2, y2 = self.lmList[p2][1], self.lmList[p2][2]
    #     cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    #
    #     if draw:
    #
    #         cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
    #         cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
    #
    #         cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
    #
    #         cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
    #     length = math.hypot(x2 - x1, y2 - y1)
    #     return length,img,[x1,y1,x2,y2,cx,cy]

    def fingresup(self):
        fingres=[]
        #thumb
        if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0]-1][1]:
            fingres.append(1)
        else:
            fingres.append(0)

        for id in range(1,5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingres.append(1)
            else:
                fingres.append(0)
        return fingres






def main():
        pTime = 0
        cTime = 0
        cap = cv2.VideoCapture(0)
        detector=handDetector()

        while True:
            success, img = cap.read()
            #img=detector.findHand(img)
            img=detector.findHand(img)
            lmList=detector.findposition(img)
            if len(lmList)!=0:
                print(lmList[4])

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

            cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 8, 255), 3)

            cv2.imshow("image", img)
            cv2.waitKey(1)


if __name__ == "__main__":
    main()