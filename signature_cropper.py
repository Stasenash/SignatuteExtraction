import cv2
import matplotlib.pyplot as plt
from skimage import measure, morphology
from skimage.color import label2rgb
from skimage.measure import regionprops
import numpy as np

delta = 19


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Area:
    def __init__(self, topLeft):
        self.topLeft = topLeft
        self.bottomRight = topLeft
        self.tlPoint = topLeft
        self.brPoint = topLeft

    def changeRightAndLeft(self, point):
        self.bottomRight = point
        brX = point.x if self.brPoint.x < point.x else self.brPoint.x
        brY = point.y if self.brPoint.y < point.y else self.brPoint.y
        tlX = point.x if self.tlPoint.x > point.x else self.tlPoint.x
        tlY = point.y if self.tlPoint.y > point.y else self.tlPoint.y
        self.brPoint = Point(brX, brY)
        self.tlPoint = Point(tlX, tlY)

    def isInArea(self, point):
        flag = False

        minX = min(self.topLeft.x, self.bottomRight.x)
        maxX = max(self.topLeft.x, self.bottomRight.x)
        minY = min(self.topLeft.y, self.bottomRight.y)
        maxY = max(self.topLeft.y, self.bottomRight.y)
        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                if abs(point.x - x) < delta or abs(point.y - y) < delta:
                    flag = True
                    break

        return flag

    def print(self, areaIndex: int = None):
        if areaIndex == None:
            print("area: [" + str(area.topLeft.x) + ", " + str(area.topLeft.y) + "] [" +
                  str(area.bottomRight.x) + ", " + str(area.bottomRight.y) + "]")
        else:
            print("area #" + str(areaIndex) + ": [" + str(area.topLeft.x) + ", " + str(area.topLeft.y) + "] [" +
                  str(area.bottomRight.x) + ", " + str(area.bottomRight.y) + "]")


def getAreaIndex(areaList, point):
    for area in areaList:
        if area.isInArea(point):
            return areaList.index(area)

    return -1


img = cv2.imread('./inputs/in5.png', 0)

# список всех областей с подписями
list = []

currentAreaIndex = -1  # индекс области, в которой мы находимся в данный момент
for y in range(img.shape[0]):
    for x in range(img.shape[1]):
        point = Point(x, y)
        # если нашли черный цвет
        if img[y][x] == 0:
            # проверяем не войдет ли данная точка в уже найденные области
            index = getAreaIndex(list, point)

            if index == -1:
                # если нет, то это новая область
                list.append(Area(point))  # добавляем в список новую область
                currentAreaIndex = len(list)
            else:
                # если входит в какую-то область, то обновляем у нее правую нижнюю точку
                list[index].changeRightAndLeft(point)

print("found " + str(len(list)) + " areas")
for area in list:
    area.print(list.index(area))
    # old_img = cv2.imread('./inputs/in3.jpg', 0)
    croppedArea = img[area.tlPoint.y - 50:area.brPoint.y + 50, area.tlPoint.x - 50:area.brPoint.x + 50]
    cv2.imwrite('area'+str(list.index(area))+'.png', croppedArea)
    img = cv2.rectangle(img, (area.tlPoint.x, area.tlPoint.y),
                        (area.brPoint.x, area.brPoint.y),
                        (127, 127, 127),
                        1)

cv2.imwrite('ch5.png', img)
