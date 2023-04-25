#!/usr/bin/python3
#-*-coding:utf-8-*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


data = pd.read_csv('/Users/marialinechardelin/Desktop/ZABARGAD/4_analysis/4_synthesis/4_synthesis_results.txt', sep = ';')


colour = pd.read_csv('/Users/marialinechardelin/Desktop/ZABARGAD/param/ZAB4_colour.txt', sep = ';')
marker = pd.read_csv('/Users/marialinechardelin/Desktop/ZABARGAD/param/ZAB4_marker.txt', sep = ';')
plot = pd.read_csv('/Users/marialinechardelin/Desktop/ZABARGAD/param/ZAB4_plotPT.txt', sep = ';')


colour.index = colour.ts
marker.index = marker['class']


for i in data.index:
    data.loc[i, 'colour'] = colour.loc[data.loc[i, 'Sample'], 'colour']
    data.loc[i, 'marker'] = marker.loc[data.loc[i, 'Class'], 'marker']

mean = data[data['tri'] == 'mean']
std = data[data['tri'] == 'std']
data = data[data['tri'] == 'points']


mean.index = np.arange(0, mean.shape[0], 1)
std.index = np.arange(0, std.shape[0], 1)

for i in plot.index:
    X = plot.loc[i, 'X']
    Y = plot.loc[i, 'Y']
    for i in data.index:
    	plt.plot(data.loc[i, X], data.loc[i, Y], color = data.loc[i, 'colour'], marker = data.loc[i, 'marker'])
    plt.title(f'{X} {Y}')
    plt.xlabel(X)
    plt.ylabel(Y)
    plt.savefig(f'{X}_{Y}.png')
    plt.show()
    
    
for i in plot.index:

    X = plot.loc[i, 'X']
    Y = plot.loc[i, 'Y']


    for i in data.index:
    	plt.plot(data.loc[i, X], data.loc[i, Y], color = 'gray', marker = data.loc[i, 'marker'])
    
    for j in mean.index:
    	plt.plot(mean.loc[j, X], mean.loc[j, Y], color = mean.loc[j, 'colour'], marker = mean.loc[j, 'marker'])
    	
    	plt.errorbar(mean.loc[j, X], mean.loc[j, Y], xerr = std.loc[j, X], yerr = mean.loc[j, X],
  fmt = 'none', capsize = 10, ecolor = 'red', zorder = 1)

    plt.title(f'{X} {Y}')
    plt.xlabel(X)
    plt.ylabel(Y)
    plt.savefig(f'{X}_{Y}_mean.png')
    plt.show() 
    
       
    
for i in plot.index:

    X = plot.loc[i, 'X']
    Y = plot.loc[i, 'Y']

    for i in data.index:
    	plt.plot(data.loc[i, X], data.loc[i, Y], color = 'gray', marker = data.loc[i, 'marker'])
    for j in mean.index:
    	plt.plot(mean.loc[j, X], mean.loc[j, Y], color = mean.loc[j, 'colour'], marker = mean.loc[j, 'marker'])
    	
    plt.title(f'{X} {Y}')
    plt.xlabel(X)
    plt.ylabel(Y)
    plt.savefig(f'{X}_{Y}_meanSBE.png')
    plt.show()
    
    
    
T = np.arange(773, 1673, 200)
P = np.arange(0.5, 6.5, 0.5)
import random
x = random.sample(range(1650),20)
for i in x:
    for p in P:
    	a = (p - p)/6.5
    	plt.scatter(data.loc[i, f'TNG_{p} kbar'], p, color = 'red', alpha = a)
    for t in T:
    	a = (1673 - t)/1673
    	plt.scatter(t, data.loc[i, f'P_{t} K'], color = 'black', alpha = a)
plt.savefig('essaiLuca.png')
plt.show()

