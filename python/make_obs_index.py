"""
Script to plot all velocity data from all gauges in directories given
by the list dirs.
"""

import os,sys,glob
import velocities as V
from gaugedirs import set_gauges

obsdir = os.path.abspath('../Observations')
gaugenos, HAIdirs, rundirs = set_gauges()


index_file = os.path.join(obsdir, 'index.html')

html = open(index_file,'w')
html.write("""
        <html>
        <body>
        <h1>Velocity plots</h1>
        <p>
        <a href="gauge_locations.png">Gauge locations</a>
        <p>
        <ul>
        """)

for gaugeno in gaugenos:
    dir = os.path.join(obsdir, HAIdirs[gaugeno])

    html.write("""
        <p>
        <li><a href="%s/plots.html">%s</a><p>
        <img src="%s/fig14.png" height=300>
        <img src="%s/fig13.png" height=300>
        """ % (dir,dir,dir,dir))
    
    subdir_index_file = os.path.join(dir,'plots.html')
    html2 = open(subdir_index_file,'w')
    html2.write("""
        <html>
        <body>
        <h1>Plots for %s</h1>
        <a href="../gauge_locations.png">Gauge locations</a>
        <p>
        <a href="%s_station_data.txt">Station data</a> ...
        <a href=".">raw data files </a>
        <hr>
        <h2>Speed at different depths:</h2>
        <p> <img src="fig10.png" width=900><p>
        <hr>
        <h2>Speed at different depths:</h2>
        <p> <img src="fig11.png" width=900><p>
        <hr>
        <h2>Average speed at all depths:</h2>
        <p> <img src="fig14.png" width=900><p>
        <hr>
        <h2> u, v at all depths:</h2>
        <p> <img src="fig18.png" width=600>
        <img src="fig12.png" width=600>
        <hr>
        <h2> u, v at all depths and average:</h2>
        <p> <img src="fig17.png" width=600><p>
        <hr>
        <h2>Average u, v at all depths:</h2>
        <p> <img src="fig16.png" width=600>
        &nbsp;&nbsp;&nbsp;
        <img src="fig13.png" width=600>
        <hr>
        <h2>Result of de-tiding:</h2>
        <p> <img src="u_detided.png" width=600>
        &nbsp;&nbsp;&nbsp;
        <img src="v_detided.png" width=600><p>
        """ % (dir,dir[:7]))
    html2.close()
    print "Created ",subdir_index_file
    
html.close()

print "Created ",index_file
            
