## NenuMS
Quick look plots for NenuFAR MSs: 

        ms_info_ant.py 
Quick look at an MS header, listing antenna positions in both meters and degrees (Lon, La)  and returns a plot of the used antenna distribution.  


Example of output in terminal: 
![Image description](https://github.com/tremou/Nenu/blob/master/print.png)


Example of MiniArrays/Antennas position plot:
![Image description](https://github.com/tremou/Nenu/blob/master/NENUFAR_XST_20200209_155700_20200209_162900_3C48_TRACKING_XST__SB351.ms_plotant.png)


       nenu_calib_ms.py
  Performs the following steps in a list of MSs: 
  - Flagging (auto-correlations with NDPPP and aoflagger in auto mode-no particular strategy) 
  - Gain calibration using the Lofar LBA  A-team sources skymodel (NDPPP)
  - Apply calibration (NDPPP)
  - Quick image by concatenating the MSs (WSClean) 
  
        msplot.py
  Reading the MS file and creat UV, Real vs Imag, Amp vs UVdist, Amp vs Time plots. 
  Correlation index and antenna options to plot. 
  Example of output file: 
  ![Image description](https://github.com/tremou/Nenu/blob/master/NENUFAR_XST_20200310_110200_20200310_150400_3C10_TRACKING_XST__SB282.ms_plot.png)
        
        
        
        nenuvplt.py
  Converting the MS into dask-ms xarray in order to do quick plots. 
  Not yet completed but you may use it for quick uv-plot. It has also many dependancies that I will eventually list here... 
  
  
 
