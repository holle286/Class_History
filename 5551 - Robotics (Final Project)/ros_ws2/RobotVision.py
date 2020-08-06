import cv2 #install this    ~ pip install opencv-python
import numpy as np
import statistics # install this ~ pip install statistics `
import math
import random
import Queue

filters = { "pink": [np.array([5, 60, 0]), np.array([10, 80, 255])], "black": [np.array([0, 0, 0]), np.array([255, 255, 25])],
            "lightblue": [np.array([85, 60, 0]), np.array([95, 100, 255])], "dark_red": [np.array([0, 162, 0]), np.array([5, 168, 255])],
            "yellowgreen": [np.array([30, 50, 0]), np.array([40, 65, 255])], "yellow": [np.array([20, 40, 0]), np.array([29, 49, 255])],
            "dark_dark_red": [np.array([0, 105, 0]), np.array([5, 120, 255])], "blue": [np.array([105, 88, 0]), np.array([115, 100, 255])],
            "teal": [np.array([92, 55, 0]), np.array([105, 70, 255])], "red": [np.array([0, 140, 0]), np.array([5, 160, 255])],
            "green": [np.array([75, 80, 0]), np.array([85, 115, 255])], "gold": [np.array([10, 40, 0]), np.array([30, 90, 255])]}

class SearchTool:
    def __init__(self, name):
        self.fileName = name
        self.image = cv2.imread(name)

    # returns a ((x, y), r)
    def findColor(self, color):
        # convert to hsv
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        print hsv[432, 671]
        #set which filter to use / default is black

        filter = filters["black"]
        if color in filters:
            filter = filters[color]

        #build mask
        mask = cv2.inRange(hsv, filter[0], filter[1])
        res = cv2.bitwise_and(self.image, self.image, mask=mask)
        cv2.imwrite(self.fileName[:-4] + '_mask.png', mask)
        mask = cv2.imread(self.fileName[:-4] + "_mask.png")

        #find unmasked white points
        height = mask.shape[0]
        width = mask.shape[1]
        whitePointsX = []
        whitePointsY = []

        for i in range(width):
            for j in range(height):
                # print mask[j, i]
                if mask[j, i][0] == 255:
                    whitePointsX += [i]
                    whitePointsY += [j]

        # calculate avg and std * 1.5
        avg_x = int(statistics.mean(whitePointsX))
        avg_y = int(statistics.mean(whitePointsY))

        isolatePoints = True
        radius = 0

        while isolatePoints:
            std_x = int(statistics.stdev(whitePointsX)*1.5)
            std_y = int(statistics.stdev(whitePointsY)*1.5)

            # remove points that are outliers
            for i in xrange(len(whitePointsX)-1, -1, -1):
                if whitePointsX[i] > std_x + avg_x or whitePointsX[i] < abs(std_x - avg_x) or whitePointsY[i] > std_y + avg_y or whitePointsY[i] < abs(std_y - avg_y):
                    mask[whitePointsY[i], whitePointsX[i]] = [0, 0, 0]
                    del whitePointsX[i]
                    del whitePointsY[i]

            # re-avg the points
            avg_x = int(statistics.mean(whitePointsX))
            avg_y = int(statistics.mean(whitePointsY))

            #find radius
            maxPoint = [avg_x, avg_y]

            for i in xrange(len(whitePointsX)):
                if math.sqrt((avg_x-whitePointsX[i]) ** 2 + (avg_y-whitePointsY[i]) ** 2) > math.sqrt((avg_x-maxPoint[0]) ** 2 + (avg_y-maxPoint[1]) ** 2):
                    maxPoint = [whitePointsX[i], whitePointsY[i]]

            radius = int(math.sqrt((avg_x-maxPoint[0]) ** 2 + (avg_y-maxPoint[1]) ** 2))

            area = math.pi * radius ** 2

            cv2.imwrite(self.fileName[:-4] + '_mask.png', mask)
            if((len(whitePointsX) / area > 0.20)):
                isolatePoints = False

        # show recognition in picture
        self.drawCircle(avg_x, avg_y, radius)

        cv2.imwrite(self.fileName[:-4] + "_recognition.png", self.image)
        self.refreshImage()
        return ((avg_x, avg_y), radius)


    # uses a DBscan clustering method to gather the centers of points
    def DBScan(self, color):
        self.refreshImage()
        # convert to hsv
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        # print hsv[432, 671]
        #set which filter to use / default is black

        filter = filters["black"]
        if color in filters:
            filter = filters[color]

        #build mask
        mask = cv2.inRange(hsv, filter[0], filter[1])
        res = cv2.bitwise_and(self.image, self.image, mask=mask)
        cv2.imwrite(self.fileName[:-4] + '_mask.png', mask)
        mask = cv2.imread(self.fileName[:-4] + "_mask.png")

        #find unmasked white points
        height = mask.shape[0]
        width = mask.shape[1]
        whitePoints = []

        for i in xrange(width):
            for j in xrange(height):
                # print mask[j, i]
                if mask[j, i][0] == 255:
                    whitePoints += [(i,j)]

        db = {}
        number_of_clusters = 0
        mindist = 2

        for i in xrange(0, len(whitePoints)):
            queue = Queue.Queue()
            if whitePoints[i] not in db.keys():
                # check points around it
                queue.put(whitePoints[i])

                while not queue.empty():
                    (cur_x, cur_y) = queue.get()

                    for circle_x in xrange(-mindist, mindist+1):
                        circle_y = int(math.sqrt(mindist ** 2 - circle_x ** 2) + 0.5)

                        for j in xrange(int(cur_y-circle_y), int(circle_y+cur_y+1)):
                            x_value = int(circle_x+cur_x)
                            if(j >= 0 and j < height and x_value < width and x_value >= 0):
                                if mask[j, x_value][0] == 255 and (x_value, j) not in db.keys():
                                    db[(x_value, j)] = number_of_clusters
                                    queue.put((x_value, j));

                number_of_clusters += 1

        clusters = [[] for i in range(number_of_clusters)]
        clusters_amount = [0] * number_of_clusters

        for i in xrange(0, len(whitePoints)):
            if whitePoints[i] in db.keys():
                clusters[db[whitePoints[i]]] += [whitePoints[i]]
                clusters_amount[db[whitePoints[i]]] += 1

        cutoff = int(max(clusters_amount)/2)

        # delete clusters that don't make the cutoff
        for i in xrange(number_of_clusters-1, -1, -1):
            if len(clusters[i]) < cutoff:
                for j in xrange(len(clusters[i])):
                    (x, y) = clusters[i][j]
                    mask[y, x] = [0, 0, 0]
                del clusters[i]

        # assemble the final results
        cluster_points = []

        for i in xrange(len(clusters)):

            x_points = []
            y_points = []
            for j in xrange(len(clusters[i])):
                (x, y) = clusters[i][j]
                x_points += [x]
                y_points += [y]

            # avg the points of the given cluster
            avg_x = int(statistics.mean(x_points))
            avg_y = int(statistics.mean(y_points))

            #find radius
            maxPoint = [avg_x, avg_y]

            for j in xrange(len(clusters[i])):
                if math.sqrt((avg_x-x_points[j]) ** 2 + (avg_y-y_points[j]) ** 2) > math.sqrt((avg_x-maxPoint[0]) ** 2 + (avg_y-maxPoint[1]) ** 2):
                    maxPoint = [x_points[j], y_points[j]]

            radius = int(math.sqrt((avg_x-maxPoint[0]) ** 2 + (avg_y-maxPoint[1]) ** 2))
            cluster_points += [((avg_x, avg_y), radius)]

            # draw recognition on new image
            self.drawCircle(avg_x, avg_y, radius)

        cv2.imwrite(self.fileName[:-4] + '_recognition.png', self.image)
        self.refreshImage()
        return cluster_points

    # Call everytime the image changes
    def refreshImage(self):
        self.image = cv2.imread(self.fileName)

    def drawCircle(self, avg_x, avg_y, radius):

        height = self.image.shape[0]
        width = self.image.shape[1]

        # draw recognition on new image
        self.image[avg_y, avg_x] = [0, 255, 30]

        # add circle around detected object
        for circle_x in xrange(0, radius+1):
            circle_y = int(math.sqrt(radius ** 2 - circle_x ** 2) + 0.5)
            if(int(circle_y+avg_y) < height and int(circle_x+avg_x) < width):
                self.image[int(circle_y+avg_y), int(circle_x+avg_x)] = [0, 255, 30]
            if(int(avg_y-circle_y) < height and int(circle_x+avg_x) < width):
                self.image[int(avg_y-circle_y), int(circle_x+avg_x)] = [0, 255, 30]
            if(int(circle_y+avg_y) < height and int(avg_x-circle_x) < width):
                self.image[int(circle_y+avg_y), int(avg_x-circle_x)] = [0, 255, 30]
            if(int(avg_y-circle_y) < height and int(avg_x-circle_x) < width):
                self.image[int(avg_y-circle_y), int(avg_x-circle_x)] = [0, 255, 30]

    def calculateAngle(self, (x1, y1), (x2, y2)):
        return np.arctan((y2-y1)/(x2-x1))

def main():
    searchTool = SearchTool("camera_img3.png")
    tealCoords = searchTool.DBScan("blue")
    print tealCoords
    # print searchTool.DBScan("red")
    # [((rx, ry), rr)] = searchTool.DBScan("red")

    # [((x1, y1), r1), ((x2, y2), r2), ((x3, y3), r3)] = tealCoords
    # print searchTool.calculateAngle((x1, y1), (rx, ry))s

    # print searchTool.findColor("red")
    # print searchTool.findColorPoints("teal", 3)



if __name__ == '__main__':
	main()
