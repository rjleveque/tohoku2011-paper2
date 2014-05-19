"""
Plot fgmax output from GeoClaw runs, assuming points are on a rectangular
grid.

"""

import matplotlib
matplotlib.use('Agg')

from pylab import *
from numpy import ma
import os


def make_plots(outdir='_output', plotdir='_plots'):

    # Some things that might need to change...
    fgmax_input_file = 'fgmax1.txt'

    plot_zeta = True
    plot_zeta_times = False
    plot_arrival_times = False
    plot_arrival_times_on_zeta = False
    plot_speed = True

    sea_level = 0.  # relative to MHW

    # Contour levels for zeta in filled contour plots:
    clines_zeta = [0] + list(linspace(0.4,1.1,8))
    

    # Contour levels for arrival time and time of max zeta:
    #clines_t = None  
    clines_t = linspace(0,60,7)  # minutes

    clines_t_label = clines_t[::2]  # which ones to label 
    clines_t_colors = [.5,.5,.5]    # RGB of color for contour lines
    clines_topo = [0]

    clines_speed = [0,0.25,0.5, 0.75, 1., 2, 3, 4]

    if not os.path.isdir(outdir):
        raise Exception("Missing directory: %s" % outdir)

    if not os.path.isdir(plotdir):
        os.mkdir(plotdir)

    print outdir
    print fgmax_input_file

    # read mx and my from the input file:
    try:
        fid = open(fgmax_input_file)
    except:
        raise Exception("cannot open %s" % fgmax_input_file)

    # skip some lines:
    for i in range(6):
        line = fid.readline()

    line = fid.readline().split()
    fid.close()
    mx = int(line[0])
    my = int(line[1])
    print "fgmax grid should be %s by %s with %s values" %(mx,my,mx*my)


    fname = outdir + '/fort.FG1.valuemax' 
    print "Reading %s ..." % fname
    try:
        d = loadtxt(fname)
    except:
        raise Exception("*** Cannot read file: %s" % fname)

    ncols = d.shape[1]  
    if ncols != 8:
        print "*** Unexpected number of columns in FG file: ",ncols
    ind_s = 4
    ind_tzeta = 5
    ind_ts = 6

    print "Read %s values" % d.shape[0]

    x = reshape(d[:,0],(mx,my),order='F')
    y = reshape(d[:,1],(mx,my),order='F')
    y0 = 0.5*(y.min() + y.max())   # mid-latitude for scaling plots
    eta_tilde = reshape(d[:,3],(mx,my),order='F')

    # AMR level used for each zeta value:
    level = reshape(d[:,2].astype('int'),(mx,my),order='F')
    
    # Determine topo B at each point from the same level of AMR:
    fname = outdir + '/fort.FG1.aux1' 
    print "Reading %s ..." % fname
    daux = loadtxt(fname)
    topo = []
    nlevels = daux.shape[1]
    for i in range(2,nlevels):
        topoi = reshape(daux[:,i],(mx,my),order='F')
        topoi = ma.masked_where(topoi < -1e50, topoi)
        topo.append(topoi)

    B = ma.masked_where(level==0, topo[0])  # level==0 ==> never updated
    levelmax = level.max()
    for i in range(levelmax):
        B = where(level==i+1, topo[i], B)

    h = where(eta_tilde > B, eta_tilde - B, 0.)

    # zeta = max h on land or max eta offshore:
    zeta = where(B>sea_level, h, eta_tilde)
    zeta = where(zeta > -1e20, zeta, sea_level)

    tzeta = reshape(d[:,ind_tzeta],(mx,my),order='F')  # Time maximum h recorded
    tzeta = ma.masked_where(tzeta < -1e50, tzeta)      
    tzeta = ma.masked_where(zeta == 0., tzeta) / 60.  # minutes 

    speed = reshape(d[:,ind_s],(mx,my),order='F')
    speed = ma.masked_where(zeta==0.,speed) ###  * 100. # convert to cm/sec

    inundated = logical_and((B>0), (h>0))


    # last column is arrival times:
    atimes = reshape(d[:,-1],(mx,my),order='F')
    atimes = ma.masked_where(atimes < -1e50, atimes)  
    atimes = ma.masked_where(zeta == 0., atimes) / 60.  # minutes 

    if plot_zeta:

        # Plot h or eta along with contours of topo:
        figure(101)
        clf()
        zeta = ma.masked_where(zeta==0.,zeta)
        print "max zeta = ", zeta.max()
        if clines_zeta is None:
            cmax = zeta.max()
            cmin = zeta.min()
            clines_zeta = linspace(cmin,cmax,10)
        colors = discrete_cmap(clines_zeta)
        contourf(x,y,zeta,clines_zeta,colors=colors,extend='max')

        cbar = colorbar()
        cbar.set_ticks(clines_zeta)
        cbar.set_label('meters', fontsize=15)


        # Contours of topo:
        contour(x,y,B,clines_topo,colors='k',linestyles='-')


        if plot_arrival_times_on_zeta:
            # Contours of arrival time
            cs = contour(x,y,atimes,clines_t,colors=clines_t_colors)
            clabel(cs,clines_t_label)


        ticklabel_format(format='plain',useOffset=False)
        xticks(rotation=20)
        gca().set_aspect(1./cos(y0*pi/180.))

        title("Zeta Maximum",fontsize=20)
        if plot_arrival_times_on_zeta:
            title("Zeta Maximum and arrival times",fontsize=15)
        
        add_gauges()
        fname = plotdir + '/zeta.png' 
        savefig(fname)
        print "Created ",fname



    def plot_variable(name, v, clines):
        figure(108)
        clf()

        print "max %s = %s" % (name,v.max())
        colors = discrete_cmap(clines)
        contourf(x,y,v,clines,colors=colors,extend='max')

        cbar = colorbar()
        cbar.set_ticks(clines)
        #cbar.set_label('meters', fontsize=15)


        # Contours of topo:
        contour(x,y,B,clines_topo,colors='k',linestyles='-')

        ticklabel_format(format='plain',useOffset=False)
        xticks(rotation=20)
        gca().set_aspect(1./cos(y0*pi/180.))

        title("Maximum %s" % name,fontsize=20)
        
        add_gauges()
        fname = plotdir + '/%s.png' % name
        savefig(fname)
        print "Created ",fname


    if plot_speed:
        plot_variable('speed',speed,clines_speed)


def discrete_cmap(clines):
    """
    Construct a discrete color map for the regions between the contour lines
    given in clines. Colors go from turqouise through yellow to red.
    """
    nlines = len(clines)
    n1 = int(floor((nlines-1)/2.))
    n2 = nlines - 1 - n1
    Green = hstack([linspace(1,1,n1),linspace(1,0,n2)])
    Red = hstack([linspace(0,0.8,n1), ones(n2)])
    Blue = hstack([linspace(1,0.2,n1), zeros(n2)])
    colors = zip(Red,Green,Blue)
    return colors

def discrete_cmap_times(clines):
    """
    Construct a discrete color map for the regions between the contour lines
    given in clines. For arrival times, colors go from red to turquoise.
    """
    nlines = len(clines)
    n1 = int(floor((nlines-1)/2.))
    n2 = nlines - 1 - n1
    Green = flipud(hstack([linspace(1,1,n1),linspace(1,0,n2)]))
    Red = flipud(hstack([linspace(0,0.8,n1), ones(n2)]))
    Blue = flipud(hstack([linspace(1,0.2,n1), zeros(n2)]))
    colors = zip(Red,Green,Blue)
    return colors

def add_gauges():
    plot([203.52825],[20.9021333],'ko',markersize=8)
    text(203.529,20.9023,'1123',fontsize=15)
    #plot([203.52333],[20.895],'ko',markersize=8)
    #text(203.524,20.8951,'TG',fontsize=15)
    # more accurate location from Yong Wei:
    plot([203.530944],[20.895],'ko',markersize=8)
    text(203.5293,20.8951,'TG',fontsize=15)

if __name__ == "__main__":
    make_plots('_americano_25apr14')
