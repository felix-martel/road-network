# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 22:54:19 2016

@author: felix
"""
from time import time
from os import getcwd
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
dataset = 'maison'
default_time = 5*60*1000
startingPoint = demo[dataset]['start'] # id du sommet de départ

### TRAITEMENT DU JEU DE DONNEES ###
# <G> liste d'adjacence qui représente le graphe fourni
# <coordinates> sert uniquement à la visualisation : associe à chaque id ses
# coordonnées
G = {}
coordinates = {}
file = open(demo[dataset]['set'], 'r', newline='\n')
for line in file:
    data = line.split(" ")
    if data[0] == 'v':
        G[int(data[1])] = {}
        coordinates[int(data[1])] = [int(data[3])/1000000, int(data[2])/1000000]
    elif data[0] == 'a':
        G[int(data[1])][int(data[2])] = int(data[3][:-1])
file.close()
print("Données traitées en", time()-t0, "secondes")


def getIsochrone(D=default_time, graph=G, expall=False):
    """
    Renvoie l'isochrone D, càd la liste des sommets <s> de <G> tel que le plus court
    chemin entre <startingPoint> et <s> est de longueur <D>.
    En fait pas exactement, cf les notes quelque part.
    Pour être raccord avec ce qui est fait après, il faudrait faire une copie
    de G en début d'exécution, mais ça va bouffer de la mémoire.
    """
    t0 = time()
    I = {}
    J = {}
    I[startingPoint] = 0
    d = 0
    while d < D:
        for s, delta in I.items():  
            if delta == 0: # cas où s est un point de l'isochrone d
                for t, w in G[s].items():
                    if (t in G) and (t not in I):
                        J[t] = 0 if w == 1 else w - 1
                G.pop(s)
            else: # cas où s est un point d'une isochrone d' > d
                J[s] = delta - 1
        I = J.copy()
        J = {}
        d += 1
    print("durée d'exécution :", time() - t0)
    return(I)

def getIsochroneEnhanced(D, I=dict([(startingPoint, 0)]), graph=G, d=0):
    """
    Renvoie l'isochrone D ainsi que l'état du graphe G à la fin de l'exécution
    et le temps D associé à l'isochrone
    Permet de partir d'une isochrone donnée, déjà calculée, afin de construire
    une isochrone de rang supérieur
    En effet, le calcul de l'isochrone I(D+1) est entièrement déterminé par I(D),
    G(D) et D.
    """
    t0 = time()
    J = {}
    while d < D:
        for s, delta in I.items():  
            if delta == 0: # cas où s est un point de l'isochrone d
                for t, w in G[s].items():
                    if (t in G) and (t not in I):
                        J[t] = 0 if w == 1 else w - 1
                G.pop(s)
            else: # cas où s est un point d'une isochrone d' > d
                J[s] = delta - 1
        I = J.copy()
        J = {}
        d += 1
    print("durée d'exécution :", time() - t0)
    return(I, G, D)

  
def getIsochrones(Tmin, Tmax, step):
    """
    Renvoie les isochrones successives entre <Tmin> et <Tmax> à intervalle <step>
    """
    assert Tmin < Tmax
    I, G, D = getIsochroneEnhanced(Tmin) 
    isochrones = [I]
    t = 0
    while t < Tmax:
        I, G, D = getIsochroneEnhanced(D + step, I, G, D)
        isochrones.append(I)
    return(isochrones)
        
        
    
def getPseudoIsochrone(D1, D2, graph=G):
    """
        Returns all isochrones between D1 and D2 (ie each point such as the
        quickest path from <startingPoint> has a length between D1 and D2)
        It returns a hash table <isochrones> such as isochrones[d] contains
        the d-th isochrone
        Bah en fait non toujours pas, pour ça il ne faudrait garder que les
        sommets s vérifiant I[s] = 0
    """
    startingPoint = 2700253082 # id of the starting vertex
    I = {}
    J = {}
    I[startingPoint] = 0
    d = 0
    isochrones = {}
    while d < D2:
        for s, delta in I.items():  
            if delta == 0: # cas où s est un point de l'isochrone d
                for t, w in G[s].items():
                    if (t in G) and (t not in I):
                        J[t] = w - 1
                G.pop(s)
            else: # cas où s est un point d'une isochrone d' > d
                J[s] = delta - 1
        I = J.copy()
        J = {}
        d += 1
        if d >= D1:
            isochrones[d] = I
    return(I)
    
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
    path = 'file:///' + getcwd().replace('\\', '/') + '/vis/vis.html'
    file.write('var plottedPoints = [\n')
    for vertex in I:
        file.write(str(coordinates[vertex]))
        file.write(',\n')
    file.write('];\n\n')
    file.write('var centralMarker = \n')
    file.write(str(coordinates[startingPoint]))
    file.write('\n;')
    file.close()
    web.open(path)


def run(D=default_time, output="viz"):
    I = getIsochrone(D)
    if output == "viz":
        visualize(I)
    elif output == "list":
        exportPointList(I)
    else:
        return(I)
             