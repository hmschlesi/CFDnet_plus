import cfdnetplus.extract2D as extract2D
import numpy as np
from scipy.interpolate import griddata
from cfdnetplus.VTKlatestTime import VTKlatestTime


mainfolder='airfoil2d/airFoil_500'
data=np.load(mainfolder+'/input.npy')
fields= ['U','p','k','omega', 'nut']
xlim =[-50,50]
ylim = [-40 , 40]
xres=256
yres=66

a,b =VTKlatestTime(mainfolder)


print(b)