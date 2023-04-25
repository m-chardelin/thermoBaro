import numpy as np
import pandas as pd

class functions():
    def __init__(self, data):
        
        self.data = data
        self.phases = set(self.data['phase'])
        self.samples = set(self.data['sample'])

    ## OL

    def XCa(self, Ca, Na):
        xca = Ca/(Ca+Na)
        return xca
    
    def FeMg(self, Fe2, Mg):
        femg = Fe2 + Mg
        return femg

    def Si22(self, Si):
        si22 = 2 - Si
        return si22

    def XMg(self, Mg, Fe2):
        xmg = Mg/(Mg+Fe2)
        return xmg

    def afo(self, XMg):
        a = XMg*XMg
        return a
        
    ## CPX

    def AlIVcpx(self, Al, Cr, Ti, Na):
        aliv = (Al + Cr + 2*Ti-Na)/2
        return aliv

    def AlVIcpx(self, Al, AlIV):
        alvi = (Al - AlIV)
        return alvi

    def NAlT(self, AlIV, Si):
        nalt = AlIV/(AlIV+Si)
        return nalt

    def NSiT(self, AlIV, Si):
        nsit = Si/(Si + AlIV)
        return nsit

    def NCaM2(self, Ca):
        return Ca

    def acats(self, AlVI, NCaM2, NAlT, NSiT):
        a = 4*AlVI*NCaM2*NAlT*NSiT
        return a
        
    ## PLG

    def Xb(self, XCa):
        xb = 0.12 + 0.00038 * XCa
        return xb

    def XanC(self, XCa):
        xanc = XCa * (1 + XCa)**2 * (1/4)
        return xanc

    def Ian(self, XCa, XanC, Xb, wc = 1070, wi = 9790, R = 8.314):
        ian = R * XCa * np.log(XanC/XCa)-(wc-wi)*(1-Xb)**2
        return ian

    def aAnc(self, XanC, XCa, Ian, T = 1000, wc = 1070, R = 8.314):
        aanc = XanC * np.exp(1/(R*T)*(wc*(1-XCa)**2 + Ian ))
        return aanc
        
    ## OPX
    
    def AlVIopx(self, Al, Cr, Ti, Na):
        alvi = (Al - Cr - 2*Ti + Na)/2
        return alvi
        
    def AlIVopx(self, Al, AlVI):
        aliv = Al - AlVI
        return aliv
        
    def XMgM2(self, Mg, Fe2, Ca, Na):
        xmgm2 = Mg/(Mg + Fe2 + Ca + Na)
        return xmgm2
        
    def XMgM1(self, Mg, AlVIopx, Fe2, Ti, Cr):
        xmgm1 = Mg/(Mg / AlVIopx + Fe2 + Ti + Cr)
        return xmgm1
        
    def XAl(self, Al, Cr, Ti, Na):
        xal = 0.5*(Al-Cr-2*Ti+Na)
        return xal
        
    def aen(self, XMgM1, XMgM2):
        aen = XMgM1 * XMgM1
        return aen

    def W(self, Ca, Mg, Mn, Fe2):
        w = Ca/(Ca+Mg+Mn+Fe2)
        return w

    def A(self, Ca, Al):
        a = (Al-Ca)/2
        return a

    def FCR(self, Cr, Al, Na):
        fcr = Cr/(Al+Cr-Na)
        return fcr

    def XKW(self, W):
        xkw = 6*W/(1-2*W)
        return xkw
        
    def XKA(self, A, FCR):
        xka = A/(1-A)/(1-2.87*FCR)**2
        return xka
        
    def D(self, XKW, XKA):
        d = np.log(XKA)*np.log(XKW) - 8.6751 * np.log(XKW) + 2.2595 * np.log(XKA) + 24.568
        return d
        
    def XCr(self, Cr, Al):
        xcr = Cr/(Al+Cr)
        return xcr

    def OLIVINE(self, data, **kwargs):
        
        Si = data.Si
        Ca = data.Ca
        Na = data.Na
        Mg = data.Mg
        Fe2 = data['Fe2+']

        data['XMg']  = XMg = self.XMg(Mg, Fe2)
        data['XCa'] = self.XCa(Ca, Na)
        data['Fe+Mg'] = self.FeMg(Fe2, Mg)
        data['2-Si'] = self.Si22(Si)
        data['afo'] = self.afo(XMg)

        return data


    def CLINOPYROXENE(self, data, **kwargs):

        Al = data.Al
        Cr = data.Cr
        Ti = data.Ti
        Na = data.Na
        Si = data.Si
        Ca = data.Ca

        data['XCa'] = self.XCa(Ca, Na)
        data['2-Si'] = self.Si22(Si)
        data['AlIVcpx'] = AlIVcpx = self.AlIVcpx(Al, Cr, Ti, Na)
        data['AlVIcpx'] = AlVIcpx = self.AlVIcpx(Al, AlIVcpx)
        data['NAlT'] = NAlT = self.NAlT(AlIVcpx, Si)
        data['NSiT'] = NSiT = self.NSiT(AlIVcpx, Si)
        data['NCaM2'] = NCaM2 = self.NCaM2(Ca)
        data['acats'] = self.acats(AlIVcpx, NCaM2, NAlT, NSiT)

        return data
        
        
    def ORTHOPYROXENE(self, data, **kwargs):

        Al = data.Al
        Cr = data.Cr
        Ti = data.Ti
        Na = data.Na
        Mg = data.Mg
        Fe2 = data['Fe2+']
        Ca = data.Ca
        Na = data.Na
        Si = data.Si
        Mn = data.Mn
        P = 5

        data['2-Si'] = self.Si22(Si)
        data['AlVIopx'] = AlVIopx = self.AlVIopx(Al, Cr, Ti, Na)
        data['AlIVopx'] = AlIVopx= self.AlIVopx(Al, AlVIopx)
        data['XMgM2'] = XMgM2 = self.XMgM2(Mg, Fe2, Ca, Na)
        data['XMgM1'] = XMgM1 = self.XMgM1(Mg, AlVIopx, Fe2, Ti, Cr)
        data['aen'] = self.aen(XMgM2, XMgM1)
        XAl = data['XAl'] = self.XAl(Al, Cr, Ti, Na)
        
        
        W = data['W'] = self.W(Ca, Mg, Mn, Fe2)
        A = data['A'] = self.A(Ca, Al)
        FCR = data['FCR'] = self.FCR(Cr, Al, Na)
        XKW = data['XKW'] = self.XKW(W)
        XKA = data['XKA'] = self.XKA(A, FCR)
        D = data['D'] = self.D(XKW, XKA)
   
        self.ResetAdd()
        self.Ca = Ca
        t = self.temperature_BK(Ca, P = 5)
        data['temperature (Ca-in-Opx C)'] = self.temperature_NG(t) - 273
        data['temperature (Al-in-Opx C)'] = self.temperature_Al_in_Opx(XAl, Cr)
        
        data['temperature (Opx C)'] = self.temperatureOpx(D, XKW)
        data['pressure (Opx C)'] = self.pressureOpx(XKW, XKA, D)
        
        return data


    def PLAGIOCLASE(self, data, **kwargs):

        Ca = data.Ca 
        Na = data.Na

        data['XCa'] = XCa = self.XCa(Ca, Na)
        data['Xb'] = Xb = self.Xb(XCa)
        data['XanC'] = XanC = self.XanC(XCa)
        data['Ian'] = Ian = self.Ian(XCa, XanC, Xb)
        data['aAnc'] = aAnc = self.aAnc(XanC, XCa, Ian)

        return data


    ####### ITERATIONS ######

    def iteration(self):
    
        self.data['XMg'] = self.XMg(self.data.Mg, self.data['Fe2+'])
        self.data['XCa'] = self.XMg(self.data.Ca, self.data.Na)
        self.data['Na+K'] = self.data.Na + self.data.K
        self.data['XCr'] = self.XCr(self.data.Cr, self.data.Al)
        self.data['AlIV'] = self.AlIVcpx(self.data.Al, self.data.Cr, self.data.Ti, self.data.Na)

        for m in self.phases:

            if m == 'Ol':
                data = self.data[self.data['phase'] == m]
                ol = self.OLIVINE(data = data)

            if m == 'Cpx':

                data = self.data[self.data['phase'] == m]
                cpx = self.CLINOPYROXENE(data = data)

            if m == 'Opx':

                data = self.data[self.data['phase'] == m]
                opx = self.ORTHOPYROXENE(data = data)

            if m == 'Pl' :

                data = self.data[self.data['phase'] == m]
                pl = self.PLAGIOCLASE(data = data)
                
            if m == 'Sp':
                 sp = self.data[self.data['phase'] == m]
                 
            if m == 'Tr':
                 tr = self.data[self.data['phase'] == m]

        self.data = pd.concat([cpx, opx, ol, pl, sp, tr])



    ## TEMPERATURE
    
    def temperature_BK(self, Ca, P):                                # P [kbar] T [K]

        t = (6425 + 26.4*P)/(-np.log(Ca) + 1.843)
        
        self.add.append(t)
        self.title.append('temperature_BK')
        return t

    def temperature_NG(self, T):
        t = -0.00047262*T**2 + 2.1062*T -643.7
        
        self.add.append(t)
        self.title.append('temperature_NG')
        return t

    def temperature_Al_in_Opx(self, XAl, Cr):
        t = 636.54 + 2088.21*XAl + 14527.32 * Cr
        return t
        
    def temperatureOpx(self, D, XKW):
        t = (-6308.5 * np.log(XKW) + 45449)/ D - 273
        return t
        
    def pressureOpx(self, XKW, XKA, D):
        t = (351.32 * np.log(XKW) - 706.14 * np.log(XKA) + 299.13)/D
        return t

    def temperature(self, data, P = 5):
        
        Ca = data.Ca
        self.Ca = Ca
        t = self.temperature_BK(Ca, P)

        data['temperature_BKNG_K'] = t2 = self.temperature_NG(t)
        
        return data, t, t2


    def PT(self, files, name, data, P = 5, T = 1273):
        
        data, data['T1BK'], data['T1NG'] = self.temperature(data, P)
        data['T1BK_C'] = data['T1BK'] - 273
        data['T1NG_C'] = data['T1NG'] -273

        XanC = data.XanC
        Ian = data.Ian
        XCa = data.XCa
        
        data['aAnc1'] = data.aAnc
        data['aAnc'] = self.aAnc(XanC, XCa, Ian, T = data['T1NG'])
        data, data['P1F'] = self.pressure_F(data, T = data.T1NG)
        data, data['T2BK'], data['T2NG'] = self.temperature(data, P = data.P1F)
        data['T2BK_C'] = data['T2BK'] - 273
        data['T2NG_C'] = data['T2NG'] - 273
        data['aAnc2'] = data.aAnc
        data['aAnc'] = self.aAnc(XanC, XCa, Ian, T = data['T2NG'])
        data, data['P2F'] = self.pressure_F(data, T = data.T2NG)
        
        data['P2F/T2NG'] = data.P2F/data.T2NG
        
        data.to_csv(f'{files.output}/{name}_PT.txt', sep = '&')

        return data



        
    ## PRESURE

    def K(self, acats, aen, aAnc, afo):
        k = (acats*aen)/(aAnc*afo)
        return k

    def pressure_F(self, data, T = 1273):          # T [K], p [kbar]
        acats = data.acats
        aen = data.aen
        aAnc = data.aAnc
        afo = data.afo
        
        data['K'] = K = self.K(acats, aen, aAnc, afo)
        data['ln(K)'] = np.log(K)
        data['P_F_K'] = p = 7.2 + 0.0078*T + 0.0022*T*np.log(K)

        return data, p



    ## SetParam
    
    def SetParam(self, data, elements):
        calc = pd.DataFrame()
        for i in elements:
            calc[i] = data[i]
            setattr(self, i, data[i])
        for i in ['sample', 'triplet', 'phase', 'class']:
            calc[i] = data[i]
            setattr(self, i, data[i])
        return calc


    def SplitData(self, data, on):
        ons = list(set(data[on]))
        print(ons)
        for o in ons:
            sub = data[data[on] == o]
            setattr(self, o, sub)
            print(getattr(self, o))
            

    def ResetAdd(self):
        self.add = []
        self.title = []
        
        
    def SetAdd(self, data):
        for i, j in zip(self.title, self.add):
            data[i] = j
        return data


    ##Ca_in_Opx:
    
    def Ca_in_Opx(self, files, name, data):
        
        elements  = ['Ca']
        
        self.SplitData(data, on = 'phase')
        calc = self.SetParam(self.Opx, elements)
        
        self.ResetAdd()

        T = self.temperature_BK(self.Ca, P = 5)
        self.temperature_NG(T)
        
        calc = self.SetAdd(calc)
        calc.to_csv(f'{files.output}/{name}_BKNG.txt')
