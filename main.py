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


def getShortestDistances(quandsarreter):
	# ni plus ni moins qu'un algo de Djikstra
	# retourne le dictionnaire contenant pour clés les sommets de G et pour valeurs leur (plus courte) distance à SP
	# l'algorithme s'arrête quand la plus courte distance de startingPoint au sommet courant est plus grande que quandsarreter
	# en effet, cette distance augmente toujours au cours de l'éxecution de l'algorithme
	quandsarreter = getTime(quandsarreter)
	pluscourtedistance = dict([(s, math.inf if s!=startingPoint else 0) for s in G])
	sommetsavisiter = heapq.heapify([s for s in G], key = lambda s : pluscourtedistance[s])

	while(sommetsavisiter and pluscourtedistance[sommetsavisiter[0]] < quandsarreter):

		sommetcourant = sommetsavisiter.pop(0)
		for sommetvoisin, distance in G[sommetcourant].items():
			if pluscourtedistance[sommetvoisin] > pluscourtedistance[sommetcourant] + G[sommetcourant][sommetvoisin]:
				pluscourtedistance[sommetvoisin] = pluscourtedistance[sommetcourant] + G[sommetcourant][sommetvoisin]
		sommetsavisiter = sorted([s for s in sommetsavisiter], key = lambda s : pluscourtedistance[s])
		
		print("Pourcentage d'accomplissement :", "{:10.2f}".format(pluscourtedistance[sommetsavisiter[0]] / quandsarreter * 100))
	return(pluscourtedistance)
	

def getIsochronePab(D):
	data = {startingPoint: 0}
	result = []
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
	print(" ---------------------------- ISOCHRONE ", D , " milliseconds ")
	print(result)
	return result

def getTime(t):
    return t * 60 *1000
    
def getClosestElement(data):
    return min(data.items(), key = itemgetter(1))
 
distance = {}
previousVertex = {}
    
def getPseudoisochrone(d1=default_time, d2=2*default_time, debug=False):
      d1 = getTime(d1)
      d2 = getTime(d2)
      # Constantes
      SELECTED = False
      VISITED = True
      
      # Initialisation
      
      result = []
      
      test = []
      
      data = {startingPoint: 0}
      visitedVertices = {startingPoint: SELECTED}
      currentVertex, currentDistance = getClosestElement(data)
      
      while currentDistance < d2:
          for currentNeighbor, distanceNeighbor in G[currentVertex].items():
              if (currentNeighbor not in visitedVertices) or ((visitedVertices[currentNeighbor] == SELECTED) and (currentDistance + distanceNeighbor < data[currentNeighbor])):
                  data[currentNeighbor] = currentDistance + distanceNeighbor
                  visitedVertices[currentNeighbor] = SELECTED
                  distance[currentNeighbor] = currentDistance + distanceNeighbor
                  previousVertex[currentNeighbor] = currentVertex
#                  if (currentNeighbor not in visitedVertices) or ((visitedVertices[currentNeighbor] == SELECTED) and (currentDistance + distanceNeighbor < data[currentNeighbor])):
#                      data[currentNeighbor] = currentDistance + distanceNeighbor
#                      distance[currentNeighbor] = currentDistance + distanceNeighbor
#                      previousVertex[currentNeighbor] = currentVertex
          #fin pour tout
          
          del data[currentVertex]
          visitedVertices[currentVertex] = VISITED
          test.append(currentVertex)
          currentVertex, currentDistance = getClosestElement(data)
      #print(" --------------- PSEUDO ISOCHRONES ", d2 ," milliseconds -----")
      #print(data)
      # Fin de l'étape 1
      
      paths = []
      for vertex, distanceFromStart in data.items():
          #print("Distance from start : ", distanceFromStart/60000)
          path = []
          while distanceFromStart > d1:
              vertex = previousVertex[vertex]
              distanceFromStart = distance[vertex]
              path.append(vertex)
          result.append(vertex)
          if debug:
              paths.append(path)
          #print("Distance parcourue : ", currentDistance/60000)
      if debug:
          return paths
      return [result, data]

			
	
def vizIsochroneDjikstra(exact_time = default_time):
	delta_time = 1000 # intervalle de temps autorisé quand on dit "exactement", ici 1 seconde
	exact_time = getTime(exact_time) 
	I = getShortestDistances(quandsarreter = exact_time + delta_time + 1)
	visualize([ s for s in I if I[s] > exact_time - delta_time and I[s] < exact_time + delta_time])
    
def exportPointList(I):
    pointList = []
    for vertex in I:
        pointList.append(coordinates[vertex])
        print(coordinates[vertex], ',')
    print('\n')
    print(coordinates[startingPoint])
    return(pointList)
                    
def visualize(I):
	file = open('vis/points.js', 'w')
	file.write('var plottedPoints = [\n')
	for vertex in I:
		file.write(str(coordinates[vertex]))
		file.write(',\n')
	file.write('];\n\n')
	file.write('var centralMarker = \n')
	file.write(str(coordinates[startingPoint]))
	file.write('\n;')
	file.close()
	os.system('firefox vis/vis.html')

def visualizeMany(L):
    """
        Each element L[i] of L is a list of vertices 
        Make sure your vis/vis.html file is up-to-date
    """
    I = L[0]
    file = open('vis/points.js', 'w')
    file.write('var plottedPoints = [\n')
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
        for vertex in I:
            file.write(str(coordinates[vertex]))
            file.write(',\n')
        file.write('],\n')
    file.write('\n];')    
    file.close()
    # os.system('firefox vis/vis.html')

def viz(L):
    try: # L est une liste de liste
        origin = L[0][0]
        visualizeMany(L)
    except TypeError: # L est une liste
        visualizeMany([L])


def compareIsochroneAndPseudoisochrone():
    processData()
    t1, t2 = 5, 10
    I, J = getPseudoisochrone(t1, t2)
    processData()
    K = getIsochronePab(t1)
    processData()
    L = getIsochronePab(t2)
    isochrones = [I, J, K, L]
    visualizeMany(isochrones)
    see()
    return isochrones

def test(d1=default_time, d2=2*default_time, loc=dataset, debug=False):
    print(" --- Testing function : getPseudoisochrone  with parameters : ")
    print("Dataset : ", loc)
    print("Destination time : ", d2)
    print("Halfway time : ", d1)
    if loc != dataset:
        processData(loc)
    l = getPseudoisochrone(d1, d2, debug)
    viz(l)
    see()

def see():
    if os.name == 'nt':
        path = 'file:///' + os.getcwd().replace('\\', '/') + '/vis/vis.html'
        web.open(path) #Pour Chrome/Windows
    else:
        os.system('firefox vis/vis.html') #Pour Firefox/Linux

processData()
#visualize(getIsochronePab2(default_time))