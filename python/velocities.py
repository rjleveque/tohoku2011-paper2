"""
Module for plotting velocity data from observations at gauges.
"""

import numpy as np
import os
import datetime as DT
#from pyclaw.data import Data
from pylab import plot,clf,figure,xticks,yticks,subplot,text,title,legend,\
           xlabel,ylabel,xlim,ylim,axis,draw,savefig,find
from time import sleep

tquake_utc = DT.datetime(2011, 3, 11, 5, 46, 24)
# Note: could read the timezone from HAI*_station_data.txt.
dt_hawaii = DT.timedelta(0,-10*3600.)

# For 1123 only due to bug in NGDC data:
#dt_hawaii = DT.timedelta(0,-9*3600.)
# This is no longer needed -- correction is made when detiding data

tquake_default = tquake_utc + dt_hawaii

t_ts = {}
t_ts['HAI1102'] = 7.2
t_ts['HAI1107'] = 7.4
t_ts['HAI1112'] = 8.0
t_ts['HAI1116'] = 7.5
t_ts['HAI1117'] = 7.8
t_ts['HAI1118'] = 7.5
t_ts['HAI1119'] = 8.0
t_ts['HAI1120'] = 8.0
t_ts['HAI1121'] = 8.0
t_ts['HAI1122'] = 7.9
t_ts['HAI1123'] = 8.7
t_ts['HAI1124'] = 7.5
t_ts['HAI1125'] = 7.95
t_ts['HAI1126'] = 7.95
t_ts['HAI1127'] = 10 # ??
t_ts['HAI1128'] = 7.4
t_ts['HAI1129'] = 7.5  # ?
#t_ts['HAI1130'] = ?

def parse_time(s):
    """ 
    Convert string of form
     s = '2011-03-10 01:30:00'
    to datetime object t.
    """
    year = int(s[:4])
    month = int(s[5:7])
    day = int(s[8:10])
    hour = int(s[11:13])
    minute = int(s[14:16])
    sec = int(s[17:19])
    t = DT.datetime(year,month,day,hour,minute,sec)
    return t

def datetime2seconds(t, tquake=tquake_default):
    """
    t = a datetime object or an np.array of such objects,
    tquake = datetime object giving time of earthquake.
    
    return: 
    tseconds = seconds since earthquake for each element of t. 
    """

    dt = t - tquake
    if type(dt) == DT.timedelta:
        tseconds = dt.days*3600.*24 + dt.seconds
    else:
        tseconds = np.array([(d.days*3600.*24 + d.seconds) for d in dt])
    return tseconds

class Gauge(object):
    def __init__(self):
        self.tdata = []
        self.vdata = []
        self.name = ""
        self.id = ""
        self.depth = None

def read_velofile(fname, tquake=tquake_default):
    lines = open(fname,'r').readlines()
    tdata = []
    vdata = np.zeros((len(lines)-8, 4))
    for i,line in enumerate(lines[8:]):
        s = line[:19].strip()
        thours = datetime2seconds(parse_time(s), tquake) / 3600.
        tdata.append(thours)

        s = line[19:].split()
        v = float(s[0])
        theta = float(s[1])
        vdata[i,0] = v
        vdata[i,1] = theta 
        vdata[i,2] = v * np.cos((90.-theta)*np.pi/180.)
        vdata[i,3] = v * np.sin((90.-theta)*np.pi/180.)
    gauge = Gauge()
    gauge.tdata = np.array(tdata)
    gauge.vdata = vdata
    for line in lines[:10]:
        if "Station Name" in line:
            gauge.name = line.split(':')[-1].strip()
        if "Station ID" in line:
            gauge.id = line.split()[-1]
        if "Depth" in line:
            gauge.depth = float(line.split()[-1][:-1])
    return gauge


def read_all(subdir, tquake=tquake_default):
    import glob
    fnames = glob.glob(os.path.join(subdir, 'depth_*m.txt'))
    gauges = {}
    for fname in fnames:
        gauge = read_velofile(fname, tquake)
        print "Reading %s  at depth %s" % (fname, gauge.depth)
        gauges[gauge.depth] = gauge
    print "Found %s gauges" % len(gauges)
    return gauges

def get_gauge(subdir, tquake=tquake_default):
    gauges = read_all(subdir, tquake=tquake_default)
    ng = len(gauges)
    depths = gauges.keys()
    depths.sort()
    g = gauges[depths[0]]
    speed_average = g.vdata[:,0]
    u_average = g.vdata[:,2]
    v_average = g.vdata[:,3]

    for i in range(1,ng):
        g = gauges[depths[i]]
        speed_average = speed_average + g.vdata[:,0]
        u_average = u_average + g.vdata[:,2]
        v_average = v_average + g.vdata[:,3]
    speed_average = speed_average / ng
    u_average = u_average / ng
    v_average = v_average / ng
    return g.tdata,u_average,v_average

def plot_all(gauges, save=False, plotdir='.'):
    ng = len(gauges)
    R = np.linspace(0,1,ng)
    G = np.linspace(0,0,ng)
    B = np.linspace(1,0,ng)
    depths = gauges.keys()
    depths.sort()
    figure(10, [12,10])
    clf()
    for i in range(ng):
        g = gauges[depths[i]]
        subplot(ng,1,i+1)
        plot(g.tdata,g.vdata[:,0],color=[R[i],G[i],B[i]])
        if i<ng-1:
            xticks([])
        else:
            xticks(rotation=20)
        yticks([0,20])
        text(g.tdata[10],g.vdata[:,0].max()/2, '%s m' % g.depth, color='r')
        if i==0:
            title("%s   %s" % (g.id,g.name))

    if save: savefig(plotdir+"/fig10.png")
    figure(11,(12,6))
    clf()
    for i in range(ng):
        g = gauges[depths[i]]
        plot(g.tdata,g.vdata[:,0],color=[R[i],G[i],B[i]])
    #xticks(rotation=20)
    #xlim([g.tdata[0] - DT.timedelta(0,12.*3600), g.tdata[-1]])
    xlabel("Hours post-quake")
    ylabel("Speed in cm/sec")
    title("%s   %s" % (g.id,g.name))
    legend([str(d) for d in depths], 'upper left')
    if save: savefig(plotdir+"/fig11.png")

    #figure(15,(14,10))
    #clf()
    #axes([.1,.6,.5,.35])
    #axes([.1,.1,.5,.35])
    #axes([.6,.1,.35,.75])


    figure(12)
    clf()
    for i in range(ng):
        g = gauges[depths[i]]
        plot(g.vdata[:,2],g.vdata[:,3],'.',color=[R[i],G[i],B[i]],markersize=3)
    title("%s   %s" % (g.id,g.name))
    #legend([str(d) for d in depths], 'upper left')
    plot(xlim(), [0,0], 'k')
    plot([0,0], ylim(), 'k')
    xlabel('u')
    ylabel('v')
    axis('scaled')
    if save: savefig(plotdir+"/fig12.png")

    figure(13)
    clf()
    
    g = gauges[depths[0]]
    speed_average = g.vdata[:,0]
    u_average = g.vdata[:,2]
    v_average = g.vdata[:,3]
    umin = g.vdata[:,2].min()
    umax = g.vdata[:,2].max()
    vmin = g.vdata[:,3].min()
    vmax = g.vdata[:,3].max()
    dumax = max(umax-umin, vmax-vmin)
    uminmax = np.array([umin,umax])*dumax/(umax-umin)
    vminmax = np.array([vmin,vmax])*dumax/(vmax-vmin)
    print 'speed_average.shape: ', speed_average.shape

    for i in range(1,ng):
        g = gauges[depths[i]]
        speed_average = speed_average + g.vdata[:,0]
        u_average = u_average + g.vdata[:,2]
        v_average = v_average + g.vdata[:,3]
    speed_average = speed_average / ng
    u_average = u_average / ng
    v_average = v_average / ng
    t_start = t_ts.get(g.id, 0.)
    if t_start > 0:
        t_end = t_start + 5.
    else:
        t_end = 0.
    print "t_start, t_end: ",t_start,t_end
    i_ts = find((g.tdata >= t_start) & (g.tdata <= t_end))
    try:
        i_end = i_ts.max()  # last time in 5-hour window
    except:
        i_end = len(u_average)
    plot(u_average[:i_end],v_average[:i_end],'k')
    #plot(u_average[i_ts],v_average[i_ts],'r-',linewidth=1)
    plot(u_average[i_ts],v_average[i_ts],'rD-',markersize=4)
    if t_end > 0:
        legend(['Pre-tsunami','5-hour window'],'lower right')
    title("%s   %s" % (g.id,g.name))
    #legend([str(d) for d in depths], 'upper left')
    xlabel('u (velocity in longitude direction)')
    ylabel('v (velocity in latitude direction)')
    axis('scaled')
    xlim(uminmax)
    ylim(vminmax)
    plot(xlim(), [0,0], 'k')
    plot([0,0], ylim(), 'k')
    if save: savefig(plotdir+"/fig13.png")

    figure(16)
    clf()
    subplot(211)
    plot(g.tdata,u_average,'b-')
    title('u (east-west velocity) at gauge %s' % g.id)
    ylabel('cm/sec')
    xlabel('Hours post-quake')

    subplot(212)
    plot(g.tdata,v_average,'b-')
    title('v (north-south velocity) at gauge %s' % g.id)
    ylabel('cm/sec')
    xlabel('Hours post-quake')
    if save: savefig(plotdir+"/fig16.png")
    
    
    figure(17)
    clf()
    subplot(211)
    t_start = 2.
    t_end = 13.
    i_ts = find((g.tdata >= t_start) & (g.tdata <= t_end))
    for i in range(1,ng):
        g = gauges[depths[i]]
        plot(g.tdata[i_ts],g.vdata[i_ts,2],'-',color=[R[i],G[i],B[i]])
    plot(g.tdata[i_ts],u_average[i_ts],'k',linewidth=3)
    title('u (east-west velocity) at gauge %s' % g.id)
    ylabel('cm/sec')
    xlim(t_start,t_end)

    subplot(212)
    for i in range(1,ng):
        g = gauges[depths[i]]
        plot(g.tdata[i_ts],g.vdata[i_ts,3],'-',color=[R[i],G[i],B[i]])
    plot(g.tdata[i_ts],v_average[i_ts],'k',linewidth=3)
    title('v (north-south velocity) at gauge %s' % g.id)
    ylabel('cm/sec')
    xlabel('Hours post-quake')
    xlim(t_start,t_end)
    if save: savefig(plotdir+"/fig17.png")
    
    
    figure(18, figsize=(10,10))
    clf()
    subplot(211)
    t_start = -20.  # -15.
    t_end = 30.  # 15.
    i_ts = find((g.tdata >= t_start) & (g.tdata <= t_end))
    for i in range(1,ng):
        g = gauges[depths[i]]
        plot(g.tdata[i_ts],g.vdata[i_ts,2],'-',color=[R[i],G[i],B[i]])
    #plot(g.tdata[i_ts],u_average[i_ts],'k',linewidth=3)
    title('u (east-west velocity) at gauge %s' % g.id)
    ylabel('cm/sec')
    xlim(t_start,t_end)

    subplot(212)
    for i in range(1,ng):
        g = gauges[depths[i]]
        plot(g.tdata[i_ts],g.vdata[i_ts,3],'-',color=[R[i],G[i],B[i]])
    #plot(g.tdata[i_ts],v_average[i_ts],'k',linewidth=3)
    title('v (north-south velocity) at gauge %s' % g.id)
    ylabel('cm/sec')
    xlabel('Hours post-quake')
    xlim(t_start,t_end)
    if save: savefig(plotdir+"/fig18.png")

    
    
    figure(14,(12,6))
    clf()
    plot(g.tdata,speed_average,'k')
    if 0:
        vel_average = np.sqrt(u_average**2 + v_average**2)
        plot(g.tdata,vel_average,'r')
        legend(['ave speed','ave velocity'])
    #xlim([g.tdata[0] - DT.timedelta(0,12.*3600), g.tdata[-1]])
    #xticks(rotation=20)
    xlabel("Hours post-quake")
    ylabel("Speed in cm/sec")
    t_start = t_ts.get(g.id, 0.)
    if t_start > 0:
        t_end = t_start + 5.
    else:
        t_end = 0.
    print "t_start, t_end: ",t_start,t_end
    i_ts = find((g.tdata >= t_start) & (g.tdata <= t_end))
    plot(g.tdata[i_ts],speed_average[i_ts],'r')
    if t_end > 0:
        legend(['All times','5-hour window'],'upper left')

    title("Average flow speed at %s   %s" % (g.id,g.name))
    if save: savefig(plotdir+"/fig14.png")

    if 0:
        # plot points one by one
        for i,t in enumerate(g.tdata):
            figure(14)
            print '+++ t = ',t
            plot([t], [vel_average[i]], 'go')
            draw()
            figure(13)
            plot([u_average[i]], [v_average[i]], 'ro')
            if i>0:
                plot([u_average[i-1],u_average[i]], [v_average[i-1],v_average[i]], 'r-')
            draw()
            sleep(.005)
            #plot([u_average[i]], [v_average[i]], 'bo')
            draw()
    
