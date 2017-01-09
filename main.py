# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 22:54:19 2016

@author: felix
"""
from time import time
import os
import math
from operator import itemgetter
import heapq
import webbrowser as web
import matplotlib.pyplot as plt

t0 = time()

### CONSTANTES ###
#
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
    'fr': {
        'set': 'data/france.in',
        'start': 122935          # Boulevard de Sébastopol
    },
    'maison': {
        'set': 'data/idf.in',
        'start': 2638124123         
    }
}
dataset = 'fr'
default_time = 5
startingPoint = demo[dataset]['start'] # id du sommet de départ
G = {}
coordinates = {}
distance = {}
previousVertex = {}
### TRAITEMENT DU JEU DE DONNEES ###
# <G> liste d'adjacence qui représente le graphe fourni
# <coordinates> sert uniquement à la visualisation : associe à chaque id ses
# coordonnées

def resetData():
    distance.clear()
    previousVertex.clear()


def processData(location=dataset):
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


def getIsochrone2(D, output='xy'):
	data = {startingPoint: 0}
	result = []
	resultXY = []
	D = getTime(D)
     
	while data:
		sommet, distanceSommet = min(data.items(), key = itemgetter(1))
		
		
		
		#print("{:10.2f}".format(distanceSommet / D * 100)) # indicateur d'avancement
		
		if distanceSommet >= D: 
			result.append(sommet)
		else:
			for voisin, dvoisin in G[sommet].items():
				if voisin in G:
					if voisin in data :
						data[voisin] = min(distanceSommet + dvoisin, data[voisin])
					else:
						data[voisin] = distanceSommet + dvoisin
		del data[sommet] # ne pas conserver 
		del G[sommet] # pour ne pas revenir en arrière
	if output == 'xy':
         resultXY = [coordinates[v] for v in result]
         return resultXY
	else:
         return result
         
def getIsochrone(d=default_time, output='xy', seeBarycenters=False):
      # Conversions minutes -> millisecondes
      d = getTime(d)
      
      # Constantes
      SELECTED = False
      VISITED = True
      
      # Initialisation
      
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
    return t * 60 *1000
    
def getClosestElement(data):
    return min(data.items(), key = itemgetter(1))
 

    
def getPseudoisochrone(d1=default_time, d2=2*default_time, output='xy', debug=False, seeBarycenters=False):
      # Conversions minutes -> millisecondes
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
                  #print(t)
                  resultXY.append((t*x1+(1-t)*x2, t*y1+(1-t)*y2))
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

    
def exportPointList(I):
    pointList = []
    for vertex in I:
        pointList.append(coordinates[vertex])
        print(coordinates[vertex], ',')
    print('\n')
    print(coordinates[startingPoint])
    return(pointList)


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
    visualizeMany(L, modeXY)
    
def compareIsochroneAndPseudoisochrone():
    processData()
    t1, t2 = 5, 10
    I, J = getPseudoisochrone(t1, t2)
    processData()
    K = getIsochrone(t1)
    processData()
    L = getIsochrone(t2)
    isochrones = [I, J, K, L]
    visualizeMany(isochrones)
    see()
    return isochrones

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
    print(" --- Testing function : getPseudoisochrone  with parameters : ")
    print("Dataset : ", loc)
    print("Destination time : ", d2)
    print("Halfway time : ", d1)
    if loc != dataset:
        processData(loc)
    l = getPseudoisochrone(d1, d2, debug=debugMode)
    viz(l)
    see()

def see():
    if os.name == 'nt':
        path = 'file:///' + os.getcwd().replace('\\', '/') + '/vis/vis.html'
        web.open(path) #Pour Chrome/Windows
    else:
        os.system('firefox vis/vis.html') #Pour Firefox/Linux

#processData()

def default(function):
    a = function()
    viz(a)
    see()
    

def isochrones(d, returnIsos=False):
    t0 = time()
    a = getIsochrone(d)
    visualizeMany(a, filename='point_'+str(d))
    t = time() - t0
    if returnIsos:
        return d, len(a[0]), t , a[0]
    else:
        return d, len(a[0]), t

def pseudoisochrones(t1, t2):
    t0 = time()
    a = getPseudoisochrone(t1, t2)
    visualizeMany(a, filename='point_'+str(t2))
    rt = time() - t0
    return len(a[0]), rt

def itereTestA(saveIsos=False):
    X, Y, runtimes = [], [], []
    print(" --- Running getIsochrone for different values of t1 --- ")
    distances = [1, 2, 3, 5, 8, 10, 15, 18, 20, 25, 30, 40, 50, 60, 2*60, 3*60, 4*60, 5*60, 6*60, 7*60, 8*60]
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

def itereTestB():
    X, Y, runtimes = [], [], []
    ratios = [1.1, 1.5, 2, 3, 4]
    t1 = 60
    print(" --- Running getPseudoisochrone for different values of t2/t1 --- ")
    t0 = time()
    for ratio in ratios:
        t2 = ratio * t1
        print("--\nt1 = ", t1)
        print("t2 = ", t2)
        print("ratio = ", ratio)
        y, r = pseudoisochrones(t1, t2)
        print("result = ", y)
        print("runtime = ", r)
        X.append(x)
        Y.append(y)
        runtimes.append(r)
        resetData()
    print("\n\nTotal runtime : ", time()-t0)
    plt.plot(X, Y)
    return X, Y, runtimes
        
