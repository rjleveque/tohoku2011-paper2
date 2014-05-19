
""" 
Read tide gauge file of the form:
    DATE,TIME,1MIN,6MIN,ALTERNATE,PREDICTED,RESIDUAL
    03/11/2011,02:29,0.38,-,-,-,-
    03/11/2011,02:30,0.40,0.39,-,0.40,0.00
    03/11/2011,02:31,0.38,-,-,0.40,-0.02
    etc.

Usage:

    >>> import tidegauge as TG
    >>> TG.plot_tide_gauge(fname)

    where for example
      fname = '1612340_Honolulu_2011-03-11_to_2011-03-11.csv'

See:
     http://tidesandcurrents.noaa.gov/press/update031111.shtml
"""

import pylab
import numpy as np
from time import mktime
import dateutil.parser


def timestr2num(s):
    hours = int(s[:2])
    minutes_past_hour = int(s[3:5])
    minutes = hours*60 + minutes_past_hour
    return minutes

def check_missing(s):
    if s=="-":
        return np.nan
        #return 0.
    else:
        return float(s)

def read_tide_gauge(fname):
    converters = {}
    converters[0] = pylab.datestr2num
    converters[1] = timestr2num
    converters[2] = check_missing
    converters[3] = check_missing
    converters[4] = check_missing
    converters[5] = check_missing
    converters[6] = check_missing

    d = np.loadtxt(fname, converters=converters, delimiter=',', skiprows=1)
    #days = d[:,0] - d[0,0]
    #minutes = days*24*60 + d[:,1]
    days = d[:,0] + d[:,1]/(24*60.)
    t = pylab.num2date(days)
    predicted = d[:,5]
    residual = d[:,6]
    tsec = np.array([mktime(tj.timetuple()) for tj in t])
    # Time of quake:  05:46:24 UTC on March 11, 2011
    tquake = dateutil.parser.parse('05:46:24 UTC on March 11, 2011')
    tquake_sec = mktime(tquake.timetuple())
    tsec = tsec - tquake_sec
    return t,tsec,predicted,residual

def plot_tide_gauge(fname,gaugeno='?'):
    if gaugeno=='?':
        try:
            gaugeno = int(fname[:7])
        except:
            pass
    t,tsec,predicted,residual = read_tide_gauge(fname)
    fig = pylab.figure(1)
    pylab.clf()
    ax1 = pylab.subplot(211)
    pylab.plot(t,predicted,'k')
    pylab.plot(t,predicted+residual,'b')
    t1 = t[0]
    t1s = '%s/%s/%s' % (t1.month,t1.day,t1.year)
    t2 = t[-1]
    t2s = '%s/%s/%s' % (t2.month,t2.day,t2.year)
    # rotate and align the tick labels so they look better
    pylab.title('Gauge %s, From %s to %s' % (gaugeno,t1s,t2s))
    #pylab.legend(['Predicted','Observed'])
    pylab.setp( ax1.get_xticklabels(), visible=False)


    pylab.subplot(212,sharex=ax1)
    pylab.plot(t,residual,'k')
    fig.autofmt_xdate()
    pylab.title('Residual')

