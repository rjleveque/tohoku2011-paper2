
import os,sys,glob
import velocities as V
from gaugedirs import set_gauges

obsdir = os.path.abspath('../Observations')
gaugenos, HAIdirs, rundirs = set_gauges()

for gaugeno in [1107,1119]:
    dir = os.path.join(obsdir, HAIdirs[gaugeno])

    try:
        g = V.read_all(dir)
    except:
        print "*** Error reading velocities in ",dir


    try:
        V.plot_all(g, save=True, plotdir=dir)
    except:
        print "*** Error plotting velocities in ",dir
        
    if gaugeno in [1107,1119]:
        fname1 = os.path.join(dir, 'fig18.png')
        fname2 = '../Figures/uv_depthHAI%s.png' % gaugeno
        os.system('cp %s %s' % (fname1, fname2))
        print 'Created ', fname2

