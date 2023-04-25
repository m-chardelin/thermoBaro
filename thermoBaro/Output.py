import os
from itertools import product
import pandas as pd
import numpy as np


class data():
    def __init__(selfi, **kwargs):

        self.__dict__.update(kwargs)

        
    def load(self, element, infio, files):

        self.element = pd.read_csv(f'{files.input}/{element}.txt', sep = ';')
        print(self.element.head())

        self.info= pd.read_csv(f'{files.input}/{info}.txt', sep = ';')
        print(self.info.head())

        self.samples = set(self.info.Sample)
        self.phases = set(self.info.Phase)
        self.classes = set(self.info.Class)


    def combine(self, key, *fields):
        keys = [key]
        for e in fields:
            keys.append(e)

        self.data = self.element.merge(self.info[keys], on=key, how='outer')
        self.data = self.data[self.data['Include'] == 'y']


    def statisticsPCRM(self, data, *keys):
        stats = pd.DataFrame()
        liste = []

        for e in keys:
            liste.append(set(data[e]))

        for (i, j, k) in product(liste[0], liste[1], liste[2]):
            sub = data[data[keys[0]] == i]
            sub = sub[sub[keys[1]] == j]
            sub = sub[sub[keys[2]] == k]

            if sub.shape[0] > 0:

                sub = sub.describe()

                sub[keys[0]] = i
                sub[keys[1]] = j
                sub[keys[2]] = k

                stats = pd.concat([stats, sub])
                stats['ID'] = np.arange(0, stats.shape[0], 1)
        self.stats = stats
        return stats


    def triplet(self, data):

        self.data = data

        self.ol = self.data[self.data['Phase'] == 'Ol']
        self.opx = self.data[self.data['Phase'] == 'Opx']
        self.cpx = self.data[self.data['Phase'] == 'Cpx']
        self.pl = self.data[self.data['Phase'] == 'Pl']
        
        describe = pd.DataFrame()

        for s in self.samples:
            olt = self.ol[self.ol['Sample'] == s]
            opxt = self.opx[self.opx['Sample'] == s]
            cpxt = self.cpx[self.cpx['Sample'] == s]
            plt = self.pl[self.pl['Sample'] == s]
                        
            if opxt.shape[0] > 0 and cpxt.shape[0] > 0 and olt.shape[0] > 0 and plt.shape[0] > 0:
                for c in self.classes:
                    opxc = opxt[opxt['Class'] == c]
                    cpxc = cpxt[cpxt['Class'] == c]
                    olc = olt[olt['Class'] == c]
                    plc = plt[plt['Class'] == c]
                    
                    if opxc.shape[0] > 0 and cpxc.shape[0] > 0 and olc.shape[0] > 0 and plc.shape[0] > 0:
                        opxi = opxc.ID
                        cpxi = cpxc.ID
                        pli = plc.ID
                        oli = olc.ID
                        output = list(product(cpxi, opxi, pli, oli))
                        des = pd.DataFrame(output)
                        des.columns = ['Cpx', 'Opx', 'Pl', 'Ol']
                        des['Sample'] = s 
                        des['Class'] = c
                        describe = pd.concat([describe, des])
        describe['tri'] = 'points'
        self.triplets = describe


    def tripletMean(self, data):
	
        self.save = self.triplets
        mean = data.loc['mean']
        self.triplet(mean)
        mean = self.triplets
        mean['tri'] = 'mean'
        
        std = data.loc['std']
        self.triplet(std)
        std = self.triplets
        std['tri'] = 'std'

        self.tripletsMean = pd.concat([mean, std])
        self.triplets = self.save

    def table(self, data):

        self.values = data

        syn = self.triplets.copy()
        
        add = pd.merge(syn, data[['ID', 'acats', 'XCa', 'AlVIcpx', 'XMg']], left_on = 'Cpx', right_on = 'ID', how = 'left')
        syn.index = add.index
        syn['XCacpx'] = add.XCa
        syn['AlVICpx'] = add.AlVIcpx
        syn['XMgcpx'] = add.XMg
        syn['acats'] = add.acats

        add = pd.merge(syn, data[['ID', 'aen', 'Ca']], left_on = 'Opx', right_on = 'ID', how = 'left')
        syn['Ca'] = add.Ca
        syn['aen'] = add.aen

        
        add = pd.merge(syn, data[['ID', 'afo', 'XMg']], left_on = 'Ol', right_on = 'ID', how = 'left')
        syn['XMgol'] = add.XMg
        syn['afo'] = add.afo

        add = pd.merge(syn, data[['ID', 'XanC', 'XCa', 'Ian', 'aAnc']], left_on = 'Pl', right_on = 'ID', how = 'left')
        syn['XanC'] = add.XanC
        syn['XCa'] = add.XCa
        syn['Ian'] = add.Ian
        syn['aAnc'] = add.aAnc

        self.synthesis = syn


    def tableMean(self, data):

        self.valuesMean = data

        syn = self.tripletsMean.copy()
        
        add = pd.merge(syn, data[['ID', 'acats', 'XCa', 'AlVIcpx', 'XMg']], left_on = 'Cpx', right_on = 'ID', how = 'left')
        syn.index = add.index
        syn['XCacpx'] = add.XCa
        syn['AlVICpx'] = add.AlVIcpx
        syn['XMgcpx'] = add.XMg
        syn['acats'] = add.acats

        add = pd.merge(syn, data[['ID', 'aen', 'Ca']], left_on = 'Opx', right_on = 'ID', how = 'left')
        syn['Ca'] = add.Ca
        syn['aen'] = add.aen

        add = pd.merge(syn, data[['ID', 'afo', 'XMg']], left_on = 'Ol', right_on = 'ID', how = 'left')
        syn['XMgol'] = add.XMg
        syn['afo'] = add.afo

        add = pd.merge(syn, data[['ID', 'XanC', 'XCa', 'Ian', 'aAnc']], left_on = 'Pl', right_on = 'ID', how = 'left')
        syn['XanC'] = add.XanC
        syn['XCa'] = add.XCa
        syn['Ian'] = add.Ian
        syn['aAnc'] = add.aAnc

        self.synthesisMean = syn



    def tables_Fumagalli(self):

        syn = self.triplets.copy()
        synMean = self.tripletsMean.copy()
        data = self.values
        dataMean = self.valuesMean

        table = pd.merge(syn, data[['ID', 'Si', 'Ti', 'Al', 'Cr', 'Fe2', 'Mg', 'Ca', 'Na']], left_on = 'Cpx', right_on = 'ID', how = 'left')
        tableMean = pd.merge(synMean, dataMean[['ID', 'Si', 'Ti', 'Al', 'Cr', 'Fe2', 'Mg', 'Ca', 'Na']], left_on = 'Cpx', right_on = 'ID', how = 'left')
        table = pd.concat([table, tableMean])

        table.to_csv(f'{self.folder}/ZAB4_analysis_cpxFEPMA.txt', sep = ';')

        table = pd.merge(syn, data[['ID', 'Si', 'Ti', 'Al', 'Cr', 'Fe2', 'Mg', 'Ca', 'Na']], left_on = 'Opx', right_on = 'ID', how = 'left')
        tableMean = pd.merge(synMean, dataMean[['ID', 'Si', 'Ti', 'Al', 'Cr', 'Fe2', 'Mg', 'Ca', 'Na']], left_on = 'Opx', right_on = 'ID', how = 'left')
        table = pd.concat([table, tableMean])
        table.to_csv(f'{self.folder}/ZAB4_analysis_opxFEPMA.txt', sep = ';')

        table = pd.merge(syn, data[['ID', 'XCa']], left_on = 'Pl', right_on = 'ID', how = 'left')
        tableMean = pd.merge(synMean, dataMean[['ID', 'XCa']], left_on = 'Pl', right_on = 'ID', how = 'left')
        table = pd.concat([table, tableMean])
        table.to_csv(f'{self.folder}/ZAB4_analysis_plFEPMA.txt', sep = ';')

        table = pd.merge(syn, data[['ID', 'XMg']], left_on = 'Ol', right_on = 'ID', how = 'left')
        tableMean = pd.merge(synMean, dataMean[['ID', 'XMg']], left_on = 'Ol', right_on = 'ID', how = 'left')
        table = pd.concat([table, tableMean])
        table.to_csv(f'{self.folder}/ZAB4_analysis_olFEPMA.txt', sep = ';')
    

    def tables_Nimis(self):

        syn = self.triplets.copy()
        synMean = self.tripletsMean.copy()
        data = self.values
        dataMean = self.valuesMean
        
        table = pd.merge(syn, data[['ID', 'SiO2', 'TiO2', 'Al2O3', 'Cr2O3', 'FeO', 'MnO', 'NiO', 'MgO', 'CaO', 'Na2O', 'K2O']], left_on = 'Ol', right_on = 'ID', how = 'left')
        tableMean = pd.merge(synMean, dataMean[['ID', 'SiO2', 'TiO2', 'Al2O3', 'Cr2O3', 'FeO', 'MnO', 'NiO', 'MgO', 'CaO', 'Na2O', 'K2O']], left_on = 'Ol', right_on = 'ID', how = 'left')
        table = pd.concat([table, tableMean])
        table.to_csv(f'{self.folder}/ZAB4_analysis_olNEPMA.txt', sep = ';')


        table = pd.merge(syn, data[['ID', 'SiO2', 'TiO2', 'Al2O3', 'Cr2O3', 'FeO', 'MnO', 'NiO', 'MgO', 'CaO', 'Na2O', 'K2O']], left_on = 'Opx', right_on = 'ID', how = 'left')
        tableMean = pd.merge(synMean, dataMean[['ID', 'SiO2', 'TiO2', 'Al2O3', 'Cr2O3', 'FeO', 'MnO', 'NiO', 'MgO', 'CaO', 'Na2O', 'K2O']], left_on = 'Opx', right_on = 'ID', how = 'left')
        table = pd.concat([table, tableMean])
        table.to_csv(f'{self.folder}/ZAB4_analysis_opxNEPMA.txt', sep = ';')

        
        table = pd.merge(syn, data[['ID', 'SiO2', 'TiO2', 'Al2O3', 'Cr2O3', 'FeO', 'MnO', 'NiO', 'MgO', 'CaO', 'Na2O', 'K2O']], left_on = 'Cpx', right_on = 'ID', how = 'left')
        tableMean = pd.merge(synMean, dataMean[['ID', 'SiO2', 'TiO2', 'Al2O3', 'Cr2O3', 'FeO', 'MnO', 'NiO', 'MgO', 'CaO', 'Na2O', 'K2O']], left_on = 'Cpx', right_on = 'ID', how = 'left')
        table = pd.concat([table, tableMean])
        table.to_csv(f'{self.folder}/ZAB4_analysis_cpxNEPMA.txt', sep = ';')



    def CONCAT(self):

        self.SYN = pd.concat([self.synthesis, self.synthesisMean])


    def saveResults(self):

        self.values.to_csv(f'{self.folder}/ZAB4_calcEPMA.txt', sep = ';')
        self.valuesMean.to_csv(f'{self.folder}/ZAB4_calcStatsEPMA.txt', sep = ';')
        self.triplets.to_csv(f'{self.folder}/ZAB4_triplets.txt', sep = ';')
        self.tripletsMean.to_csv(f'{self.folder}/ZAB4_tripletsMean.txt', sep = ';')
        self.synthesis.to_csv(f'{self.folder}/ZAB4_synthesis.txt', sep = ';')
        self.synthesisMean.to_csv(f'{self.folder}/ZAB4_synthesisMean.txt', sep = ';')
        self.SYN.to_csv(f'{self.folder}/ZAB4_synthesisEPMA.txt', sep = ';')
        
