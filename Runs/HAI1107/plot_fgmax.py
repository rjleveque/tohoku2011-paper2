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
    plot([202.12623],[21.29147],'ko',markersize=8)
    if label: text(202.125,21.2885,'1107',fontsize=15)
    plot([202.1333333],[21.30666667],'ko',markersize=8)
    if label: text(202.130,21.306,'TG',fontsize=15)
    plot([202.1035], [21.302],'ko',markersize=8)
    if label: text(202.102,21.299,'S1',fontsize=15)
    plot([202.135], [21.288],'ko',markersize=8)
    if label: text(202.136,21.286,'KN',fontsize=15)


fg = fgmax_tools.FGmaxGrid()
fg.read_input_data('fgmax1.txt')
fg.read_output(outdir='_americano_1sep14')

figure(1, figsize=(10,7))

bounds = [0,.25,.5,.75,1,2,3,4]
cmap = mpl.colors.ListedColormap([[1,1,1],[.8,.8,1],[.5,.5,1],[0,0,1],\
                 [1,.7,.7], [1,.4,.4], [1,0,0]])
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
ylim(21.28,21.3313)

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
ylim(21.28,21.3313)

add_gauges()

show()
if 1:
    figure(2)
    fname = 'Hon_gauges.png'
    savefig(fname)
    print 'Created ', fname

    figure(1)
    fname = 'Hon_smax.png'
    savefig(fname)
    print 'Created ', fname
