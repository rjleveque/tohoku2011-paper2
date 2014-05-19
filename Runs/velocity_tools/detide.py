
"""
Currently must be run with 4.6.
"""

from numpy import vstack, savetxt
import sys
#sys.path.append('/Users/rjl/git/tohoku2011/python/tohoku/')
import velocities as V
import dart
from gaugedirs import set_gauges

import os
topdir = os.environ['HOME'] + '/git/tohoku2011/Hawaii_velocity_measurements/'

def detide(gaugeno,HAIdir):
    """
    Detide the observations and write out the new time series for later
    use.
    """

    t,uave,vave = V.get_gauge(HAIdir)

    degree = 20
    c, t2, u2 = dart.fit_tide_poly(t,uave,degree,-20,28,0,25)
    c, t2, v2 = dart.fit_tide_poly(t,vave,degree,-20,28,0,25)
    
    if gaugeno==1123:
        t2 = t2 - 1.   # correct error in NGDC data for this gauge

    fname = HAIdir + '/detided.txt' 
    tuv = vstack([t2,u2,v2]).T
    savetxt(fname, tuv, fmt="%20.10f")
    print "Saved detided t,u,v in ",fname

if __name__ == "__main__":

    gaugenos, HAIdirs, rundirs = set_gauges()

    for gaugeno in gaugenos:
        detide(gaugeno, topdir + HAIdirs[gaugeno])
    
