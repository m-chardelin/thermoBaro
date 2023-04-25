import os
from itertools import product
import pandas as pd
import numpy as np
import string
import random


class Data():
    def __init__(self, **kwargs):

        self.__dict__.update(kwargs)

       
    def SetParam(self, **kwargs):
        self.__dict__.update(kwargs)
        
        
    def Load(self, files, element, info):
        """Charge les valeurs et les infos d'un set de données"""
        self.element = pd.read_csv(f'{files.input}/{element}.txt', sep = '&')
        self.infos = pd.read_csv(f'{files.input}/{info}.txt', sep = '&')

        self.samples = set(self.infos['sample'])
        self.phases = set(self.infos['phase'])
        self.classes = set(self.infos['class'])


    def Combine(self, files, name, table1, table2, key, *fields):
        keys = [key]
        for e in fields:
            keys.append(e)

        table1 = self.element.merge(table2[keys], on=key, how='outer')
        result = table1[table1['include'] == 'y']
        
        for c in result.columns:
            try:
                result[c] = result[c].astype(float)
            except:
                pass
        
        self.data = result
        self.data.to_csv(f'{files.output}/{name}_points.txt', sep = '&')
        return result


    def Statistics(self, files, name, data, *keys):
        stats = pd.DataFrame()
        values = []

        for k in keys:
            values.append(set(data[k]))

        for (i, j, k) in product(values[0], values[1], values[2]):
        
            su = data[(data[keys[0]] == i) & (data[keys[1]] == j) & (data[keys[2]] == k) ]
            
            if su.shape[0] > 0:
                sub = su.describe()
                sub[keys[0]] = i
                sub[keys[1]] = j
                sub[keys[2]] = k
                stats = pd.concat([stats, sub])
                stats['id'] = np.arange(0, stats.shape[0], 1)
                
        for (i, j) in product(values[0], values[1]):
        
            su = data[(data[keys[0]] == i) & (data[keys[1]] == j) ]
            
            if su.shape[0] > 0:
                sub = su.describe()
                sub[keys[0]] = i
                sub[keys[1]] = j
                sub[keys[2]] = 'all'
                stats = pd.concat([stats, sub])
                stats['id'] = np.arange(0, stats.shape[0], 1)
                
        self.stats = stats
        self.stats['operation'] = self.stats.index
        self.stats.to_csv(f'{files.output}/{name}_stats.txt', sep = '&')
        return stats


    def Resumes(self, files, name, data, stats, on = ['mean', '50 %', 'std']):
        data['operation'] = 'point'
        for o in on:
            sub = stats[stats['operation'] == o]
            data = pd.concat([data, sub])
        self.resume = data
        self.resume.to_csv(f'{files.output}/{name}_resume.txt', sep = '&')
        return data


    def triplet(self, data):

        self.data = data

        self.ol = self.data[self.data['phase'] == 'Ol']
        self.opx = self.data[self.data['phase'] == 'Opx']
        self.cpx = self.data[self.data['phase'] == 'Cpx']
        self.pl = self.data[self.data['phase'] == 'Pl']
        
        describe = pd.DataFrame()

        for s in self.samples:
            olt = self.ol[self.ol['sample'] == s]
            opxt = self.opx[self.opx['sample'] == s]
            cpxt = self.cpx[self.cpx['sample'] == s]
            plt = self.pl[self.pl['sample'] == s]
                        
            if opxt.shape[0] > 0 and cpxt.shape[0] > 0 and olt.shape[0] > 0 and plt.shape[0] > 0:
                for c in self.classes:
                    opxc = opxt[opxt['class'] == c]
                    cpxc = cpxt[cpxt['class'] == c]
                    olc = olt[olt['class'] == c]
                    plc = plt[plt['class'] == c]
                    
                    if opxc.shape[0] > 0 and cpxc.shape[0] > 0 and olc.shape[0] > 0 and plc.shape[0] > 0:
                        opxi = opxc.id
                        cpxi = cpxc.id
                        pli = plc.id
                        oli = olc.id
                        output = list(product(cpxi, opxi, pli, oli))
                        des = pd.DataFrame(output)
                        des.columns = ['Cpx', 'Opx', 'Pl', 'Ol']
                        des['sample'] = s
                        des['class'] = c
                        describe = pd.concat([describe, des])
        self.triplets = describe


    def tripletMean(self, files, name, data):
	
        self.save = self.triplets
        mean = data.loc['mean']
        self.triplet(mean)
        mean = self.triplets
        mean['operation'] = 'mean'
        
        med = data.loc['50%']
        self.triplet(med)
        med = self.triplets
        med['operation'] = '50%'
        
        std = data.loc['std']
        self.triplet(std)
        std = self.triplets
        std['operation'] = 'std'

        mini = data.loc['min']
        self.triplet(mini)
        mini = self.triplets
        mini['operation'] = 'min'

        maxi = data.loc['max']
        self.triplet(maxi)
        maxi = self.triplets
        maxi['operation'] = 'max'
        
        self.tripletsMean = pd.concat([mean, med, std, mini, maxi])
        self.triplets = self.save
        self.triplets['operation'] = 'points'
        
        self.tripletsAll = pd.concat([self.triplets, self.tripletsMean])
        #self.tripletsAll.to_csv(f'{files.output}/{name}_triplets.txt', sep = '&')
        return self.tripletsAll


    def table(self, data):

        self.values = data
        syn = self.triplets.copy()
        
        add = pd.merge(syn, data[['id', 'Si', 'Ti', 'Al', 'Cr', 'Fe2+', 'Mg', 'Ca', 'Na', 'AlIVcpx', 'AlVIcpx', 'NAlT', 'NSiT', 'NCaM2', 'acats']], left_on = 'Cpx', right_on = 'id', how = 'left')

        syn.index = add.index
        syn['Sicpx'] = add.Si
        syn['Ticpx'] = add.Ti
        syn['Alcpx'] = add.Al
        syn['Crcpx'] = add.Cr
        syn['Fe2+cpx'] = add['Fe2+']
        syn['Mgcpx'] = add.Mg
        syn['Cacpx'] = add.Ca
        syn['Nacpx'] = add.Na
        syn['NAlT'] = add.NAlT
        syn['NSiT'] = add.NSiT
        syn['NCaM2'] = add.NCaM2
        syn['acats'] = add.acats

        add = pd.merge(syn, data[['id', 'Si', 'Ti', 'Al', 'Cr', 'Fe2+', 'Mg', 'Ca', 'Na', 'AlVIopx', 'AlIVopx', 'XMgM2', 'XMgM1', 'aen']], left_on = 'Opx', right_on = 'id', how = 'left')
        print(add)
        syn['Siopx'] = add.Si
        syn['Tiopx'] = add.Ti
        syn['Alopx'] = add.Al
        syn['Cropx'] = add.Cr
        syn['Fe2+opx'] = add['Fe2+']
        syn['Mgopx'] = add.Mg
        syn['Caopx'] = add.Ca
        syn['Naopx'] = add.Na
        syn['AlVIopx'] = add.AlVIopx
        syn['AlIVopx'] = add.AlIVopx
        syn['XMgM2'] = add.XMgM2
        syn['XMgM1'] = add.XMgM1
        syn['aen'] = add.aen
        

        add = pd.merge(syn, data[['id', 'afo', 'XMg']], left_on = 'Ol', right_on = 'id', how = 'left')
        syn['XMgol'] = add.XMg
        syn['afo'] = add.afo

        add = pd.merge(syn, data[['id', 'XanC', 'XCa', 'Ian', 'aAnc']], left_on = 'Pl', right_on = 'id', how = 'left')
        syn['XCa'] = add.XCa
        syn['XanC'] = add.XanC
        syn['Ian'] = add.Ian
        syn['aAnc'] = add.aAnc

        self.synthesis = syn


    def tableMean(self, data):

        self.valuesMean = data

        syn = self.tripletsMean.copy()
        
        add = pd.merge(syn, data[['id', 'Si', 'Ti', 'Al', 'Cr', 'Fe2+', 'Mg', 'Ca', 'Na', 'AlIVcpx', 'AlVIcpx', 'NAlT', 'NSiT', 'NCaM2', 'acats']], left_on = 'Cpx', right_on = 'id', how = 'left')

        syn.index = add.index
        syn['Sicpx'] = add.Si
        syn['Ticpx'] = add.Ti
        syn['Alcpx'] = add.Al
        syn['Crcpx'] = add.Cr
        syn['Fe2+cpx'] = add['Fe2+']
        syn['Mgcpx'] = add.Mg
        syn['Cacpx'] = add.Ca
        syn['Nacpx'] = add.Na
        syn['NAlT'] = add.NAlT
        syn['NSiT'] = add.NSiT
        syn['NCaM2'] = add.NCaM2
        syn['acats'] = add.acats

        add = pd.merge(syn, data[['id', 'Si', 'Ti', 'Al', 'Cr', 'Fe2+', 'Mg', 'Ca', 'Na', 'AlVIopx', 'AlIVopx', 'XMgM2', 'XMgM1', 'aen']], left_on = 'Opx', right_on = 'id', how = 'left')
        print(add)
        syn['Siopx'] = add.Si
        syn['Tiopx'] = add.Ti
        syn['Alopx'] = add.Al
        syn['Cropx'] = add.Cr
        syn['Fe2+opx'] = add['Fe2+']
        syn['Mgopx'] = add.Mg
        syn['Ca'] = add.Ca
        syn['Naopx'] = add.Na
        syn['AlVIopx'] = add.AlVIopx
        syn['AlIVopx'] = add.AlIVopx
        syn['XMgM2'] = add.XMgM2
        syn['XMgM1'] = add.XMgM1
        syn['aen'] = add.aen
        

        add = pd.merge(syn, data[['id', 'afo', 'XMg']], left_on = 'Ol', right_on = 'id', how = 'left')
        syn['XMgol'] = add.XMg
        syn['afo'] = add.afo

        add = pd.merge(syn, data[['id', 'XanC', 'XCa', 'Ian', 'aAnc']], left_on = 'Pl', right_on = 'id', how = 'left')
        syn['XCa'] = add.XCa
        syn['XanC'] = add.XanC
        syn['Ian'] = add.Ian
        syn['aAnc'] = add.aAnc

        self.synthesisMean = syn


    def CONCAT(self, files, name):
        self.synthesis['operation'] = 'points'
        self.SYN = pd.concat([self.synthesis, self.synthesisMean])
        self.SYN.to_csv(f'{files.output}/{name}_Fumagalli.txt', sep = '&')


