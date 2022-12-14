del CFDnet_plus
import CFDnet_plus
import os
import numpy as np

mainfolder='airfoil2d/airFoil_400'
data=np.load(mainfolder+'/input.npy')
fields= ['U','p','nut','nuTilda']
xlim =[-50,50]
ylim = [-20 , 20]
xres=256
yres=66

test_path2msh='airfoil2d/airFoil_400/VTK/airFoil_400_20/internal.vtu'
x = np.arange(xlim[0],xlim[1], (xlim[1]-xlim[0])/xres)
y = np.arange(ylim[0],ylim[1], (ylim[1]-ylim[0])/yres)
grid_x, grid_y= np.meshgrid(x,y)

CFDnet_plus.pred(mainfolder,data,'foil')
CFDnet_plus.pred2OF2D(mainfolder,fields,xlim,ylim)
df=CFDnet_plus.extract2D(test_path2msh,fields,xres,yres,grid_x, grid_y, 0.05)
CFDnet_plus.extractInput2d(mainfolder,fields,xlim,ylim,xres,yres,0.05)

print(df.shape)

n=VTK2np(folder)
os.listdir('airfoil2d/airFoil_30')
#newFolder=newCase('airfoil2d/airFoil_400')
print(data.shape)