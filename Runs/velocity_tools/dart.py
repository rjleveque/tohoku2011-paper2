from pylab import *
import numpy

def plotdart(fname):
    d = loadtxt(fname,skiprows=2);
    t1 = d[:,2]*24*60 + d[:,3]*60 + d[:,4]  # minutes since start of month
    #t1 += (d[:,1]-2)*28*24*60 # For times in March (specific to 27 Feb 2010 Chile)
    eta1 = d[:,7]
    mask = eta1<9990
    eta = eta1[mask]
    t = t1[mask]
    figure(60)
    clf()
    plot(t,eta)
    #eta2 = smooth(eta, window_len=50)
    #plot(t,eta2,'r')
    title(fname)
    return t,eta
    
def find_freq(t,eta,t1,t2,ampl):
    """
    Determine the dominant frequencies in the gauge data by taking FFT of data
    between times t1 and t2. Returns a list of frequencies for which the
    transform amplitude is greater than ampl. Also plots the transform and
    looking at this should give a good indication of how to choose ampl.
    """
    from numpy import fft
    mask = (t>=t1) & (t<=t2)
    tsub = t[mask]
    etasub = eta[mask]
    etahat = fft.fft(etasub)
    fr = fft.fftfreq(len(etasub), tsub[1]-tsub[0])
    figure(61)
    clf()
    plot(fr[1:],abs(etahat[1:]), 'o-')
    mask = (abs(etahat)>ampl) & (fr>0)
    freqlist = fr[mask]
    return freqlist
    
def fit_tide(t,eta,freqlist,t1=-inf,t2=inf,t3=-inf,t4=inf):
    """
    Fit a function of the form c[0] + sum of sines and cosines over the
    frequencies in the list freqlist. Fit the data only in the ranges 
    t1 <= t <= t2 and t3 <= t <= t4 which should be chosen to include 
    a few periods before and a few periods after the event respectively.
    
    This does not work well for Honshu 2011 for buoys near Japan... 
    The data before and after the tsunami does not match the same Fourier series well, 
    presumably because of the large co-seismic displacement of the earth.
    
    Use fit_tide_poly below instead.
    """
    from numpy.linalg import lstsq
    mask = ((t>=t1) & (t<=t2)) | ((t>=t3) & (t<=t4))
    tsub = t[mask]
    etasub = eta[mask]
    A = ones(tsub.shape)
    for freq in freqlist:
        s1 = sin(2*pi*freq*tsub)
        c1 = cos(2*pi*freq*tsub)
        A = vstack([A,s1,c1])
    A = A.T
    c = lstsq(A,etasub)[0]
    etafit = dot(A,c)
    figure(60)
    eta2 = c[0]
    mask = (t>=t1) & (t<=t4)
    etasub2 = eta[mask]
    tsub2 = t[mask]
    for i in range((len(c)-1)/2):
        freq = freqlist[i]
        eta2 += c[2*i+1]*sin(2*pi*freq*tsub2)
        eta2 += c[2*i+2]*cos(2*pi*freq*tsub2)
    plot(tsub2,eta2,'r')
    #plot(tsub,etafit,'r')
    
    eta_notide =  etasub2 - eta2
    t_notide = tsub2    
    
    if 0:
        figure(62)
        clf()
        plot(tsub2,eta_notide)
        title("After removing tide")
    
    return c,t_notide,eta_notide
    

def fit_tide_poly(t,eta,degree, t1fit,t2fit, t1out,t2out):
    """
    Fit a polynomial of the specified degree to data in the range t1fit <= t <= t2fit.
    Returns the coefficents c of c[0] + c[1]*t + ...
    and detided data eta_notide over the range t1out <= t <= t2out.
    """
    from numpy.linalg import lstsq
    
    # select subset of t, eta where fit is done:
    mask = ((t>=t1fit) & (t<=t2fit)) 
    tfit = t[mask]
    etafit = eta[mask]
    
    
    # select subset of t, eta for output:
    mask = ((t>=t1out) & (t<=t2out)) 
    tout = t[mask]
    etaout = eta[mask]
    
    # Scale data so matrix is well-conditioned:
    scale_factor = tfit[0]
    tfit = tfit/scale_factor
    tout = tout/scale_factor
    
    # Use Newton polynomial basis using these points:
    tpts = linspace(tfit.min(),tfit.max(),degree+1)
    
    # Form A matrix Afit for least squares fit and
    # Aout for applying fit to output data:
    Afit = ones((len(tfit),degree+1))
    Aout = ones((len(tout),degree+1))
    for j in range(1,degree+1):
        Afit[:,j] = Afit[:,j-1] * (tfit - tpts[j])
        Aout[:,j] = Aout[:,j-1] * (tout - tpts[j])
        
    # Performs least squares fit:
    c = lstsq(Afit,etafit)[0]
    
    #import pdb; pdb.set_trace()
    
    # evaluate polynomial at the output times:
    etaoutfit = dot(Aout,c)
    
    # evaluate polynomial at the fit times:
    etafit2 = dot(Afit,c)
    
    # Compute de-tided values by subtracting fit values from raw data:
    tout = tout*scale_factor
    tfit = tfit*scale_factor
    t_notide = tout
    eta_notide =  etaout - etaoutfit
    
    # plot fit and de-tided data:
    figure(70,figsize=(10,12))
    clf()
    subplot(211)
    plot(tfit,etafit,'b')
    plot(tout,etaout,'g')
    plot(tfit,etafit2,'k')
    plot(tout,etaoutfit,'r')
    legend(['raw data over [t1fit, t2fit]', 'raw data over [t1out, t2out]', \
            'fit to data over [t1fit, t2fit]','fit over [t1out, t2out]'], \
             loc=0)
    ymin = etafit.min() - 0.5*(etafit.max()-etafit.min())
    ymax = etafit.max() + 0.5*(etafit.max()-etafit.min())
    ylim([ymin,ymax])
    subplot(212)
    plot(t_notide, eta_notide,'k')
    title('de-tided data over [t1out, t2out]')
        
    return c, t_notide, eta_notide
    

def fit_tide_poly2(t,eta,degree, t1fit,t2fit, t1out,t2out):
    """
    Fit a polynomial of the specified degree to data in the range t1fit <= t <= t2fit.
    Returns the coefficents c of c[0] + c[1]*t + ...
    and detided data eta_notide over the range t1out <= t <= t2out.
    """
    from numpy.linalg import lstsq
    
    # select subset of t, eta where fit is done:
    mask = ((t>=t1fit) & (t<=t2fit)) 
    tfit = t[mask]
    etafit = eta[mask]
    
    
    # select subset of t, eta for output:
    mask = ((t>=t1out) & (t<=t2out)) 
    tout = t[mask]
    etaout = eta[mask]
    
    # Scale data so matrix is well-conditioned:
    scale_factor = tfit[0]
    tfit = tfit/scale_factor
    tout = tout/scale_factor
    
    # Use Newton polynomial basis using these points:
    tpts = linspace(tfit.min(),tfit.max(),degree+1)
    
    # Form A matrix Afit for least squares fit and
    # Aout for applying fit to output data:
    Afit = ones((len(tfit),degree+1))
    Aout = ones((len(tout),degree+1))
    for j in range(1,degree+1):
        Afit[:,j] = Afit[:,j-1] * (tfit - tpts[j])
        Aout[:,j] = Aout[:,j-1] * (tout - tpts[j])
        
    # Performs least squares fit:
    c = lstsq(Afit,etafit)[0]
    
    #import pdb; pdb.set_trace()
    
    # evaluate polynomial at the output times:
    etaoutfit = dot(Aout,c)
    
    # evaluate polynomial at the fit times:
    etafit2 = dot(Afit,c)
    
    # Compute de-tided values by subtracting fit values from raw data:
    tout = tout*scale_factor
    tfit = tfit*scale_factor
    t_notide = tout
    eta_notide =  etaout - etaoutfit
    eta_tide = etaoutfit
    
    # plot fit and de-tided data:
    figure(70,figsize=(10,12))
    clf()
    subplot(211)
    plot(tfit,etafit,'b')
    plot(tout,etaout,'g')
    plot(tfit,etafit2,'k')
    plot(tout,etaoutfit,'r')
    legend(['raw data over [t1fit, t2fit]', 'raw data over [t1out, t2out]', \
            'fit to data over [t1fit, t2fit]','fit over [t1out, t2out]'], \
             loc=0)
    ymin = etafit.min() - 0.5*(etafit.max()-etafit.min())
    ymax = etafit.max() + 0.5*(etafit.max()-etafit.min())
    ylim([ymin,ymax])
    subplot(212)
    plot(t_notide, eta_notide,'k')
    title('de-tided data over [t1out, t2out]')
        
    return c, t_notide, eta_notide, eta_tide


def plot_postquake(t,eta,t_quake,gaugeno=''):
    thours = (t-t_quake)/60.
    figure(63)
    clf()
    plot(thours,eta)
    xlabel("Hours after quake")
    title("DART #%s" % gaugeno)
    
def chile2010_32412():
    """
    For 27 Feb 2010 Chile event at DART buoy 32412. 
    Requires file 32412.txt that includes Feb and March 2010 from
    http://www.ndbc.noaa.gov/station_history.php?station=32412
    """
    t,eta = plotdart('32412.txt')    
    freqlist = find_freq(t,eta,100,55000,80)
    c,t_notide,eta_notide = fit_tide(t,eta,freqlist,37000,39460,40000,42000)
    t_quake = 6*60 + 34 + 27*60*24
    plot_postquake(t_notide,eta_notide,t_quake,32412)
    xlim([0,8])
    t_sec = (t_notide-t_quake)*60.
    d = vstack([t_sec,eta_notide]).T
    fname = '32412_notide.txt'
    savetxt(fname,d)
    print "Created file ",fname
    
def chile2010_32412_figs():
    """
    Figure for paper.
    For 27 Feb 2010 Chile event at DART buoy 32412. 
    Requires file 32412.txt that includes Feb and March 2010 from
    http://www.ndbc.noaa.gov/station_history.php?station=32412
    """
    t,eta = plotdart('32412.txt')    

    freqlist = find_freq(t,eta,100,55000,80)
    c,t_notide,eta_notide = fit_tide(t,eta,freqlist,37000,39460,40000,42000)
    t_quake = 6*60 + 34 + 27*60*24

    figure(65,figsize=(10,5))
    clf()
    thours = (t-t_quake)/60.
    plot(thours,eta,'k',linewidth=2)
    xlim([-20,30])
    ylim([4325.0, 4326.2])
    xlabel("Hours after quake",fontsize=15)
    xticks(fontsize=15)
    ytickvals = ['4325.2', '4325.4', '4325.6', '4325.8', '4326.0']
    yticks([float(n) for n in ytickvals], ytickvals, fontsize=15)
    title("Depth at DART buoy 32412",fontsize=20)
    savefig("dartdata32412.eps")

    plot_postquake(t_notide,eta_notide,t_quake,32412)
    xlim([0,8])
    t_sec = (t_notide-t_quake)*60.
    d = vstack([t_sec,eta_notide]).T
    fname = '32412_notide.txt'
    savetxt(fname,d)
    print "Created file ",fname
    

def chile2010_21413():
    """
    For 27 Feb 2010 Chile event at DART buoy 21413. 
    Requires file 21413.txt that includes Feb and March 2010 from
    http://www.ndbc.noaa.gov/station_history.php?station=21413
    """
    t,eta = plotdart('21413.txt')    
    freqlist = find_freq(t,eta,100,55000,20)
    print "Using %s frequencies for data fit to tides" % len(freqlist)
    c,t_notide,eta_notide = fit_tide(t,eta,freqlist,38300,40530,41300,43800)
    t_quake = 6*60 + 34 + 27*60*24
    plot_postquake(t_notide,eta_notide,t_quake,21413)
    #xlim([0,8])
    t_sec = (t_notide-t_quake)*60.
    d = vstack([t_sec,eta_notide]).T
    fname = '21413_notide.txt'
    savetxt(fname,d)
    print "Created file ",fname

def chile2010_51406():
    """
    For 27 Feb 2010 Chile event at DART buoy 51406. 
    Requires file 51406.txt that includes Feb and March 2010 from
    http://www.ndbc.noaa.gov/station_history.php?station=51406
    """
    t,eta = plotdart('51406.txt')    
    freqlist = find_freq(t,eta,100,55000,70)
    print "Using %s frequencies for data fit to tides" % len(freqlist)
    c,t_notide,eta_notide = fit_tide(t,eta,freqlist,38000,39800,40200,41600)
    t_quake = 6*60 + 34 + 27*60*24
    plot_postquake(t_notide,eta_notide,t_quake,51406)
    #xlim([0,8])
    t_sec = (t_notide-t_quake)*60.
    d = vstack([t_sec,eta_notide]).T
    fname = '51406_notide.txt'
    savetxt(fname,d)
    print "Created file ",fname

def honshu2011_21413():
    """
    For 10 March 2011 event at DART buoy 21413. 
    http://www.ndbc.noaa.gov/station_history.php?station=21413
    """
    #t,eta = plotdart('21413.dart.txt')    
    t,eta = plotdart('21413_5day.dart')    
    t = flipud(t)
    eta = flipud(eta)
    freqlist = find_freq(t,eta,7680,15680,10)
    if 0. not in freqlist: 
        freqlist = hstack((0., freqlist))
    print "Using the following %s frequencies for data fit to tides" % len(freqlist)
    print freqlist
    c,t_notide,eta_notide = fit_tide(t,eta,freqlist,15680,16180,16680,18680)
    t_quake = 11*24*60 + 5*60 + 48 + 15/60.  # 05:48:15 UTC on March 12, 2011
    print "Time of quake = %7.2f minutes after start of March" % t_quake
    plot_postquake(t_notide,eta_notide,t_quake,21413)
    #xlim([0,8])
    t_sec = (t_notide-t_quake)*60.
    d = vstack([t_sec,eta_notide]).T
    fname = '21413_notide.txt'
    savetxt(fname,d)
    print "Created file ",fname


def honshu2011_21418():
    """
    For 10 March 2011 event at DART buoy 21418. 
    http://www.ndbc.noaa.gov/station_history.php?station=21418
    """
    import os
    fname = '21418_5day-03132011.txt'
    fname_notide = os.path.splitext(fname)[0] + '_notide.txt'
    t,eta = plotdart(fname)    
    t = flipud(t)
    eta = flipud(eta)

    c,t_notide,eta_notide = fit_tide_poly(t,eta,3,16150,16600,16160,16400)
    
    t_quake = 11*24*60 + 5*60 + 48 + 15/60.  # 05:48:15 UTC on March 12, 2011
    print "Time of quake = %7.2f minutes after start of March" % t_quake
    
    plot_postquake(t_notide,eta_notide,t_quake,21418)
    #xlim([0,8])
    t_sec = (t_notide-t_quake)*60.
    d = vstack([t_sec,eta_notide]).T
    savetxt(fname_notide,d)
    print "Created file ",fname_notide
