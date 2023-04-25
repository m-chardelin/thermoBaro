docs : papiers pour le calibrage

sources : feuilles de calcul vierges

test : test pour le développement du code

thermoBaro : scripts 

        Files : input and output directories, large datasets

        Statistics : tables of data gestion, statistics 

        ThermoBarometry : contains all the daa for calibration

        Output : gestion des feuilles excel

        Display : affichage des graphs avec les bonnes couleurs et les bonnes légendes



    def ITERATIONLUCA(self, data, tmin, tmax, tstep, pmin, pmax, pstep):

        T = np.arange(tmin, tmax, tstep)

        P = np.arange(pmin, pmax, pstep)

        for p in P:

            data, data[f'TBK_{p} kbar'], data[f'TNG_{p} kbar'] = self.temperature(data, P = p)

        for t in T:
            XanC = data.XanC
            Ian = data.Ian
            XCa = data.XCa
            data['aAnc'] = self.aAnc(XanC, XCa, Ian, T = t)
            data, data[f'P_{t} K'] = self.pressure_F(data, T = t)

        return data
