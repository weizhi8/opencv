import cv2
import numpy as np


def Bubbl1(r):
    for i in range(1,len(r)):
        for j in range(0, len(r) - i):
            if r[j][1] > r[j + 1][1]:
                # print(r[j][0])
                r[j], r[j + 1] = r[j + 1], r[j]
            elif r[j][1] == r[j][1]:
                if r[j][0] > r[j + 1][0]:
                    r[j], r[j+1] = r[j + 1], r[j]

    return r


def Bubbl(r):
    for i in range(1,len(r)):
        for j in range(0, len(r) - i):
            if r[j][0] > r[j + 1][0]:
                # print(r[j][0])
                r[j], r[j + 1] = r[j + 1], r[j]
            elif r[j][0] == r[j + 1][0]:
                if r[j][1] > r[j + 1][1]:
                    r[j], r[j+1] = r[j + 1], r[j]

    return r


def findDis1(img, W, H):
    imgcon3, cons3, img2 = getContours(img)
    if len(cons3) != 0:
        List = []
        for i in cons3:
            # print(i[1])
            List.append(i[1])
        Min = min(List)
        Min = int(Min)
        inde = List.index(Min)
        nPoints = reorder(cons3[inde][2])
        xw = nPoints[1][0][0] - nPoints[0][0][0]
        xh = nPoints[2][0][1] - nPoints[0][0][1]
        a = xw / W
        a1 = xh / H
        Listcache1 = []

        for i in cons3:
            Listcache1.append(i[1])
        seat = Listcache1.index(min(Listcache1))


        for i1,i in enumerate(cons3):
            Listcache = []
            coordinate = []
            if seat == i1:
                pass
            else:
                for i3 in i[4]:
                    Listcache.append([i3[0][0],i3[0][1]])
                    Bubbl(Listcache)
                coordinate.append(Listcache[0])
                coordinate.append(Listcache[len(Listcache)-1])
                Bubbl1(Listcache)
                coordinate.append(Listcache[0])
                coordinate.append(Listcache[len(Listcache) - 1])
                Rx = (coordinate[0][0] - coordinate[1][0]) / 2
                Rx = abs(Rx)
                Ry = (coordinate[2][1] - coordinate[3][1]) / 2
                Ry = abs(Ry)
                Listcache4 = [coordinate[0][0],coordinate[1][0]]
                x = max(Listcache4) - Rx
                Listcache4 = [coordinate[2][1],coordinate[3][1]]
                y = max(Listcache4) - Ry
                # print(x,y)
                # print('++')
                print([x,y])
                cv2.arrowedLine(img2, [int(x),int(y)],[int(x),int(y+Ry)], (255, 0, 255), 2, 8, 0, 0.05)
                x, y, w, h = i[3]
                CD = Ry / a
                CD = round(CD, 1)
                cv2.putText(img2, '{}cm'.format(CD), (x + w, y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,(255, 0, 255), 1)
        cv2.imshow('img2', img2)
        cv2.waitKey(0)

def reorder(myPoints):
    myPointsNew = np.zeros_like(myPoints)
    myPoints = myPoints.reshape((4, 2))
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    return myPointsNew


def getContours(img):
    imgG = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgG, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 100, 100)
    img2 = img.copy()
    kernel = np.ones((5, 5))
    contours, hiearchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    finalCountours = []
    for i in contours:
        area = cv2.contourArea(i)
        if area > minArea:
            # 计算轮廓的周长，true表示轮廓为封闭
            peri = cv2.arcLength(i, True)
            appprox = cv2.approxPolyDP(i, 0.02 * peri, True)
            bbox = cv2.boundingRect(appprox)
            if filter > 0:
                # if (len(appprox)) == filter:
                finalCountours.append([len(appprox), area, appprox, bbox, i])
            else:
                finalCountours.append([len(appprox), area, appprox, bbox, i])
    # 对第二个数值面积进行排序，为升序，找出轮廓的最大值
    finalCountours = sorted(finalCountours, key=lambda x: x[1], reverse=True)
    for con in finalCountours:
        cv2.drawContours(img, con[4], -1, (0, 0, 255), 4)
    return img, finalCountours, img2


if __name__ == '__main__':
    minArea = 200
    filter = 6
    img = cv2.imread(r'D:\1\tp\1.jpg')
    img = cv2.resize(img, (0, 0), None, 0.5, 0.5)
    findDis1(img,W=50,H=50)


