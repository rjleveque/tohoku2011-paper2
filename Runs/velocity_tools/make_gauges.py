
"""
Create figures comparing computed gauges to measured.
"""

import os,sys,glob
try:
    from pyclaw.plotters.data import ClawPlotData
except:
    from clawpack.visclaw.data import ClawPlotData

#from clawpack.visclaw.data import ClawPlotData

from pylab import *

import velocities as V
import plot_gauge_velocities as PGV

def make_figs(gaugeno,rundir,outdir,veldir):

    rootdir = os.getcwd()
    os.chdir(rundir)

    # measurement values:
    mdir = os.path.abspath('../../Hawaii_velocity_measurements/%s') % veldir
    print "Looking for observations in ",mdir
    
    if 0:
        # Use raw data:
        t_m,u_m,v_m = V.get_gauge(mdir)
    else:
        # Use detided values:
        fname = mdir + '/detided.txt'
        t_m,u_m,v_m = loadtxt(os.path.join(mdir,fname), unpack=True)
        print "Read detided u,v from ",fname


    # computed results:
    plotdata = ClawPlotData()
    plotdata.outdir = outdir
    print "Looking for GeoClaw results in ",outdir

    t,speed,u,v,eta = PGV.plot_gauge(gaugeno,plotdata)
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
    #legend(['Observed','GeoClaw'])
    legend(loc=('lower right'))
    title('Velocities at gauge %s' % gaugeno)
    xlabel('u in cm/sec')
    ylabel('v in cm/sec')
    fname = "figure%sa.png" % gaugeno
    savefig(fname)
    print "Created ",fname

    figure(102,figsize=(8,10))
    clf()
    subplot(2,1,1)
    plot(t_m,u_m,'ko-',linewidth=2)
    #plot(t_m[i_ts],u_m[i_ts],'bo-',linewidth=2)
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
    
    #import pdb; pdb.set_trace()

    fname = "figure%sb.png" % gaugeno
    savefig(fname)
    print "Created ",fname
    os.chdir(rootdir)
    
