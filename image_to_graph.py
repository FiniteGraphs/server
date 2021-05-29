import numpy as np
import math
import networkx as nx
from PIL import Image


GROUPS = 17
SIGMA = 30
LAMBDA = 2

def weight(pixel1, pixel2, index1, index2, width):
    delta = (int(pixel1) - int(pixel2))**2
    distance = math.sqrt((delta) ** 2 + (index1 // width - index2 // width) ** 2 + (index1 % width - index2 % width) ** 2)
    return math.exp((- delta ** 2 / (2 * SIGMA**2))) / distance

def getPointIndex(row, col, width):
        index = col + width*row
        return index

def regionalCostObj(objHistogram, objLength, bgHistogram, bgLength, point, array, width):
    intensity = int(array[point // width][point % width])
    group = math.floor(intensity * GROUPS / 256)
    objProbability = objHistogram[group] / objLength
    bgProbability = bgHistogram[group] / bgLength
    sumProb = objProbability + bgProbability
    prob = 0
    if sumProb < 0.0000001:
        sumProb = 1
    prob = objProbability / sumProb
    return -LAMBDA * math.exp(prob)

def regionalCostBack(objHistogram, objLength, bgHistogram, bgLength, point, array, width):
    intensity = int(array[point // width][point % width])
    group = math.floor(intensity * GROUPS / 256)
    bgProbability = bgHistogram[group] / bgLength
    objProbability = objHistogram[group] / objLength
    sumProb = objProbability + bgProbability
    prob = 0
    if sumProb < 0.0000001:
        sumProb = 1
    prob = bgProbability / sumProb
    return -LAMBDA * math.exp(prob)

def createHistogram(array, pixels):
    hist_values = np.zeros(GROUPS, np.int32)
    for p in range(len(pixels)-1):
        intensity = array[pixels[p][1]][pixels[p][0]]
        group = int(intensity * GROUPS / 256)
        hist_values[group] += 1
    return hist_values   

def getGraph(width, height, array, bgPoints, objPoints):
    V = array.size + 2
    s = V - 2
    t = V - 1
    imageGraph = nx.DiGraph()
    imageGraph.add_nodes_from([x for x in range(V)])
    for row in range(height):
        for col in range(width):
            index = getPointIndex(row, col, width)
            if col != width-1:
                imageGraph.add_edge(index, index+1, capacity = weight(array[row][col], array[row][col+1], index, index+1, width))
            if col != 0:
                imageGraph.add_edge(index, index-1, capacity = weight(array[row][col], array[row][col-1], index, index-1, width))
            if row != 0:
                imageGraph.add_edge(index, getPointIndex(row-1, col, width), capacity = weight(array[row][col], array[row-1][col], index, getPointIndex(row-1, col, width), width))
            if row != height-1:
                imageGraph.add_edge(index, getPointIndex(row+1, col, width), capacity = weight(array[row][col], array[row+1][col], index, getPointIndex(row+1, col, width), width))
            imageGraph.add_edge(s, index, capacity=0)
            imageGraph.add_edge(index, t, capacity=0)
    
    K = 1. + max(sum([x[2]['capacity'] for x in list(imageGraph.edges(v, data=True))]) for v in imageGraph.nodes())

    objHistogram = createHistogram(array, objPoints)
    bgHistogram = createHistogram(array, bgPoints)
    objPointsIndexes = np.zeros(len(objPoints))
    for i in range (len(objPoints)):
        objPointsIndexes[i]=int(getPointIndex(objPoints[i][1], objPoints[i][0], width))
    bgPointsIndexes = np.zeros(len(bgPoints))
    for i in range (len(bgPoints)):
        bgPointsIndexes[i]=int(getPointIndex(bgPoints[i][1], bgPoints[i][0], width))

    for v in imageGraph.nodes():
        if(v == s or v == t):
            continue
        if v in objPointsIndexes:
            imageGraph[s][v]['capacity'] = 0
        elif v in bgPointsIndexes:
            imageGraph[s][v]['capacity'] = K
        else:
            imageGraph[s][v]['capacity'] = regionalCostObj(objHistogram, len(objPoints), bgHistogram, len(bgPoints), v, array, width)

        if v in objPointsIndexes:
            imageGraph[v][t]['capacity'] = K
        elif v in bgPointsIndexes:
            imageGraph[v][t]['capacity'] = 0
        else:
            imageGraph[v][t]['capacity'] = regionalCostBack(objHistogram, len(objPoints), bgHistogram, len(bgPoints), v, array, width)

    
    _, mincut = nx.minimum_cut(imageGraph, s, t)

    for to in mincut[0]:
        if(to == s or to == t):
            continue
        array[to//width][to%width] = 0
    for to in mincut[1]:
        if(to == s or to == t):
            continue
        array[to//width][to%width] = 255
    im = Image.fromarray(array)
    im.save("output.jpg")
    print('Successfull!')
     




