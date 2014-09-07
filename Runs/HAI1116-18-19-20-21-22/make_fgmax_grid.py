"""
Create fgmax_grid.txt input file
"""

#import fgmax_tools as F   # requires WAcoast/python_tools on path
from clawpack.geoclaw import fgmax_tools as F


def make_fgmax_grid1():
    FG = F.fgmax_grid_parameters()
    FG.fname = 'fgmax1.txt'
    FG.point_style = 2       # will specify a 2d grid of points
    FG.x1 = 202.6
    FG.x2 = 204.2
    FG.y1 = 20.4
    FG.y2 = 21.4
    FG.dx = 1./(240.)    # 15 arcssecond grid
    FG.tstart_max =  6.5*3600.     # when to start monitoring max values
    FG.tend_max = 1.e10       # when to stop monitoring max values
    FG.dt_check = 15.         # target time (sec) increment between updating 
                               # max values
    FG.min_level_check = 5    # which levels to monitor max on
    FG.arrival_tol = 1.e-2    # tolerance for flagging arrival
    F.make_fgmax(FG)


if __name__ == "__main__":
    make_fgmax_grid1()


