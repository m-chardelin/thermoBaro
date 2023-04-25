import pandas as pd
import numpy as np



class StructuralFormulae():
    def __init__(self, data):
    
        self.data = data.copy()
        self.data['indexColumn'] = self.data['id']
        self.data.index = self.data['indexColumn']
        
    def Slices(self):
        for c in self.data.columns:
            col = self.data[c]
            setattr(self, c, col)
            
    def SortMinerals(self, files, name):
        
        for i in self.id:
            
            #-----------------------------------------------------------------------------------------------------------------------------------------------------
            #                                Pyroxenes
            #-----------------------------------------------------------------------------------------------------------------------------------------------------
        
            if self.SiO2[i] >= 40 and  self.SiO2[i] <= 60 and  self.MgO[i] < 30 and self.Al2O3[i] < 15 :
                self.data.loc[i, 'phaseDetection'] = 'Cpx'
                
            elif self.SiO2[i] >= 40 and self.SiO2[i] <= 60 and self.MgO[i] > 30 and self.Al2O3[i] > 15 and self.Na2O[i] > 1 and self.NiO[i] < 1 :
                self.data.loc[i, 'phaseDetection'] = 'Cpx'
                        
            #-----------------------------------------------------------------------------------------------------------------------------------------------------
            #                                Olivines
            #-----------------------------------------------------------------------------------------------------------------------------------------------------
          
            elif self.SiO2[i] >= 30 and self.SiO2[i] <= 50 and self.NiO[i] > 1 :
                self.data.loc[i, 'phaseDetection'] = 'Ol'
                    
            #-----------------------------------------------------------------------------------------------------------------------------------------------------
            #                                    Amphiboles
            #-----------------------------------------------------------------------------------------------------------------------------------------------------
           
            elif self.SiO2[i] >= 30 and self.SiO2[i] <=60 and self.MgO[i] > 1 and self.Clox[i] > 0.001 :
                self.data.loc[i, 'phaseDetection'] = 'Tr'

        self.data.to_csv(f'{files.output}/{name}.txt', sep = '&', index = None)
    
