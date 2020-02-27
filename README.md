# NenuMS
Quick look plots for NenuFAR MSs: 

    ms_info_ant.py 
Quick look at an MS header, listing antenna positions in both meters and degrees (Lon, La)  and returns a plot of the used antenna distribution.  


Example of output in terminal: 
![Image description](https://github.com/tremou/Nenu/blob/master/print.png)


Example of MiniArrays/Antennas position plot:
![Image description](https://github.com/tremou/Nenu/blob/master/NENUFAR_XST_20200209_155700_20200209_162900_3C48_TRACKING_XST__SB351.ms_plotant.png)


    nenu_calibms.py
  Performs the following steps in a list of MSs: 
  - Flagging (auto-correlations with NDPPP and aoflagger in auto mode-no particular strategy) 
  - Gain calibration using the Lofar LBA  A-team sources skymodel (NDPPP)
  - Apply calibration (NDPPP)
  - Quick image by concatenating the MSs (WSClean) 
  
