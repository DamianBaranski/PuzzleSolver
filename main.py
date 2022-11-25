import cv2 as cv
import numpy as np
import math
import puzzle


kernel = np.ones((3,3), np.uint8)
img = cv.imread('5small.png')
src=img
gray   = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
thresh = cv.threshold(gray, 210, 255, cv.THRESH_BINARY)[1]
thresh = cv.erode(thresh, kernel, iterations=1)
thresh = cv.dilate(thresh, kernel, iterations=1)
thresh = cv.bitwise_not(thresh)
contours = cv.findContours(thresh,cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)[0]

puzzles = []

for i in range(len(contours)):
  perimeter = cv.arcLength(contours[i],True)
  if perimeter>600 and perimeter<950:
      print("Puzzle no:{}".format(i))
      p = puzzle.Puzzle(contours[i])
      p.draw_contour(img)
      c = p.get_center()
      cv.putText(img, '{}'.format(i), c, cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
      p.find_corners()
      p.draw_corners(img)

cv.imshow("Display window", img)


cv.waitKey(0)
