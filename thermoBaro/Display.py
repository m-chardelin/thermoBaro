#!/usr/bin/python3
#-*-coding:utf-8-*-

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



class Display():
    def __init__(self, folder, output, param, sufix):
        
        self.folder = folder
        self.output = output
        self.sufix = sufix
        self.param = param
    
        self.colour = pd.read_csv(f'{self.param}/{self.sufix}_colour.txt', sep = ';')
        self.marker = pd.read_csv(f'{self.param}/{self.sufix}_marker.txt', sep = ';')
        self.plot = pd.read_csv(f'{self.param}/{self.sufix}_plot.txt', sep = ';')
        self.mineral = pd.read_csv(f'{self.param}/{self.sufix}_mineral.txt', sep = ';')

        self.colour.index = self.colour.ts
        self.marker.index = self.marker['class']
        self.mineral.index = self.mineral.mineral


    def Load(self, data):
        self.data = pd.read_csv(data, sep = ';')

    def Initialize(self, data):

        for i in data.index:
            data.loc[i, 'colour'] = self.colour.loc[data.loc[i, 'Sample'], 'colour']
            data.loc[i, 'marker'] = self.marker.loc[data.loc[i, 'Class'], 'marker']
            data.loc[i, 'mineral'] = self.mineral.loc[data.loc[i, 'Phase'], 'colour']
    
   
    def PlotData(self,  data):
        plt.rcParams["font.family"] = "serif"
        plt.rcParams['figure.dpi'] = 149
        for i in self.plot.index:
            plt.figure()
            sub = data[data['Phase'] == self.plot.loc[i, 'mineral']]
            mineral = self.plot.loc[i, 'mineral']
    
            for j in sub.index:
                plt.plot(sub.loc[j, self.plot.loc[i, 'X']], sub.loc[j, self.plot.loc[i, 'Y']], color = sub.loc[j, 'colour'], marker = sub.loc[j, 'marker'])

            X = self.plot.loc[i, 'X']
            Y = self.plot.loc[i, 'Y']
            plt.title(f'{mineral} {X} {Y}')
            plt.xlabel(X)
            plt.ylabel(Y)
            print(f'{self.output}/{self.sufix}_{mineral}_{X}_{Y}.png')
            plt.savefig(f'{self.sufix}_{mineral}_{X}_{Y}.png')
            plt.show()
            
            
    def PlotDataTriplet(self,  data):
        plt.rcParams["font.family"] = "serif"
        plt.rcParams['figure.dpi'] = 149
        
        for i in self.plot.index:
            sub = data[data['Phase'] == self.plot.loc[i, 'mineral']]
            mineral = self.plot.loc[i, 'mineral']
            X = self.plot.loc[i, 'X']
            Y = self.plot.loc[i, 'Y']
            for t in sub.Triplet:
                if t.startswith('cr'):
                    su = sub[sub['Triplet'] == t]
                    if su.shape[0] > 2:
                        core = su[su['Class'] == 'c']
                        co = core.loc[core.index[0]]
                        rim = su[su['Class'] != 'c']
                        colour = co['colour']
                        for ir in rim.index:
                            ri = rim.loc[ir]
                            
                            cX = [co[X], ri[X]]
                            cY = [co[Y], ri[Y]]
                            plt.plot(cX, cY, color = colour)    
                    if su.shape[0] == 2:
                    	colour = su.loc[su.index[0], 'colour']
                    	plt.plot(su[X], su[Y], color = colour)                     
    
            for j in sub.index:
                plt.plot(sub.loc[j, self.plot.loc[i, 'X']], sub.loc[j, self.plot.loc[i, 'Y']], color = sub.loc[j, 'colour'], marker = sub.loc[j, 'marker'])

            plt.title(f'{mineral} {X} {Y}')
            plt.xlabel(X)
            plt.ylabel(Y)
            print(f'{self.output}/{self.sufix}_{mineral}_{X}_{Y}.png')
            plt.savefig(f'{self.sufix}_{mineral}_{X}_{Y}_triplet.png')
            plt.show()
         
      
    def PlotXY(self,  data):
        plt.rcParams["font.family"] = "serif"
        plt.rcParams['figure.dpi'] = 300
        self.ts = set(data.Sample)
        plt.rcParams.update({'font.size': 4})
        for i in self.ts :
            sub = data[data['Sample'] == i]

            for j in sub.index:
                plt.scatter(sub.loc[j, 'X'], sub.loc[j, 'Y'], color = sub.loc[j, 'mineral'], marker = sub.loc[j, 'marker'], s = 2)
                plt.annotate(sub.loc[j, 'ID'], (sub.loc[j, 'X'], sub.loc[j, 'Y']))

            plt.title(f'{i} XY')
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.axis('scaled')
            plt.savefig(f'{self.output}/{self.sufix}_{i}_XY.png')
            plt.show()

    def PlotDataInd(self, data):

        plt.rcParams["font.family"] = "serif"
        plt.rcParams['figure.dpi'] = 149

        for i in self.plot.index:
            sub = data[data['Phase'] == self.plot.loc[i, 'mineral']]
            mineral = self.plot.loc[i, 'mineral']

            for j in sub.index:
                plt.plot(sub.loc[j, self.plot.loc[i, 'X']], sub.loc[j, self.plot.loc[i, 'Y']], color = sub.loc[j, 'colour'], marker = sub.loc[j, 'marker'])
    
                plt.annotate(sub.loc[j, 'ID'], (sub.loc[j, self.plot.loc[i, 'X']], sub.loc[j, self.plot.loc[i, 'Y']]))

            X = self.plot.loc[i, 'X']
            Y = self.plot.loc[i, 'Y']
            plt.title(f'{mineral} {X} {Y}')
            plt.xlabel(X)
            plt.ylabel(Y)
            plt.savefig(f'{self.sufix}_{mineral}_{X}_{Y}_ind.png')
            plt.show()
    
    
    
    def PlotDataMean(self, data, stats):

        dataM = stats.loc['mean'] 
        dataS = stats.loc['std']
        dataM.index = np.arange(0, dataM.shape[0], 1)
        dataS.index = np.arange(0, dataS.shape[0], 1)

        for i in dataM.index:
            dataM.loc[i, 'colour'] = self.colour.loc[dataM.loc[i, 'Sample'], 'colour']
            dataM.loc[i, 'marker'] = self.marker.loc[dataM.loc[i, 'Class'], 'marker']
            data.loc[i, 'colour'] = self.colour.loc[dataM.loc[i, 'Sample'], 'colour']
            data.loc[i, 'marker'] = self.marker.loc[dataM.loc[i, 'Class'], 'marker']

        for i in self.plot.index:
            sub = data[data['Phase'] == self.plot.loc[i, 'mineral']]
            subM = dataM[dataM['Phase'] == self.plot.loc[i, 'mineral']]
            subS = dataS[dataS['Phase'] == self.plot.loc[i, 'mineral']]
    
            mineral = self.plot.loc[i, 'mineral']
    
            for j in sub.index:
                plt.plot(sub.loc[j, self.plot.loc[i, 'X']], sub.loc[j, self.plot.loc[i, 'Y']], color = 'gray', marker = sub.loc[j, 'marker'])
    
            for j in subM.index:
                plt.plot(subM.loc[j, self.plot.loc[i, 'X']], subM.loc[j, self.plot.loc[i, 'Y']], color = subM.loc[j, 'colour'], marker = subM.loc[j, 'marker'])
                plt.errorbar(subM.loc[j, self.plot.loc[i, 'X']], subM.loc[j, self.plot.loc[i, 'Y']], xerr = subS.loc[j, self.plot.loc[i, 'X']], yerr = subS.loc[j, self.plot.loc[i, 'Y']], fmt = 'none', capsize = 10, ecolor = 'red', zorder = 1)

            X = self.plot.loc[i, 'X']
            Y = self.plot.loc[i, 'Y']
            plt.title(f'{mineral} {X} {Y}')
            plt.xlabel(X)
            plt.ylabel(Y)
            plt.savefig(f'{self.sufix}_{mineral}_{X}_{Y}_EB.png')
            plt.show()


    def PlotDataMeanSBE(self, data, stats):

        dataM = stats.loc['mean'] 
        dataS = stats.loc['std']
        dataM.index = np.arange(0, dataM.shape[0], 1)
        dataS.index = np.arange(0, dataS.shape[0], 1)

        for i in dataM.index:
            dataM.loc[i, 'colour'] = self.colour.loc[dataM.loc[i, 'Sample'], 'colour']
            dataM.loc[i, 'marker'] = self.marker.loc[dataM.loc[i, 'Class'], 'marker']
            data.loc[i, 'colour'] = self.colour.loc[dataM.loc[i, 'Sample'], 'colour']
            data.loc[i, 'marker'] = self.marker.loc[dataM.loc[i, 'Class'], 'marker']

        for i in self.plot.index:
            sub = data[data['Phase'] == self.plot.loc[i, 'mineral']]
            subM = dataM[dataM['Phase'] == self.plot.loc[i, 'mineral']]
            subS = dataS[dataS['Phase'] == self.plot.loc[i, 'mineral']]
    
            mineral = self.plot.loc[i, 'mineral']
    
            for j in sub.index:
                plt.plot(sub.loc[j, self.plot.loc[i, 'X']], sub.loc[j, self.plot.loc[i, 'Y']], color = 'gray', marker = sub.loc[j, 'marker'])
    
            for j in subM.index:
                plt.plot(subM.loc[j, self.plot.loc[i, 'X']], subM.loc[j, self.plot.loc[i, 'Y']], color = subM.loc[j, 'colour'], marker = subM.loc[j, 'marker'])
                #plt.errorbar(subM.loc[j, self.plot.loc[i, 'X']], subM.loc[j, self.plot.loc[i, 'Y']], xerr = subS.loc[j, self.plot.loc[i, 'X']], yerr = subS.loc[j, self.plot.loc[i, 'Y']], fmt = 'none', capsize = 10, ecolor = 'red', zorder = 1)

            X = self.plot.loc[i, 'X']
            Y = self.plot.loc[i, 'Y']
            plt.title(f'{mineral} {X} {Y}')
            plt.xlabel(X)
            plt.ylabel(Y)
            plt.savefig(f'{self.sufix}_{mineral}_{X}_{Y}_SBE.png')
            plt.show()




