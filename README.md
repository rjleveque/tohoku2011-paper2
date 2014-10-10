

Code and data repository for the paper "Validating Velocities in the GeoClaw
Tsunami Model using Observations Near Hawaii from the 2011 Tohoku Tsunami"
by M. E. M. Arcos and R. J. LeVeque.

Topography and earthquake source data (topo and dtopo files) can be found in
a tar file posted at
http://faculty.washington.edu/rjl/pubs/tohoku2/index.html

Below is a summary of the contents of this repository and
instructions to recreate figures in paper.

Observations:
-------------

  - The observation data is stored in subdirectory `Observations`, with further
    subdirectories for each gauge, e.g. `HAI1107_Hon_Harbor`.  

  - Each subdirectory contains files 
      - HAIxxxx_station_data.txt:  Metadata about the station
      - depth_xxx.xxm.txt: the raw data at each depth
      - detided_harmonic.txt:   Data detided using harmonic constituents

            with columns 
                t, u, v
            where t is in hours 
                  u, v are detided versions of the depth-averaged velocities

      - detided_poly.txt:   Data detided using polynomial fit, same format
      - u_detided.png, v_detided.png: comparison of harmonic vs. poly fits
      - figXX.png:  Other figures illustrating the data.
      - plots.html: A file to display all plots for this station.

  - The file Observations/index.html facilitates viewing all the plots
    from all stations.

To recreate these plots:
------------------------

The directory *python* contains Python scripts and modules to detide the
data and make the plots:

    ```
    python make_obs_plots.py     # make the figures of observation data
								 # creates Figures/uv_depth*.png
    python make_obs_index.py     # make the plots.html and index.html files
    python detide_compare.py     # detide via harmonic and polynomial fits
								 # creates Figures/uv_tide*.png
    ```

    
To run the simulations
----------------------

Install Clawpack and insure that you have a suitable version.
    http://www.clawpack.org/installing.html

Final runs were verified using Clawpack 5.2.1.
(Earlier versions give essentially identical results, but some of the
routines for making and plotting fgmax grids showing max speed do not exist
in earlier versions).



In each of the directories `Runs/HAI*` do the following:

```       
    python make_fgmax_grid.py
    make .exe     # Makefile is set to compile with OpenMP flags 
    make .output   # will run for several hours
	python plot_fgmax.py  # to make spatial plots of maximum velocity recorded
                          # and save to Figures subdirectory
```       

Then postprocess the results:

In directory `python`:

```       
    python plot_TG_1612340.py  # will create Figures/TG_1612340_compare.png
    python plot_TG_1615680.py  # will create Figures/TG_1615680_compare.png
    python plot_TG_1617760.py  # will create Figures/TG_1617760_compare.png

    python make_geoclaw_gauge_plots.py  # will create Figures/figure*.png 
	python HAI1107_compare_gauges.py   # will create plots comparing HAI1107 and S1
                                       # Figures/HAI1107compare*.png

```       


