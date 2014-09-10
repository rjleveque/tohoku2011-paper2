"""
Plot fgmax output from GeoClaw run.

"""
try:
    matplotlib  # see if it's already been imported (interactive session)
except:
    import matplotlib
    matplotlib.use('Agg')  # set to image backend


from pylab import *
import matplotlib as mpl
import os
from clawpack.geoclaw import fgmax_tools

def add_gauges(label=True):
    dy = -0.04
    fs = 12
    xy = [203.04117, 21.0033]
    plot([xy[0]], [xy[1]], 'ko',markersize=8)
    if label: text(xy[0], xy[1]+dy, '1116',fontsize=fs)
    xy = [203.30818, 21.00178]
    plot([xy[0]], [xy[1]], 'ko',markersize=8)
    if label: text(xy[0]-.07, xy[1]+dy, '1118',fontsize=fs)
    xy = [203.25283, 20.86727]
    plot([xy[0]], [xy[1]], 'ko',markersize=8)
    if label: text(xy[0]-.05, xy[1]+dy, '1119',fontsize=fs)
    xy = [203.31472, 20.86845]
    plot([xy[0]], [xy[1]], 'ko',markersize=8)
    if label: text(xy[0]-0.02, xy[1]-0.065, '1120',fontsize=fs)
    xy = [203.49188, 20.61252]
    plot([xy[0]], [xy[1]], 'ko',markersize=8)
    if label: text(xy[0], xy[1]+dy, '1121',fontsize=fs)
    xy = [203.50765, 20.76525]
    plot([xy[0]], [xy[1]], 'ko',markersize=8)
    if label: text(xy[0]-.06, xy[1]+dy, '1122',fontsize=fs)


fg = fgmax_tools.FGmaxGrid()
fg.read_input_data('fgmax1.txt')
fg.read_output()

figure(1, figsize=(11,6))

bounds = [0,.1,.2,.3,.4,.5,1]
cmap = mpl.colors.ListedColormap([[1,1,1],[.8,.8,1],[.5,.5,1],[.2,.2,1],[0,0,1],\
         [1,0,0]])

bounds = [0,.1,.2,.4,.5,0.8,1.]
cmap = mpl.colors.ListedColormap([[1,1,1],[.8,.8,1],[.5,.5,1],[.2,.2,1],\
         [1,.5,.5], [1,0,0]])
ax1 = axes()
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
contourf(fg.X,fg.Y,fg.s,bounds,cmap=cmap,norm=norm,extend='max')
cb = colorbar(extend='max')
cb.set_label('meters / sec')

contour(fg.X,fg.Y,fg.s,bounds,colors='w')
contour(fg.X,fg.Y,fg.B,[0],colors='k')

ticklabel_format(format='plain',useOffset=False)
#title('Maximum speed s')
xticks(rotation=20,fontsize=15)
yticks(fontsize=15)
ax1.set_aspect(1./cos(fg.Y.mean()*pi/180.))
xlim(fg.X.min(), fg.X.max())
ylim(fg.Y.min(), fg.Y.max())
#add_gauges(label=False)
show()

# Plot gauges and topo:

bounds = [-1e10,0,1e10]
cmap = mpl.colors.ListedColormap([[1,1,1],[0,1,0]])
figure(2, figsize=(11,6))
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
contourf(fg.X,fg.Y,fg.B,bounds,cmap=cmap,norm=norm,extend='max')
contour(fg.X,fg.Y,fg.B,[0],colors='k')
ticklabel_format(format='plain',useOffset=False)
xticks(rotation=20,fontsize=15)
yticks(fontsize=15)
ax1.set_aspect(1./cos(fg.Y.mean()*pi/180.))
xlim(fg.X.min(), fg.X.max())
ylim(fg.Y.min(), fg.Y.max())

add_gauges()

show()

if 1:
    figure(2)
    fname = 'channel_gauges.png'
    savefig(fname)
    print 'Created ', fname

    figure(1)
    fname = 'channel_smax.png'
    savefig(fname)
    print 'Created ', fname
