# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 18:26:49 2017

@author: felix
"""

from time import time
import os
import math
from heapq import heappush, heappop
from operator import itemgetter

t0 = time()

### CONSTANTES ###
#
source = {
    'man': {
        'set': 'data/man.in',
        'start' : 283479111
        },
    'malta' : {
        'set': 'data/malta.in',
        'start': 30910604
    },
    'idf': {
        'set': 'data/idf.in',
        'start': 680443050          # Boulevard de Sébastopol
    },
    'maison': {
        'set': 'data/idf.in',
        'start': 2638124123         
    }
}
defaultLocation = 'malta'
defaultTime = 5
startingPoint = source[defaultLocation]['start'] # id du sommet de départ
G = {}
coordinates = {}

def convertTime(t):
    return t * 60 *1000
    
def getClosestElement(data):
    return min(data.items(), key = itemgetter(1))


    
def processData(dataset=defaultLocation):
    global startingPoint
    print('Processing data...')
    G = {}
    coordinates = {}
    startingPoint = source[dataset]['start']
    file = open(source[dataset]['set'], 'r', newline='\n')
    for line in file:
        data = line.split(" ")
        if data[0] == 'v':
            G[int(data[1])] = {}
            coordinates[int(data[1])] = [int(data[3])/1000000, int(data[2])/1000000]
        elif data[0] == 'a':
            G[int(data[1])][int(data[2])] = int(data[3][:-1])
    file.close()
    print('Data processed in ', time() - t0)

def getIsochrone(destinationTime = defaultTime):
    d = convertTime(destinationTime)
    frontier = {}
    result = []
    
    while frontier:
        

class Frontier():
    def __init__(self):
        self.ranks = {}
        self.distances = []
    
    def addVertex(vertex, distance):
        heappush(self.distances, (distance, vertex))
        
