import numpy as np
import math

def weight(pixel1, pixel2, sigma):
    multiplier = 100
    delta = abs(int(pixel1) - int(pixel2))**2
    return (multiplier * math.exp(-delta/ (2 * sigma**2)))

def getPointIndex(row, col, width):
        index = col + width*row
        return index

def getGraph(width, height, array):
    sigma = 1
    central_ribs = (width - 2) * (height-2) * 4
    border_ribs = (width - 2) * 6 + (height - 2) * 6 + 4 * 2 
    st_ribs =  2 * width * height
    total_ribs = central_ribs + border_ribs + st_ribs
    ribs_list = np.zeros((total_ribs, 3), np.int32)
    iterator = 0
    for row in range(height-1):
        for col in range(width-1):
            index = getPointIndex(row, col, width)
            print('R', row, ' C', col)
            if col != width-1:
                ribs_list[iterator][0] = index
                ribs_list[iterator][1] = index+1
                ribs_list[iterator][2] = weight(array[row][col], array[row][col+1], sigma)
                iterator+=1
            if col != 0:
                ribs_list[iterator][0] = index
                ribs_list[iterator][1] = index-1
                ribs_list[iterator][2] = weight(array[row][col], array[row][col-1], sigma)
                iterator+=1
            if row != 0:
                ribs_list[iterator][0] = index
                ribs_list[iterator][1] = getPointIndex(row-1, col, width)
                ribs_list[iterator][2] = weight(array[row][col], array[row-1][col], sigma)
                iterator+=1
            if row != height-1:
                ribs_list[iterator][0] = index
                ribs_list[iterator][1] = getPointIndex(row+1, col, width)
                ribs_list[iterator][2] = weight(array[row][col], array[row+1][col], sigma)
                iterator+=1
    print(ribs_list)
