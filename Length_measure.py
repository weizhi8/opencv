#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023年3月29号
# @Author  : LJC
# @E-mail  : 2275716724@qq.com

import cv2
import numpy as np


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


def findDis(pts1, pts2):
    return ((pts2[0] - pts1[0]) ** 2 + (pts2[1] - pts1[1]) ** 2) ** 0.5


def coordinate(cons, img):
    for i in cons:
        List = []
        for i1 in i[2]:
            List.append([i1[0][0], i1[0][1]])
        Bubbl(List)
        seat = int(len(List)-2)
        cv2.arrowedLine(img, List[0], List[1],
                        (255, 0, 255), 2, 8, 0, 0.05)
        cv2.arrowedLine(img, List[seat], List[seat+1],
                        (255, 0, 255), 2, 8, 0, 0.05)
    cv2.imshow('img2', img)


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
        for i in cons3:
            List = []
            for i1 in i[2]:
                List.append([i1[0][0], i1[0][1]])
            Bubbl(List)
            seat = int(len(List) - 2)
            cv2.arrowedLine(img2,List[0], List[1],(255, 0, 255), 2, 8, 0, 0.05)
            cv2.arrowedLine(img2, List[seat], List[seat + 1],(255, 0, 255), 2, 8, 0, 0.05)
            xscd = findDis(List[0],List[1])
            CD = xscd / a
            CD = round(CD,1)
            x, y, w, h = i[3]
            cv2.putText(img2, '{}cm'.format(CD), (x + w, y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                        (255, 0, 255), 1)
            xscd1 = findDis(List[seat], List[seat+1])
            CD1 = xscd1 /a
            CD1 =round(CD1,1)
            cv2.putText(img2, '{}cm'.format(CD1), (x , y + h // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                        (255, 0, 255), 1)
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
    img = cv2.imread(r'D:\1\tp\7.jpg')
    img = cv2.resize(img, (0, 0), None, 0.5, 0.5)
    findDis1(img,W=50,H=50)


