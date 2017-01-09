# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 22:54:19 2016

@author: felix
"""
from time import time
import os
from operator import itemgetter
import webbrowser as web
import matplotlib.pyplot as plt



### CONSTANTS ###

demo = {
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
    'paris': {
        'set': 'data/france.in',
        'start': 361061          # Quai de Seine
    },
    'home_idf': {
        'set': 'data/idf.in',
        'start': 2638124123         
    },
    'countryside': {            # Campagne
        'set': 'data/france.in',
        'start': 1117958031
    },
    'home': {
        'set': 'data/france.in', # This is my home
        'start': 17975480
    }
}

dataset = 'paris'
default_time = 5
startingPoint = demo[dataset]['start'] # id of the starting point
G = {}
coordinates = {}
distance = {}
previousVertex = {}

### PROCESSING DATA ###
# <G> adjacency list for the provided graph
# <coordinates> used for computing the barycenters, and for visualization purpose

    
def resetData():
    distance.clear()
    previousVertex.clear()


def processData(location=dataset):
    """
        Turn the given .in file into a hashtable G, more suitable for our algorithms
        <location> should be a key of the <demo> dictionary
    """
    global dataset
    global startingPoint
    t0 = time()
    dataset = location
    startingPoint = demo[dataset]['start']
    print('Traitement des données... \n')
    G.clear()
    coordinates.clear()
    distance.clear()
    previousVertex.clear()
    file = open(demo[dataset]['set'], 'r', newline='\n')
    #~ compteur = 1
    #~ nombrelignes = sum(1 for _ in file)
    for line in file:
        data = line.split(" ")
        if data[0] == 'v':
            G[int(data[1])] = {}
            coordinates[int(data[1])] = [int(data[3])/1000000, int(data[2])/1000000]
        elif data[0] == 'a':
            G[int(data[1])][int(data[2])] = int(data[3][:-1])
        #~ print("Pourcentage d'accomplissement :", compteur/nombrelignes*100)
        #~ compteur += 1
    file.close()
    print("Données traitées en", time()-t0, "secondes")
         
def getIsochrone(d=default_time, output='xy', seeBarycenters=False):
    """
        Returns the dth isochrone
        output='xy' enables the barycenter mode
        seeBarycenters=True also returns the list of the two points involved in the barycenter, for each barycenter
    """
      # Conversion minutes -> milliseconds
      d = getTime(d)
      
      # Constants
      SELECTED = False
      VISITED = True
      
      # Initialization
      
      result = []
      resultXY = []
      if seeBarycenters:
          baryXY = []

      iso = {startingPoint: 0}
      visitedVertices = {startingPoint: SELECTED}
      #currentVertex, currentDistance = getClosestElement(iso)
      
      while iso:
          currentVertex, currentDistance = getClosestElement(iso)
          if currentDistance > d:
              x1, y1 = coordinates[previousVertex[currentVertex]]
              x2, y2 = coordinates[currentVertex]
              u1 = abs(d - distance[previousVertex[currentVertex]])
              u2 = abs(currentDistance - d)
              t = u1 / (u1 + u2)
              resultXY.append((t*x1+(1-t)*x2, t*y1+(1-t)*y2))
              if seeBarycenters:
                  baryXY.append((x1, y1))
                  baryXY.append((x2, y2))
          else:
              for currentNeighbor, distanceNeighbor in G[currentVertex].items():
                  if (currentNeighbor not in visitedVertices) or ((visitedVertices[currentNeighbor] == SELECTED) and (currentDistance + distanceNeighbor < iso[currentNeighbor])):
                      iso[currentNeighbor] = currentDistance + distanceNeighbor
                      visitedVertices[currentNeighbor] = SELECTED
                      distance[currentNeighbor] = currentDistance + distanceNeighbor
                      previousVertex[currentNeighbor] = currentVertex
          
          del iso[currentVertex]
          visitedVertices[currentVertex] = VISITED
          

      
      if seeBarycenters:
          return [resultXY, baryXY]
      else:
          return [resultXY]
      

          

def getTime(t):
    """
        Convert minutes to milliseconds
    """
    return t * 60 *1000
    
def getClosestElement(data):
    """
        Returns the (key, value) pair with minimal value, for a given <data> dictionary
    """
    return min(data.items(), key = itemgetter(1))
 

    
def getPseudoisochrone(d1=default_time, d2=2*default_time, output='xy', debug=False, seeBarycenters=False):
    """
        Returns the list of the points located at exactly t1 when the destination is more than t2 away (inner ring), and
        the t2-th isochrone (outer ring).
        debug=True also returns the path between outer and inner ring
    """
      # Conversions minutes -> milliseconds
      d1 = getTime(d1)
      d2 = getTime(d2)
      # Constantes
      SELECTED = False
      VISITED = True
      
      # Initialisation
      
      result = []
      resultXY = []
      test = []
      
      iso = {startingPoint: 0}
      visitedVertices = {startingPoint: SELECTED}
      currentVertex, currentDistance = getClosestElement(iso)
      
      while currentDistance < d2:
          for currentNeighbor, distanceNeighbor in G[currentVertex].items():
              if (currentNeighbor not in visitedVertices) or ((visitedVertices[currentNeighbor] == SELECTED) and (currentDistance + distanceNeighbor < iso[currentNeighbor])):
                  iso[currentNeighbor] = currentDistance + distanceNeighbor
                  visitedVertices[currentNeighbor] = SELECTED
                  distance[currentNeighbor] = currentDistance + distanceNeighbor
                  previousVertex[currentNeighbor] = currentVertex
          
          del iso[currentVertex]
          visitedVertices[currentVertex] = VISITED
          test.append(currentVertex)
          currentVertex, currentDistance = getClosestElement(iso)
      # -- End of step 1
          
      if seeBarycenters:
          baryXY = []
      paths = []
      for vertex, distanceFromStart in iso.items():
          path = []
          while distanceFromStart > d1:
              if (output == 'xy') and (distance[previousVertex[vertex]] <= d1):
                  x1, y1 = coordinates[vertex]
                  x2, y2 = coordinates[previousVertex[vertex]]
                  u1 = distanceFromStart - d1
                  u2 = d1 - distance[previousVertex[vertex]]
                  t = u1 / (u1 + u2)
                  newPoint = (t*x1+(1-t)*x2, t*y1+(1-t)*y2)
                  if newPoint not in resultXY:
                      resultXY.append(newPoint)
                  if seeBarycenters:
                      baryXY.append((x1, y1))
                      baryXY.append((x2, y2))
              vertex = previousVertex[vertex]
              distanceFromStart = distance[vertex]
              if debug:
                  path.append(vertex)
          result.append(vertex)
          if debug:
              paths.append(path)
      # -- End of step 2
              
      if debug:
          return paths
      if output == 'xy':
          isoXY = [coordinates[v] for v in iso]
          if seeBarycenters:
              return [resultXY, isoXY, baryXY]
          else:
              return [resultXY, isoXY]
      else:
          return [result, iso]


def visualizeMany(L, modeXY=True, filename='points'):
    """
        Each element L[i] of L is a list of vertices 
        Make sure your vis/vis.html file is up-to-date
    """
    I = L[0]
    file = open('vis/'+filename+'.js', 'w')
    file.write('var plottedPoints = [\n')
    if modeXY:
        for xy in I:
            file.write("["+"{:6f}".format(xy[0])+", "+"{:6f}".format(xy[1])+"]")
            file.write(',\n')
    else:
        for vertex in I:
            file.write(str(coordinates[vertex]))
            file.write(',\n')
    file.write('];\n\n')
    file.write('var centralMarker = \n')
    file.write(str(coordinates[startingPoint]))
    file.write('\n;\n')
    
    file.write('var pointList = [\n')
    for I in L:
        file.write('[\n')
        if modeXY:
            for xy in I:
                file.write("["+"{:6f}".format(xy[0])+", "+"{:6f}".format(xy[1])+"]")
                file.write(',\n')
        else:
            for vertex in I:
                file.write(str(coordinates[vertex]))
                file.write(',\n')
        file.write('],\n')
    file.write('\n];')    
    file.close()
    # os.system('firefox vis/vis.html')

def viz(L, modeXY=True):
    """
        Shortcut for visualizeMany
    """
    visualizeMany(L, modeXY)


def testA(d1=default_time, loc=dataset, debugMode=False):
    t0 = time()
    print(" --- Testing function : getIsochrone  with parameters : ")
    print("Dataset : ", loc)
    print("Duration : ", d1)
    if loc != dataset:
        processData(loc)
    l = getIsochrone(d1)
    print("\nResult : ", len(l[0]))
    print("\nRuntime : ", time() - t0)
    viz(l)
    see()

def testB(d1=default_time, d2=2*default_time, loc=dataset, debugMode=False):
    t0 = time()
    print(" --- Testing function : getPseudoisochrone  with parameters : ")
    print("Dataset : ", loc)
    print("Destination time : ", d2)
    print("Halfway time : ", d1)
    if loc != dataset:
        processData(loc)
    l = getPseudoisochrone(d1, d2, debug=debugMode)
    print("\nResult : ", len(l[0]))
    print("Runtime : ", time() - t0)
    viz(l)
    see()

def see():
    if os.name == 'nt':
        path = 'file:///' + os.getcwd().replace('\\', '/') + '/vis/vis.html'
        web.open(path) #Pour Chrome/Windows
    else:
        os.system('firefox vis/vis.html') #Pour Firefox/Linux


def isochrones(d, returnIsos=False):
    t0 = time()
    a = getIsochrone(d)
    visualizeMany(a, filename='point_'+str(d))
    t = time() - t0
    if returnIsos:
        return d, len(a[0]), t , a[0]
    else:
        return d, len(a[0]), t

def pseudoisochrones(t1, t2, returnIsos=False):
    t0 = time()
    a = getPseudoisochrone(t1, t2)
    visualizeMany(a, filename='point_'+str(t2))
    rt = time() - t0
    if returnIsos:
        return len(a[0]), rt, a
    else:
        return len(a[0]), rt

def itereTestA(saveIsos=False):
    X, Y, runtimes = [], [], []
    print(" --- Running getIsochrone for different values of t1 --- ")
    distances = [1, 2, 3, 5, 8, 10, 15, 18, 20, 25, 30, 40, 50] + [k*60 for k in range(1, 9)]
    t0 = time()
    if saveIsos:
        isos = []
    for d in distances:
        print("--\n t1 = ", d)
        if saveIsos:
            x, y, r, iso = isochrones(d, saveIsos)
            isos.append(iso)
        else:
            x, y, r = isochrones(d)
        print("result = ", y)
        print("runtime = ", r)
        X.append(x)
        Y.append(y)
        runtimes.append(r)
        resetData()
    print("\n\nTotal runtime : ", (time()-t0)/60)
    plt.plot(X, Y)
    if saveIsos:
        visualizeMany(isos)
        see()
        return X, Y, runtimes, isos
    return X, Y, runtimes

def itereTestB(saveIsos=False):
    X, Y, runtimes = [], [], []
    ratios = [1.1, 1.5, 2, 3, 4]
    t1 = 60
    print(" --- Running getPseudoisochrone for different values of t2/t1 --- ")
    t0 = time()
    if saveIsos:
        isos = []
    for ratio in ratios:
        t2 = ratio * t1
        print("--\nt1 = ", t1)
        print("t2 = ", t2)
        print("ratio = ", ratio)
        if saveIsos:
            y, r, iso = pseudoisochrones(t1, t2, saveIsos)
            isos.append(iso)
        else:
            y, r = pseudoisochrones(t1, t2)
        print("result = ", y)
        print("runtime = ", r)
        X.append(t2)
        Y.append(y)
        runtimes.append(r)
        resetData()
    print("\n\nTotal runtime : ", time()-t0)
    plt.plot(X, Y)
    if saveIsos:
        visualizeMany(isos)
        see()
        return X, Y, runtimes, isos
    return X, Y, runtimes
        
def getResultA(t1, location='paris'):
    global startingPoint
    startingPoint = demo[location]['start']
    t0 = time()
    print("\nStarting point : ", location)
    print("Duration : ", t1)
    l = getIsochrone(t1)
    print(" ||| Result : ", len(l[0]), " ||| ")
    print("Runtime : ", time() - t0)
    viz(l)
    see()
    return len(l[0])

def getResultB(t1, t2, location='paris'):
    global startingPoint
    startingPoint = demo[location]['start']
    t0 = time()
    print("\nStarting point : ", location)
    print("t1 : ", t1)
    print("t2 : ", t2)
    a = getPseudoisochrone(t1, t2)
    print(" ||| Result : ", len(a[0]), " ||| ")
    print("Runtime : ", time() - t0)
    visualizeMany(a)
    see()
    return len(a[0])

def itereResultA(t1):
    for loc in ['paris', 'countryside', 'home']:
        getResultA(t1, loc)
        resetData()

def itereResultB(t1, t2):
    for loc in ['paris', 'countryside', 'home']:
        getResultB(t1, t2, loc)
        resetData()

def itereResult(t1, t2):
    for loc in ['paris', 'countryside', 'home']:
        getResultA(t1, loc)
        resetDat()
        getResultA(t2, loc)
        resetData()
        getResultB(t1, t2, loc)
        resetData()
    
    
