import cv2
import matplotlib.pyplot as plt
from skimage import measure, morphology
from skimage.color import label2rgb
from skimage.measure import regionprops
import numpy as np

delta = 20


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Area:
    def __init__(self, topLeft):
        self.topLeft = topLeft
        self.bottomRight = topLeft

    def changeBottomRight(self, bottomRight):
        self.bottomRight = bottomRight

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


img = cv2.imread('./inputs/in4.png', 0)

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
                list[index].changeBottomRight(point)

print("found " + str(len(list)) + " areas")
for area in list:
    area.print(list.index(area))
    img = cv2.rectangle(img, (area.topLeft.x, area.topLeft.y),
                        (area.bottomRight.x, area.bottomRight.y),
                        (127, 127, 127),
                        1)

    # minX = min(area.topLeft.x, area.bottomRight.x)
    # maxX = max(area.topLeft.x, area.bottomRight.x)
    # minY = min(area.bottomRight.y, area.topLeft.y)
    # maxY = max(area.bottomRight.y, area.topLeft.y)
    # croppedArea = img[minX:maxX, minY:maxY]
    # cv2.imwrite('area'+str(list.index(area))+'.png', croppedArea)
cv2.imwrite('ch2.png', img)
