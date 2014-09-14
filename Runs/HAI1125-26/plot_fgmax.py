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
    fs = 15
    dy = -.002
    xy = [204.91802, 19.74517]
    plot([xy[0]], [xy[1]], 'wo',markersize=8)
    plot([xy[0]], [xy[1]], 'k+',markersize=8)
    if label: text(xy[0], xy[1]+dy, '1125',fontsize=fs)
    xy = [204.93003, 19.74167]
    plot([xy[0]], [xy[1]], 'wo',markersize=8)
    plot([xy[0]], [xy[1]], 'k+',markersize=8)
    if label: text(xy[0], xy[1]+dy, '1126',fontsize=fs)

fg = fgmax_tools.FGmaxGrid()
fg.read_input_data('fgmax1.txt')
fg.read_output(outdir='_americano_10sep14')

figure(1, figsize=(10,7))

bounds = [0,.25,.5,.75,1,2,3,4]
cmap = mpl.colors.ListedColormap([[1,1,1],[.8,.8,1],[.5,.5,1],[0,0,1],\
                 [1,.7,.7], [1,.4,.4], [1,0,0]])
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
gca().set_aspect(1./cos(fg.Y.mean()*pi/180.))
xlim(204.905,204.95)
ylim(19.715,19.7538)
add_gauges(False)
show()

# Plot gauges and topo:

bounds = [-1e10,0,1e10]
cmap = mpl.colors.ListedColormap([[1,1,1],[0,1,0]])
figure(2, figsize=(10,7))
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
contourf(fg.X,fg.Y,fg.B,bounds,cmap=cmap,norm=norm,extend='max')
contour(fg.X,fg.Y,fg.B,[0],colors='k')
ticklabel_format(format='plain',useOffset=False)
xticks(rotation=20,fontsize=15)
yticks(fontsize=15)
gca().set_aspect(1./cos(fg.Y.mean()*pi/180.))
xlim(204.905,204.95)
ylim(19.715,19.7538)
add_gauges()
show()

if 1:
    figure(2)
    fname = 'Hilo_gauges.png'
    savefig(fname)
    print 'Created ', fname

    figure(1)
    fname = 'Hilo_smax.png'
    savefig(fname)
    print 'Created ', fname
