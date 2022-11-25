import numpy as np
import math

def distance(p1, p2):
    return math.sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)

def calc_area(p1, p2, p3, p4):
    l1=distance(p1, p3)
    l2=distance(p1, p4)
    l3=distance(p2, p3)
    l4=distance(p2, p4)
    l5=distance(p1, p2)
    #triangle 1
    p=(l1+l3+l5)/2
    area1 = math.sqrt(p*(p-l1)*(p-l3)*(p-l5))
    #triangle 2
    p=(l2+l4+l5)/2
    area2 = math.sqrt(p*(p-l2)*(p-l4)*(p-l5))
    return area1+area2

def check_crosing(p1, p2, p3, p4):
    epsilon = 0.15
    if p1[0] == p2[0] or p3[0] == p4[0]:
        return False #Todo

    a12=(p1[1]-p2[1])/(p1[0]-p2[0])
    a34=(p3[1]-p4[1])/(p3[0]-p4[0])
    b12=p1[1]-p1[0]*a12
    b34=p3[1]-p3[0]*a34

    if a12 == a34:
        return False #lines parallel, not crosing

    x = (b34-b12)/(a12-a34)

    x12mean = (p1[0]+p2[0])/2
    x34mean = (p3[0]+p4[0])/2
    x12len = abs(p1[0]-p2[0])
    x34len = abs(p3[0]-p4[0])

    if abs(x12mean-x)<epsilon*x12len and abs(x34mean-x)<epsilon*x34len:
        return True
    else:
        return False

def check_angle(p1, p2, p3, p4):
    epsilon=0.15
    l1=distance(p1, p3)
    l2=distance(p1, p4)
    l3=distance(p2, p3)
    l4=distance(p2, p4)

    avg14=(l1+l4)/2
    avg23=(l2+l3)/2
    avg=(avg14+avg23)/2

    if abs(avg14-avg23)>0.4*avg:
        return False

    if not (abs(avg14-l1)<epsilon*avg14 and abs(avg14-l4)<epsilon*avg14):
        return False

    if not (abs(avg23-l2)<epsilon*avg23 and abs(avg23-l3)<epsilon*avg23):
        return False
    return True


def check_neighbor_contours(contours, i_index, j_index, k_index, l_index):
    l=len(contours)
    distance_i1 = distance(contours[i_index][0], contours[(i_index+1)%l][0])
    distance_i2 = distance(contours[i_index][0], contours[i_index-1][0])
    distance_j1 = distance(contours[j_index][0], contours[(j_index+1)%l][0])
    distance_j2 = distance(contours[j_index][0], contours[j_index-1][0])
    distance_k1 = distance(contours[k_index][0], contours[(k_index+1)%l][0])
    distance_k2 = distance(contours[k_index][0], contours[k_index-1][0])
    distance_l1 = distance(contours[l_index][0], contours[(l_index+1)%l][0])
    distance_l2 = distance(contours[l_index][0], contours[l_index-1][0])

    distance_ij = distance(contours[i_index][0], contours[j_index][0])
    distance_kl = distance(contours[k_index][0], contours[l_index][0])

    if distance_i1+distance_i2<distance_ij/3:
        return False
    if distance_j1+distance_j2<distance_ij/3:
        return False
    if distance_k1+distance_k2<distance_kl/3:
        return False
    if distance_l1+distance_l2<distance_kl/3:
        return False
    return True

