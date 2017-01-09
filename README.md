# README 

## Quick Start

### 1 : Processing data

The first thing to do after running the file is to process the given data to transform the given file into a more usable hash table. For this purpose, use the function `processData`. By default, the program will load the dataset given in the `dataset` variable, but you can override this behavior by passing the desired dataset to `processData` :
```
processData()       #load the default dataset, as stated in the dataset variable
processData('paris') # load the 'paris' dataset
```

### 2 : Testing

To get the results for questions (1.1) and (1.2), just run `getResultA(t1)` and `getResultA(t2)`. For question (1.3), you have to use `getResultB(t1, t2)`.
The function `iterateResult(t1, t2)` will display the results for (1.1) to (1.3), with various starting locations : one in the heart of paris, one in the Paris area (more specifically, in the neighborood I live), and one in the countryside (Campagne, département of Hérault (34)).

The functions `iterateTestA` and `iterateTestB` are used to answer questions (A.2) and (A.3).
You can use `resetData` to reset the shortest-path tree between tests.

### 3 : Bugs

If you have a `KeyError` on runtime, please make sure you have run `processData`.

## Guide

### Core functions

The two main functions are `getIsochrone` and `getPseudoisochrone`.
```
getIsochrone(t1)
```
will return the list of coordinates forming part of the t1-isochrone, starting from `startingPoint`.

```
getPseudoisochrone(t1, t2)
```
will return an array [l1, l2], where `l1` contains the points located at exaclty `t1` from `startingPoint`, and `l2` the "frontier" of points located at more than `t2` from `startingPoint` (see the report and algorithm details for more explanations).

### Visualization
Pass a list of coordinates list to the function `visualizeMany` to print them in a Javascript file. By default, the file name is `vis/points.js`, but you can change this with the `filename` option.
**Note :** You have to update the `vis/vis.html` file in order to see multiple sets of points in the same map.

Then, you just have to run `see()` in order to open the `vis/vis.html` file in your browser and thus see the map.

### Testing
The functions `testA`, `testB` are used to perform single test for the algorithms of questions (1.1) and (1.3). The functions `getResultA` and `getResultB` are similar.

The functions `itereTestA`, `itereTestB`, `itereResultA`, `itereResultB` and `itereResult` simply loop over different distances or locations.
