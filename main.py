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
    'maison': {
        'set': 'data/idf.in',
        'start': 2638124123         
    }
}
dataset = 'malta'
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

def processData(location=dataset):
    global dataset
    global startingPoint
    t0 = time()
    dataset = location
    startingPoint = demo[dataset]['start']
    print('Traitement des données... \n')
    G.clear()
    coordinates.clear()
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
              print(t)
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
                  print(t)
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


def visualizeMany(L, modeXY=True):
    """
        Each element L[i] of L is a list of vertices 
        Make sure your vis/vis.html file is up-to-date
    """
    I = L[0]
    file = open('vis/points.js', 'w')
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

def test(d1=default_time, d2=2*default_time, loc=dataset, debugMode=False):
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

processData()

def default(function):
    a = function()
    viz(a)
    see()
    

def getResults(t):
    t0 = time()
    a = getIsochrone(t)
    
#visualize(getIsochronePab2(default_time))