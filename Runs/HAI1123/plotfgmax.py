
import matplotlib
matplotlib.use('Agg')

from pylab import *
from numpy import ma
from pyclaw.plotters import colormaps

outdir = '_output_americano'
print "Plotting from ",outdir

plot_time_hmax = False
plot_speed = True
plot_momentum = False
plot_momentum_flux = False
plot_enstrophy = False

fname = outdir + '/setfixedgrids2.data'
try:
    fid = open(fname)
except:
    raise Exception("cannot open %s" % fname)

for i in range(7):
    line = fid.readline()
line = fid.readline().split()
fid.close()
mx = int(line[1])
my = int(line[2])

ifg = 1

fname = outdir + '/fort.FG%s.valuemax' % ifg
d = loadtxt(fname)
if d.shape[1] == 11:
    print "No enstrophy found"
    x = reshape(d[:,0],(my,mx))
    y = reshape(d[:,1],(my,mx))
    level = [int(i) for i in d[:,2]]
    level = reshape(level,(my,mx))
    h = reshape(d[:,3],(my,mx))
    s = reshape(d[:,4],(my,mx))
    hs = reshape(d[:,5],(my,mx))
    hss = reshape(d[:,6],(my,mx))
    th = reshape(d[:,7],(my,mx))
    ts = reshape(d[:,8],(my,mx))
    ths = reshape(d[:,9],(my,mx))
    thss = reshape(d[:,10],(my,mx))
    enstrophy = False
elif d.shape[1] == 13:
    print "Enstrophy found"
    x = reshape(d[:,0],(my,mx))
    y = reshape(d[:,1],(my,mx))
    level = [int(i) for i in d[:,2]]
    level = reshape(level,(my,mx))
    h = reshape(d[:,3],(my,mx))
    s = reshape(d[:,4],(my,mx))
    hs = reshape(d[:,5],(my,mx))
    hss = reshape(d[:,6],(my,mx))
    enstr = reshape(d[:,7],(my,mx))
    th = reshape(d[:,8],(my,mx))
    ts = reshape(d[:,9],(my,mx))
    ths = reshape(d[:,10],(my,mx))
    thss = reshape(d[:,11],(my,mx))
    tenstr = reshape(d[:,12],(my,mx))
    enstrophy = True
elif d.shape[1] == 12:
    print "Arrival times found"
    x = reshape(d[:,0],(my,mx))
    y = reshape(d[:,1],(my,mx))
    level = [int(i) for i in d[:,2]]
    level = reshape(level,(my,mx))
    h = reshape(d[:,3],(my,mx))
    s = reshape(d[:,4],(my,mx))
    hs = reshape(d[:,5],(my,mx))
    hss = reshape(d[:,6],(my,mx))
    th = reshape(d[:,7],(my,mx))
    ts = reshape(d[:,8],(my,mx))
    ths = reshape(d[:,9],(my,mx))
    thss = reshape(d[:,10],(my,mx))
    arrival_times = reshape(d[:,11],(my,mx))
    enstrophy = False
else:
    raise Exception("Oops... wrong number of columns")

# Mask areas where there's no data, indicated by FG_NOTSET = -0.99e98
h = ma.masked_where(h < -1e50, h)
s = ma.masked_where(s < -1e50, s)
hs = ma.masked_where(hs < -1e50, hs)
hss = ma.masked_where(hss < -1e50, hss)

th = ma.masked_where(th < -1e50, th)
ts = ma.masked_where(ts < -1e50, ts)
ths = ma.masked_where(ths < -1e50, ths)
thss = ma.masked_where(thss < -1e50, thss)

#import pdb; pdb.set_trace()

fname = outdir + '/fort.FG%s.aux1' % ifg
#fname = '_output_B0/fort.FG1.aux1'
d = loadtxt(fname)
topo = []
for i in range(2,9):
    topoi = reshape(d[:,i],(my,mx))
    topoi = ma.masked_where(topoi < -1e50, topoi)
    topo.append(topoi)

B = ma.masked_where(level==0, topo[0])  # level==0 ==> never updated
levelmax = level.max()
for i in range(levelmax):
    B = where(level==i+1, topo[i], B)

eta = h + B
eta = ma.masked_where(eta < -1e50, eta)

B = where(B>-1e50, B, 1000)

def levelcontour():
    # show where different levels of AMR are used.
    contour(x,y,level,[0.5,1.5,2.5,3.5],colors='r')

def addB():
    #contour(x,y,B,linspace(-20,20,41),colors='k')
    #contour(x,y,B,linspace(0,20,21),colors='k')
    contour(x,y,B,[0],colors='r')
    #contour(x,y,B,[-2],colors='r')

def add_gauges():
    plot([203.52825],[20.9021333],'ko',markersize=8)
    text(203.529,20.9023,'1123',fontsize=15)
    #plot([203.52333],[20.895],'ko',markersize=8)
    #text(203.524,20.8951,'TG',fontsize=15)
    # more accurate location from Yong Wei:
    plot([203.530944],[20.895],'ko',markersize=8)
    text(203.5293,20.8951,'TG',fontsize=15)

figure(60+ifg)
clf()
addB()

if 0:
    pcolor(x,y,eta)
    clim(-2,4)
    colorbar()

dry_tol = .01
h_inundated = ma.masked_where(B<0, h) 
h_inundated = ma.masked_where(h <= dry_tol, h_inundated) 
#pcolor(x,y,h_inundated)
eta_masked = ma.masked_where(B>0, eta)
pcolor(x,y,eta_masked)
clim(0,1.)
colorbar()
gca().set_aspect(1./(cos(21*pi/180.)))
ticklabel_format(format='plain',useOffset=False)
xticks(rotation=20)

# for diff'ing with old:
h0 = where(h_inundated.mask, 0., h_inundated)

s_inundated = ma.masked_where(B<0, s) 
s_inundated = ma.masked_where(h <= dry_tol, s_inundated) 
s_wet = ma.masked_where(h <= dry_tol, s) 
hs_inundated = ma.masked_where(B<0, hs) 
hs_inundated = ma.masked_where(h <= dry_tol, hs_inundated) 
title('Maximum flow depth h')
xlim(x.min(),x.max())
ylim(y.min(),y.max())

if plot_time_hmax:
    figure(68)
    clf()
    th_inundated = 0.*h_inundated + th
    pcolor(x,y,th_inundated)
    colorbar()
    gca().set_aspect(1./(cos(21*pi/180.)))
    ticklabel_format(format='plain',useOffset=False)
    xticks(rotation=20)
    addB()
    title('time of maximum h')
    xlim(x.min(),x.max())
    ylim(y.min(),y.max())

if plot_momentum:
    # Plot the maximum momentum in the inundated region
    hs_inundated = ma.masked_where(B<0, hs) 
    hs_inundated = ma.masked_where(h <= dry_tol, hs_inundated) 
    
    figure(70)
    clf()
    pcolor(x,y,hs_inundated)
    clim(0,2)
    colorbar()
    gca().set_aspect(1./(cos(21*pi/180.)))
    ticklabel_format(format='plain',useOffset=False)
    xticks(rotation=20)
    xticks(rotation=20)
    addB()
    title('Maximum momentum hs')
    xlim(x.min(),x.max())
    ylim(y.min(),y.max())
    
if plot_speed:
    # Plot the speed in the region where it's ever wet.
    figure(71,(12,9))
    clf()
    ax1 = axes()
    s_wet = ma.masked_where(h <= dry_tol, s) 

    if 1:
        bounds = [0,1,2,3,4,5,6]
        cmap = mpl.colors.ListedColormap([[1,1,1],[.8,.8,1],[.5,.5,1],[.2,.2,1],[0,0,1],\
                 [1,.7,.7], [1,.4,.4], [1,0,0]])
        ax1 = axes()
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        contourf(x,y,s_wet,bounds,cmap=cmap,norm=norm)
        cax,kw = mpl.colorbar.make_axes(gca(), shrink=0.8) 
        cb2 = mpl.colorbar.ColorbarBase(cax,cmap=cmap,norm=norm,boundaries=bounds)
        show()
        axes(ax1)
        contour(x,y,s_wet,bounds,colors='w')
        contour(x,y,B,[0],colors='k')

    ticklabel_format(format='plain',useOffset=False)
    title('Maximum speed s')
    xticks(rotation=20,fontsize=15)
    yticks(fontsize=15)
    ax1.set_aspect(1./cos(21*pi/180.))
    xlim(x.min(),x.max())
    ylim(y.min(),y.max())
    
    # Alternatively could plot only in inundated region with this...
    s_inundated = ma.masked_where(B<0, s) 
    s_inundated = ma.masked_where(h <= dry_tol, s_inundated) 

if 1:
    # Plot eta with contourf
    figure(81,(12,9))
    clf()
    ax1 = axes()
    eta_wet = ma.masked_where(h <= dry_tol, eta) 

    if 1:
        #bounds = [0,.4,.5,.6,.7,.8,.9,1,1.1]
        bounds = [1,1.25,1.5,1.75,2,2.25,2.5,2.75,3]
        cmap = mpl.colors.ListedColormap([[1,1,1],[.8,.8,1],[.5,.5,1],[.2,.2,1],[0,0,1],\
                 [1,.7,.7], [1,.4,.4], [1,0,0]])
        ax1 = axes()
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        contourf(x,y,eta_wet,bounds,cmap=cmap,norm=norm)
        cax,kw = mpl.colorbar.make_axes(gca(), shrink=0.8) 
        cb2 = mpl.colorbar.ColorbarBase(cax,cmap=cmap,norm=norm,boundaries=bounds)
        show()
        axes(ax1)
        contour(x,y,eta_wet,bounds,colors='w')
        contour(x,y,B,[0],colors='k')

    ticklabel_format(format='plain',useOffset=False)
    title('Maximum surface elevation')
    xticks(rotation=20,fontsize=15)
    yticks(fontsize=15)
    ax1.set_aspect(1./cos(21*pi/180.))
    xlim(x.min(),x.max())
    ylim(y.min(),y.max())

if 1:
    figure(77,(10,9))
    clf()
    ax1 = axes()
    contourf(x,y,B,[0,10000],colors='#55ff66')
    contour(x,y,B,[0],colors='k')
    add_gauges()

    ticklabel_format(format='plain',useOffset=False)
    xticks(rotation=20,fontsize=15)
    yticks(fontsize=15)
    ax1.set_aspect(1./cos(21*pi/180.))
    xlim(x.min(),x.max())
    ylim(y.min(),y.max())
    title("Gauge locations")


if 1:
    # contours of bathymetry
    figure(78,(10,9))
    clf()
    ax1 = axes()
    contourf(x,y,B,[0,10000],colors='#55ff66')
    contour(x,y,B,linspace(0,-10,6),colors='k',linestyles='-')
    contour(x,y,B,linspace(-15,-50,8),colors='k',linestyles='-')

    ticklabel_format(format='plain',useOffset=False)
    xticks(rotation=20,fontsize=15)
    yticks(fontsize=15)
    ax1.set_aspect(1./cos(21*pi/180.))
    xlim(x.min(),x.max())
    ylim(y.min(),y.max())
    title("Contours of bathymetry")



if plot_momentum_flux:
    # Plot the maximum momentum flux in the inundated region
    hss_inundated = ma.masked_where(B<0, hss) 
    hss_inundated = ma.masked_where(h <= dry_tol, hss_inundated) 
    
    figure(72)
    clf()
    addB()
    pcolor(x,y,hss_inundated)
    clim(0,2)
    colorbar()
    gca().set_aspect(1./(cos(21*pi/180.)))
    ticklabel_format(format='plain',useOffset=False)
    xticks(rotation=20)
    xticks(rotation=20)
    title('Maximum momentum flux hss')
    xlim(x.min(),x.max())
    ylim(y.min(),y.max())
    

if plot_enstrophy and enstrophy:
    enstr = ma.masked_where(enstr < -1e50, hss)
    tenstr = ma.masked_where(tenstr < -1e50, thss)

    # Plot the enstrophy in the region where it's ever wet.
    figure(73)
    clf()
    #subplot(2,2,4)
    addB()
    enstr_wet = ma.masked_where(h <= dry_tol, enstr) 
    pcolor(x,y,enstr_wet)
    clim(0,50)
    colorbar()
    gca().set_aspect(1./(cos(21*pi/180.)))
    ticklabel_format(format='plain',useOffset=False)
    xticks(rotation=20)
    title('Maximum enstrophy')
    xlim(x.min(),x.max())
    ylim(y.min(),y.max())


if 1:
    figure(77); savefig('KahuGauges.png')
    figure(78); savefig('KahuBathy.png')
    figure(71); savefig('KahuMaxs.png')
    figure(81); savefig('KahuMaxEta.png')
