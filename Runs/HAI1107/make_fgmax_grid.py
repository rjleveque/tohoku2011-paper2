"""
Create fgmax_grid.txt input file
"""

#import fgmax_tools as F   # requires WAcoast/python_tools on path
from clawpack.geoclaw import fgmax_tools as F


def make_fgmax_grid1():
    FG = F.fgmax_grid_parameters()
    FG.fname = 'fgmax1.txt'
    FG.point_style = 2       # will specify a 2d grid of points
    FG.x1 = 202.08
    FG.x2 = 202.14
    FG.y1 = 21.28
    FG.y2 = 21.34
    FG.dx = 1./(3600.)    # 1 arcssecond grid
    FG.tstart_max = 7.5*3600.     # when to start monitoring max values
    FG.tend_max = 1.e10       # when to stop monitoring max values
    FG.dt_check = 30.         # target time (sec) increment between updating 
                               # max values
    FG.min_level_check = 6    # which levels to monitor max on
    FG.arrival_tol = 1.e-2    # tolerance for flagging arrival
    F.make_fgmax(FG)


if __name__ == "__main__":
    make_fgmax_grid1()


