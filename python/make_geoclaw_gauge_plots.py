
"""
Create gauge plots comparing computed to measured.
"""

import os,sys
import matplotlib
#matplotlib.use('Agg')

from make_gauges import make_figs
from gaugedirs import set_gauges
from clawpack.visclaw.data import ClawPlotData
from pylab import *

# Top level directory of observation data:
obsdir = '../Observations/'

# Top level directory of simulation runs for each gauge:
Runs = '../Runs/'   

def make_figs(gaugeno,rundir,outdir,veldir):

    # measurement values:
    #mdir = os.path.abspath(os.path.join(obsdir, veldir))
    mdir = os.path.join(obsdir, veldir)
    print "Looking for observations in ",mdir
    
    # Use detided values:
    fname = 'detided_harmonic.txt'
    t_m,u_m,v_m = loadtxt(os.path.join(mdir,fname), unpack=True)
    print "Read detided u,v from ",fname


    # computed results:
    plotdata = ClawPlotData()
    plotdata.outdir = os.path.join(rundir,outdir)
    print "Looking for GeoClaw results in ",plotdata.outdir

    # from PGV.plot_gauge:
    g = plotdata.getgauge(gaugeno)
    gh = g.q[0,:]
    ghu = g.q[1,:]
    ghv = g.q[2,:]
    t = g.t + 600.  # Add 10 minutes for better agreement
    u = where(gh>0.01, ghu/gh * 100., 0.)  # convert to cm/sec
    v = where(gh>0.01, ghv/gh * 100., 0.)  # convert to cm/sec


    #t,speed,u,v,eta = PGV.plot_gauge(gaugeno,plotdata)
    t = t/3600.  # convert to hours

    i_ts = find((t_m >= t.min()) & (t_m <= t.min() + 5.))

    figure(101)
    clf()
    #plot(u_m,v_m,'k')
    plot(u,v,'r',linewidth=3,label='GeoClaw')
    plot(u_m[i_ts],v_m[i_ts],'ko',label='Observed')

    smax = max(abs(u).max(),abs(v).max(),abs(u_m).max(),abs(v_m).max()) * 1.05
    plot([-smax,smax],[0,0],'k')
    plot([0,0],[-smax,smax],'k')
    axis('scaled')
    axis([-smax,smax,-smax,smax])
    legend(loc=('lower right'))
    title('Velocities at gauge %s' % gaugeno)
    xlabel('u in cm/sec')
    ylabel('v in cm/sec')
    fname = os.path.join(rundir,"figure%sa.png" % gaugeno)
    savefig(fname)
    print "Created ",fname

    figure(102,figsize=(8,10))
    clf()
    subplot(2,1,1)
    plot(t_m,u_m,'ko-',linewidth=2)
    plot(t,u,'r',linewidth=3)
    #legend(['Observed','GeoClaw'],'upper left')
    title('u velocities at gauge %s' % gaugeno)
    xlim(t.min(),t.max())
    ylim(-smax,smax)
    ylabel('Velocities in cm/sec')
    #ylim(-80,40)

    subplot(2,1,2)
    plot(t_m,v_m,'ko-',linewidth=2,label="Observed")
    #plot(t_m[i_ts],v_m[i_ts],'bo-',linewidth=2)
    plot(t,v,'r',linewidth=3,label="GeoClaw")
    #legend(loc=('lower left'))
    title('v velocities at gauge %s' % gaugeno)
    xlim(t.min(),t.max())
    ylim(-smax,smax)
    ylabel('Velocities in cm/sec')
    xlabel('Hours post-quake')
 
    fname = os.path.join(rundir, "figure%sb.png" % gaugeno)
    savefig(fname)
    print "Created ",fname
    


# Set gaugenos to list of all gauges studied.
# HAIdirs and rundirs are dictionaries giving the path to observations and
# simulations for each gauge.  rundirs[gaugeno] should be a subdirectory o
# the Runs directory specified above.
gaugenos, HAIdirs, rundirs = set_gauges()


# Which gauges to plot:
gaugenos = []  # initialize empty, add to below.

# Dictionary to specify subdirectory of rundir containing fort.gauge file:
# Normally '_output' for each rundir, but useful to allow specifying
# different outdir when comparing results from different runs.

outdirs = {}  
           
if 0:
    gaugenos = gaugenos + [1107] 
    outdirs[1107] = '_output'

if 1:
    gaugenos = gaugenos + [1116,1118,1119,1120,1121,1122]
    for gaugeno in gaugenos:
        outdirs[gaugeno] = '_output'

if 0:
    gaugenos = gaugenos + [1123] 
    outdirs[1107] = '_output'

if 0:
    gaugenos = gaugenos + [1125,1126] 
    for gaugeno in gaugenos:
        outdirs[gaugeno] = '_output'

for gaugeno in gaugenos:
    rundir = Runs + rundirs[gaugeno]
    HAIdir = HAIdirs[gaugeno]
    outdir = outdirs.get(gaugeno, '_output')  
    make_figs(gaugeno,rundir,outdir,HAIdir)
    #print "Created figures in ", rundir

