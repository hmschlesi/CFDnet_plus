import cfdnetplus
import os
import numpy as np

mainfolder='airfoil2d/airFoil_500'
data=np.load(mainfolder+'/input.npy')
fields= ['U','p','k','omega', 'nut']
xlim =[-50,50]
ylim = [-40 , 40]
xres=256
yres=66

cfdnetplus.extractInput2d(mainfolder,fields,xlim,ylim,xres,yres,0.05)
cfdnetplus.pred(mainfolder,data,'foil3')
cfdnetplus.pred2OF2D(mainfolder,fields,xlim,ylim)
