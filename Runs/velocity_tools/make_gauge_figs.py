
"""
Create gauge plots comparing computed to measured.
"""

import os,sys
import matplotlib
matplotlib.use('Agg')


from velocity_tools.make_gauges import make_figs
from velocity_tools.gaugedirs import set_gauges

# Top level directory of simulation runs for each gauge:
Runs = './'   

# Set gaugenos to list of all gauges studied.
# HAIdirs and rundirs are dictionaries giving the path to observations and
# simulations for each gauge.  rundirs[gaugeno] should be a subdirectory o
# the Runs directory specified above.
gaugenos, HAIdirs, rundirs = set_gauges()



outdirs = {}  # assume outdir = '_output' below unless outdirs[gaugeno] is set
#outdirs[1123] = '_output_americano'

#gaugenos = [1123,1125,1126]  # set explicitly to plot only a subset of gauges
gaugenos = [1125,1126]  # set explicitly to plot only a subset of gauges
for gaugeno in gaugenos:
    outdirs[gaugeno] = '_mocha_28apr14'

if 0:
    gaugenos = [1116,1118,1119,1120,1121,1122]
    for gaugeno in gaugenos:
        outdirs[gaugeno] = '_americano_12apr14'

#gaugenos = [1107] 
#outdirs[1107] = '_mocha_12apr14'

for gaugeno in gaugenos:
    rundir = Runs + rundirs[gaugeno]
    HAIdir = HAIdirs[gaugeno]
    outdir = outdirs.get(gaugeno, '_output')  
    make_figs(gaugeno,rundir,outdir,HAIdir)
    print "Created figures in ", rundir

