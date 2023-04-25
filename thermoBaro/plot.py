from utils import Display
import pandas as pd

p = Display.Display('~/Desktop/ZABARGAD/4_analysis/4_EPMA/4_tables', '~/Desktop/ZABARGAD/4_analysis/4_EPMA/4_figures', '~/Desktop/ZABARGAD/param', 'ZAB4')
p.Load('~/Desktop/ZABARGAD/4_analysis/4_EPMA/4_tables/ZAB4_calcEPMA.txt')
p.Initialize(p.data)
p.PlotData(p.data)
p.PlotDataTriplet(p.data)
p.PlotDataInd(p.data)

p.stats = pd.read_csv('~/Desktop/ZABARGAD/4_analysis/4_EPMA/4_tables/ZAB4_calcStatsEPMA.txt', sep = ';', index_col = 0)
p.PlotDataMean(p.data, p.stats)
p.PlotDataMeanSBE(p.data, p.stats)