
try:
    matplotlib  # see if it's already been imported (interactive session)
except:
    import matplotlib
    matplotlib.use('Agg')  # set to image backend 

import os
import numpy
import matplotlib.pyplot as plt
import TG_DART_tools as TG
from clawpack.visclaw.data import ClawPlotData

save_plot = True

TGdir = os.path.abspath('../TideGauges')
outdir = '../Runs/HAI1123/_mocha_1sep14'

g_obs = numpy.loadtxt(os.path.join(TGdir, 'TG_1615680_detided.txt'))

tsec = g_obs[:,0]
thour = tsec / 3600.
eta = g_obs[:,1]

plt.figure(3)
plt.clf()
plt.plot(thour,eta,'k',linewidth=1)
plt.plot(thour,eta,'k.',linewidth=1,label='Observed')

# computed results:
plotdata = ClawPlotData()
plotdata.outdir = outdir
print "Looking for GeoClaw results in ",plotdata.outdir
g = plotdata.getgauge(5680)

# shift by 10 minutes:
thour = (g.t + 600.) / 3600.
plt.plot(thour, g.q[3,:],'r',linewidth=2,label='GeoClaw')
plt.xlim(7.5,13)
plt.ylim(-3,3)
plt.legend(loc='lower right')
plt.xticks(range(8,14),fontsize=15)
plt.yticks(fontsize=15)
plt.title('Surface elevation at TG 1615680',fontsize=15)

if save_plot:
    fname = os.path.join(TGdir, "TG_1615680_compare.png")
    plt.savefig(fname)
    print "Created ",fname
