"""
Plot gauge output from GeoClaw.
"""

from pylab import *
import velocities as V
import dart

def plot_gauge(gaugeno, plotdata):
    """
    Plot results for gauge number gaugeno.
    plotdata should be an object of class ClawPlotData that has 
       plotdata.outdir set to the output directory.
    """

    g = plotdata.getgauge(gaugeno)
    gh = g.q[0,:]
    ghu = g.q[1,:]
    ghv = g.q[2,:]
    t = g.t + 600.  # Add 10 minutes for better agreement
    u = where(gh>0.01, ghu/gh * 100., 0.)  # convert to cm/sec
    v = where(gh>0.01, ghv/gh * 100., 0.)  # convert to cm/sec

    figure(101)
    clf()
    plot(u,v)
    umax = abs(u).max()
    vmax = abs(v).max()
    smax = max(umax,vmax) * 1.05
    #print "+++ ",umax,vmax
    #umax = vmax = 50
    plot([-smax,smax],[0,0],'k')
    plot([0,0],[-smax,smax],'k')
    axis('scaled')
    axis([-smax,smax,-smax,smax])
    title('Velocities at gauge %s' % gaugeno)
    xlabel('u in cm/sec')
    ylabel('v in cm/sec')

    figure(102)
    clf()
    plot(t,u,'--b',linewidth=2)
    plot(t,v,'--g',linewidth=2)
    legend(['u','v'],'upper left')
    
    eta = gh - gh[0]
    speed = sqrt(u**2 + v**2)
    if 0:
        plot(t,speed,'r')
        legend(['u','v','speed'],'upper left')
    if 0:
        plot(t,eta)
        legend(['u','v','speed','eta'],'upper left')
        
    n = int(floor(t.max()/1800.)) + 2
    xticks([1800*i for i in range(n)],[str(0.5*i) for i in range(n)])
    xlim(t.min(),t.max())
    ylabel('Velocities in cm/sec')
    xlabel('Hours post-quake')
    title('Velocities at gauge %s' % gaugeno)

    figure(13)
    plot(u,v,'r')

    #figure(14)
    # need to adjust t!
    #tquake = time.time(
    #plot(t/3600.,100*speed,'r')

    return t,speed,u,v,eta

    
def plot_depths_and_detide(HAIdir):


    gauges = V.read_all(HAIdir)
    ng = len(gauges)
    R = np.linspace(0,1,ng)
    G = np.linspace(0,0,ng)
    B = np.linspace(1,0,ng)
    depths = gauges.keys()
    depths.sort()
    figure(11,(10,10))
    clf()
    subplot(211)
    for i in range(ng):
        g = gauges[depths[i]]
        plot(g.tdata,g.vdata[:,2],color=[R[i],G[i],B[i]])
    #xticks(rotation=20)
    #xlim([g.tdata[0] - DT.timedelta(0,12.*3600), g.tdata[-1]])
    #xlabel("Hours post-quake")
    ylabel("cm/sec", fontsize=15)
    #title("%s   %s" % (g.id,g.name))
    title("u-velocities at gauge   %s" % (g.id),fontsize=15)
    #legend([str(d) for d in depths], 'upper left')

    subplot(212)
    for i in range(ng):
        g = gauges[depths[i]]
        plot(g.tdata,g.vdata[:,3],color=[R[i],G[i],B[i]])
    #xticks(rotation=20)
    #xlim([g.tdata[0] - DT.timedelta(0,12.*3600), g.tdata[-1]])
    xlabel("Hours post-quake")
    ylabel("cm/sec", fontsize=15)
    title("v-velocities at gauge   %s" % (g.id),fontsize=15)
    #legend([str(d) for d in depths], 'upper left')
    savefig('uvdepth%s.png' % g.id)


    t,uave,vave = V.get_gauge(HAIdir)
    degree = 20
    c, t2, u2, u_tide = dart.fit_tide_poly2(t,uave,degree,-20,28,-20,28)
    c, t2, v2, v_tide = dart.fit_tide_poly2(t,vave,degree,-20,28,-20,28)

    figure(12,(10,10))
    clf()
    subplot(211)
    plot(t,uave,'b')
    plot(t2,u_tide,'k')
    ylabel("cm/sec", fontsize=15)
    title("Depth averaged u-velocity at gauge   %s" % (g.id),fontsize=15)
    subplot(212)
    plot(t,vave,'b')
    plot(t2,v_tide,'k')
    ylabel("cm/sec", fontsize=15)
    title("Depth averaged v-velocity at gauge   %s" % (g.id),fontsize=15)
    savefig('uvtide%s.png' % g.id)

