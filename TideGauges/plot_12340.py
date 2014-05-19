
from pylab import *
#from pyclaw.plotters.data import ClawPlotData
from clawpack.visclaw.data import ClawPlotData
import tidegauge

outdir = '../Runs/HAI1107/_output'

g_obs = loadtxt('TG12340.txt')

tsec = g_obs[:,0]
thour = tsec / 3600.
eta = g_obs[:,1]

figure(3)
clf()
plot(thour,eta,'k',linewidth=1)
plot(thour,eta,'k.',linewidth=1,label='Observed')

# computed results:
plotdata = ClawPlotData()
plotdata.outdir = outdir
print "Looking for GeoClaw results in ",plotdata.outdir
g = plotdata.getgauge(12340)

# shift by 10 minutes:
thour = (g.t + 600.) / 3600.
plot(thour, g.q[3,:],'r',linewidth=2,label='GeoClaw')
xlim(7,13)
ylim(-1,1)
legend(loc='lower right')
xticks(range(8,14),fontsize=15)
yticks(fontsize=15)
title('Surface elevation at Gauge 1612340',fontsize=15)

if 1:
    fname = "TG12340.jpg"
    savefig(fname)
    print "Created ",fname
