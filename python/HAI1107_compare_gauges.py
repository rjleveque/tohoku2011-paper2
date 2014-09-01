"""
Make comparison plots for gauges near Honolulu Harbor, including 
synthetic gauge S1 in figure.
"""

try:
    matplotlib  # see if it's already been imported (interactive session)
except:
    import matplotlib
    matplotlib.use('Agg')  # set to image backend 

import os
from pylab import *
from clawpack.visclaw.data import ClawPlotData

rundir = '../Runs/HAI1107'
outdir = os.path.join(rundir, '_americano_1sep14')
obsdir = os.path.abspath('../Observations')

pd = ClawPlotData()
pd.outdir = outdir
g1 = pd.getgauge(1)
g1107 = pd.getgauge(1107)
g12340 = pd.getgauge(12340)


figure(1)
clf()
t = g1.t / 3600.
plot(t, g1.q[3,:], 'b', linewidth=1, label='Gauge S1')
plot(t, g1107.q[3,:], 'r', linewidth=2, label='HAI1107')
#plot(t, g12340.q[3,:], 'g', linewidth=2, label='TG 2340')
xlabel('Hours post-quake')
ylabel('meters')

legend(loc='upper right')
title('Surface elevation at Honolulu gauges')



figure(2)
clf()
s1 = 100.*sqrt(g1.q[1,:]**2 + g1.q[2,:]**2) / g1.q[0,:]
s1107 = 100.*sqrt(g1107.q[1,:]**2 + g1107.q[2,:]**2) / g1107.q[0,:]
s12340 = 100.*sqrt(g12340.q[1,:]**2 + g12340.q[2,:]**2) / g12340.q[0,:]

plot(t, s1, 'b', linewidth=1, label='Gauge S1')
plot(t, s1107, 'r', linewidth=2, label='HAI1107')
#plot(t, s12340, 'g', linewidth=2, label='TG 2340')
ylim(0,200)
xlabel('Hours post-quake')
ylabel('cm/sec')

legend(loc='upper right')
title('Flow speed at Honolulu gauges')
show()

if 1:
    figure(2)
    fname = os.path.join(rundir, 'HAI1107compareS.png')
    savefig(fname)
    print "created ",fname
    figure(1)
    fname = os.path.join(rundir, 'HAI1107compareEta.png')
    savefig(fname)
    print "created ",fname


