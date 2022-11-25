import cv2 as cv
import numpy as np
import math
import coordinates


class Puzzle:
    def __init__(self, contour):
        self.contour = contour
        self.approx_contour = cv.approxPolyDP(contour,5,True) #epsilon=5

        #corners
        self.p1=[0,0]
        self.p2=[0,0]
        self.p3=[0,0]
        self.p4=[0,0]
        self.area=0
        self.d1=0
        self.d2=0

    def find_corners(self):
        counter=0
        for i_index, i in enumerate(self.approx_contour):
            for j_index, j in enumerate(self.approx_contour):
                if (i==j).all():
                    continue
                new_d1=coordinates.distance(i[0],j[0])
                if new_d1<self.d1*0.9:
                    continue

                for k_index, k in enumerate(self.approx_contour):
                    if (k==i).all() or (k==j).all():
                        continue

                    for l_index, l in enumerate(self.approx_contour):
                        if (l==i).all() or (l==j).all() or (l==k).all():
                            continue
                        new_d2=coordinates.distance(k[0],l[0])

                        if new_d2<self.d2*0.9:
                            continue

                        if not coordinates.check_crosing(i[0], j[0], k[0], l[0]):
                            continue

                        if not coordinates.check_neighbor_contours(self.approx_contour, i_index, j_index, k_index, l_index):
                            continue

                        new_area = coordinates.calc_area(i[0], j[0], k[0], l[0])
                        if new_area > self.area and coordinates.check_angle(i[0], j[0], k[0], l[0]):
                            self.area = new_area
                            self.p1=i[0]
                            self.p2=j[0]
                            self.p3=k[0]
                            self.p4=l[0]
                            self.d1=new_d1
                            self.d2=new_d2
                            counter = counter + 1
        print("counter:{}".format(counter))

    def draw_contour(self, img):
        cv.drawContours(img, [self.contour], -1, (0,255,0), 3)
        cv.drawContours(img, [self.approx_contour], -1, (255,0,0), 1)
    
    def draw_corners(self, img):
        cv.line(img, self.p1, self.p2, color=(0,0,255), thickness=1)
        cv.line(img, self.p3, self.p4, color=(0,0,255), thickness=1)

        for p in [self.p1, self.p2, self.p3, self.p4]:
            cv.circle(img, (p[0],p[1]), radius=2, color=(0, 0, 255), thickness=3)

    def get_center(self):
        M = cv.moments(self.contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return (cX, cY)
