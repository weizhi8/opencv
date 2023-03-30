import cv2
import math


def Bubbl(r):
    for i in range(1,len(r)):
        for j in range(0, len(r) - i):
            if r[j][0] > r[j + 1][0]:
                r[j], r[j + 1] = r[j + 1], r[j]
            elif r[j][0] == r[j + 1][0]:
                if r[j][1] > r[j + 1][1]:
                    r[j], r[j+1] = r[j + 1], r[j]
    return r


def getContours(img):
    imgG = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgG, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 100, 100)
    img2 = img.copy()
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
                finalCountours.append([len(appprox), area, appprox, bbox, i])
            else:
                finalCountours.append([len(appprox), area, appprox, bbox, i])
    # 对第二个数值面积进行排序，为升序，找出轮廓的最大值
    finalCountours = sorted(finalCountours, key=lambda x: x[1], reverse=True)
    for con in finalCountours:
        cv2.drawContours(img, con[4], -1, (0, 0, 255), 4)
    return img, finalCountours, img2


def angle_between_points(p1, p2, p3):
    """
    测量三个点之间的角度
    p1, p2, p3: 三个点坐标，例如 [x1, y1], [x2, y2], [x3, y3]
    返回角度大小，以弧度为单位
    """
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    # 计算两条向量
    vector1 = [x1 - x2, y1 - y2]
    vector2 = [x3 - x2, y3 - y2]
    # 计算两个向量的长度
    length1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
    length2 = math.sqrt(vector2[0]**2 + vector2[1]**2)
    # 计算向量的点积
    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
    # 计算cos值
    cos_value = dot_product / (length1 * length2)
    # 计算弧度角
    radian_angle = math.acos(cos_value)
    # 将弧度角转换为角度
    degree_angle = math.degrees(radian_angle)
    return degree_angle


def angle(img):
    img , cons1, img2 = getContours(img)
    for i in cons1:
        jud = int(len(i[2]))
        jud1 = int((jud / 2) -2)
        List = []
        for i1 in i[2]:
            for j in i1:
                a = int(j[0])
                a2 = int(j[1])
                j1 = [a,a2]
                List.append(j1)
        jud2 = 0
        Bubbl(List)
        while jud2 ==0:
            if jud1 > 0:
                ListXY = []
                i1 = 0
                jud3 = int((len(List)) / 2)
                for i in range(jud3):
                    if List[i1][1] > List[i1+1][1]:
                        ListXY.append(List[i1+1])
                    else:
                        ListXY.append(List[i1])
                    i1 = i1 + 2
                u1 = 0
                for u in range(jud1):
                    pt1 = ListXY[u1]
                    pt2 = ListXY[u1 +1]
                    pt3 = ListXY[u1 + 2]
                    cc = angle_between_points(pt1,pt2,pt3)
                    cc = round(cc, 2)
                    cv2.putText(img, str(cc), (pt1[0] - 20, pt1[1] - 20), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 1)
                    u1 = u1 + 1
            jud2 = 4
    cv2.imshow('img2', img)
    cv2.waitKey(0)


if __name__ == '__main__':
    minArea = 200   # 最小检测物体的面积
    filter = 6
    img = cv2.imread(r'D:\1\tp\7.jpg')
    img = cv2.resize(img, (0, 0), None, 0.5, 0.5)
    angle(img)

