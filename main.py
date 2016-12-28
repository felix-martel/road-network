# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 22:54:19 2016

@author: felix
"""
from time import time
import os
import math

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
dataset = 'idf'
default_time = 5*60*1000
startingPoint = demo[dataset]['start'] # id du sommet de départ

### TRAITEMENT DU JEU DE DONNEES ###
# <G> liste d'adjacence qui représente le graphe fourni
# <coordinates> sert uniquement à la visualisation : associe à chaque id ses
# coordonnées
print('Traitement des données... \n')
G = {}
coordinates = {}
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
	pluscourtedistance = dict([(s, math.inf if s!=startingPoint else 0) for s in G])
	sommetsavisiter = sorted([s for s in G], key = lambda s : pluscourtedistance[s])

	while(sommetsavisiter and pluscourtedistance[sommetsavisiter[0]] < quandsarreter):

		sommetcourant = sommetsavisiter.pop(0)
		for sommetvoisin, distance in G[sommetcourant].items():
			if pluscourtedistance[sommetvoisin] > pluscourtedistance[sommetcourant] + G[sommetcourant][sommetvoisin]:
				pluscourtedistance[sommetvoisin] = pluscourtedistance[sommetcourant] + G[sommetcourant][sommetvoisin]
		sommetsavisiter = sorted([s for s in sommetsavisiter], key = lambda s : pluscourtedistance[s])
		
		print("Pourcentage d'accomplissement :", "{:10.2f}".format(pluscourtedistance[sommetsavisiter[0]] / quandsarreter * 100))
	return(pluscourtedistance)
	
def vizIsochroneDjikstra(exact_time = default_time):
	delta_time = 1000 # intervalle de temps autorisé quand on dit "exactement", ici 1 seconde
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


def run(D=default_time, output="viz"):
    I = getIsochrone(D)
    if output == "viz":
        visualize(I)
    elif output == "list":
        exportPointList(I)
    else:
        return(I)

vizIsochroneDjikstra()
