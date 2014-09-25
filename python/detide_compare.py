r"""
Detide the observations two different ways, using the dominant harmonic 
constituents, and with a high degree polynomial. 
"""

try:
    matplotlib  # see if it's already been imported (interactive session)
except:
    import matplotlib
    matplotlib.use('Agg')  # set to image backend 

from pylab import find
import os
import numpy
import matplotlib.pyplot as plt

from gaugedirs import set_gauges
import velocities as V
import TG_DART_tools as TG

datadir = os.getcwd()
obsdir = os.path.abspath('../Observations')
gaugenos, HAIdirs, rundirs = set_gauges()

def detide_u(t,u,gaugeno,component):
    
    """
    Detide one of the components *u*  or *v*.

    :Input:
     - *t*, *u* arrays of data
     - *gaugeno* (int) gauge number, e.g. 1107
     - *component* (str) is 'u' or 'v'
    """

    j = ((t>=-20) & (t<=28))
    t1 = t[j]
    u1 = u[j]

    u1_poly_fit = TG.fit_tide_poly(t1,u1,15)

    j = find((t>=0) & (t<=25))
    t2 = t1[j]
    u2 = u1[j]
    u2_poly_fit = u1_poly_fit[j]

    p = {k:TG.periods[k] for k in TG.constituents_hawaii}
    print "Using only constituents %s" % p.keys()

    u1_harmonic_fit, u1_offset, u1_amplitude, u1_phase= \
            TG.fit_tide_harmonic(t1, u1, periods=p, t0=0, svd_tol=1e-5)
    u2_harmonic_fit = u1_harmonic_fit[j]


    if component=='u':
        plt.figure(310,figsize=(10,10))
    else:
        plt.figure(311,figsize=(10,10))
    plt.clf()
    plt.subplot(211)
    plt.plot(t,u,'k',label='Observations')
    plt.plot(t1,u1_harmonic_fit,'b',label='Harmonic fit')
    plt.plot(t1,u1_poly_fit,'r',label='Polynomial fit')
    plt.title('%s-component of velocity at HAI%s' % (component,gaugeno))
    plt.legend()
    plt.subplot(212)
    plt.plot(t2,u2 - u2_harmonic_fit,'b',label='Residual: harmonic fit')
    plt.plot(t2,u2 - u2_poly_fit,'r',label='Residual: polynomial fit')
    plt.xlim(7,14)
    plt.legend()
    return t2, u2-u2_harmonic_fit, u2-u2_poly_fit

    

def detide_uv(gaugeno):
    """
    Detide the observations and write out the new time series for later
    use.
    """

    HAIdir = os.path.join(obsdir,HAIdirs[gaugeno])
    t,uave,vave = V.get_gauge(HAIdir)

    if gaugeno==1123:
        t = t - 1.   # correct error in NGDC data for this gauge

    t2,u2h,u2p = detide_u(t,uave,gaugeno,'u')
    plt.savefig(HAIdir + '/u_detided.png')

    t2,v2h,v2p = detide_u(t,vave,gaugeno,'v')
    plt.savefig(HAIdir + '/v_detided.png')

    if 0:
        fname = HAIdir + '/detided_harmonic.txt'
        tuv = numpy.vstack([t2,u2h,v2h]).T
        numpy.savetxt(fname, tuv, fmt="%20.10f")
        print "Saved harmonic detided t,u,v in ",fname

        fname = HAIdir + '/detided_poly.txt'
        tuv = numpy.vstack([t2,u2p,v2p]).T
        numpy.savetxt(fname, tuv, fmt="%20.10f")
        print "Saved polynomial detided t,u,v in ",fname


def detide_and_plot(t,u,gaugeno,component,axes):
    """
    Detide one of the components *u*  or *v*.

    :Input:
     - *t*, *u* arrays of data
     - *gaugeno* (int) gauge number, e.g. 1107
     - *component* (str) is 'u' or 'v'
    """

    j = ((t>=-20) & (t<=28))
    t1 = t[j]
    u1 = u[j]

    u1_poly_fit = TG.fit_tide_poly(t1,u1,15)

    j = find((t>=0) & (t<=25))
    t2 = t1[j]
    u2 = u1[j]
    u2_poly_fit = u1_poly_fit[j]

    p = {k:TG.periods[k] for k in TG.constituents_hawaii}
    print "Using only constituents %s" % p.keys()

    u1_harmonic_fit, u1_offset, u1_amplitude, u1_phase= \
            TG.fit_tide_harmonic(t1, u1, periods=p, t0=0, svd_tol=1e-5)
    u2_harmonic_fit = u1_harmonic_fit[j]


    axes.plot(t,u,'k',label='Observations (depth-averaged)')
    axes.plot(t1,u1_harmonic_fit,'b',label='Harmonic fit to tide')
    axes.plot(t1,u1_poly_fit,'r',label='Polynomial fit to tide')
    if component=='u':
        axes.set_title('u (east-west velocity) at HAI%s' % gaugeno)
    else:
        axes.set_title('v (north-south velocity) at HAI%s' % gaugeno)
        axes.legend(loc='lower left')
        plt.xlabel("Hours post-quake")
    plt.ylabel("Speed in cm/sec")
    return t2, u2-u2_harmonic_fit, u2-u2_poly_fit

def make_figures(gaugeno):
    HAIdir = os.path.join(obsdir,HAIdirs[gaugeno])
    t,uave,vave = V.get_gauge(HAIdir)

    if gaugeno==1123:
        t = t - 1.   # correct error in NGDC data for this gauge

    plt.figure(310,figsize=(10,10))
    plt.clf()
    ax1 = plt.subplot(211)
    t2,u2h,u2p = detide_and_plot(t,uave,gaugeno,'u',ax1)
    ax2 = plt.subplot(212)
    t2,v2h,v2p = detide_and_plot(t,vave,gaugeno,'v',ax2)
    fname = '../Figures/uv_tideHAI%s.png' % gaugeno
    plt.savefig(fname)
    print "Created ",fname
    

if __name__=="__main__":

    for gaugeno in gaugenos:
        detide_uv(gaugeno)  

    for gaugeno in [1107, 1119]:
        make_figures(gaugeno)  # for paper
