del CFDnet_plus
import CFDnet_plus
import os
import numpy as np

mainfolder='airfoil2d/airFoil_500'
data=np.load(mainfolder+'/input.npy')
fields= ['U','p','k','omega', 'nut']
xlim =[-50,50]
ylim = [-20 , 20]
xres=256
yres=66

test_path2msh='airfoil2d/airFoil_400/VTK/airFoil_400_20/internal.vtu'
x = np.arange(xlim[0],xlim[1], (xlim[1]-xlim[0])/xres)
y = np.arange(ylim[0],ylim[1], (ylim[1]-ylim[0])/yres)
grid_x, grid_y= np.meshgrid(x,y)

#creating new dataset
main='airfoil2d/'
folders=['airFoil_1000', 'airFoil_30', 'airFoil_300', 'airFoil_3000']
folders=['airFoil_1000']
os.listdir(main)
CFDnet_plus.VTK2np(main,folders, fields, xres,yres,xlim,ylim,0.05)

df = np.empty((0,yres, xres,7))
pth2msh1='airfoil2d/airFoil_1000/VTK/airFoil_1000_11/internal.vtu'
df1=CFDnet_plus.extract2D( pth2msh1,fields,xres,yres,grid_x,grid_y,0.05)
pth2msh2='airfoil2d/airFoil_1000/VTK/airFoil_1000_20/internal.vtu'
df2=CFDnet_plus.extract2D( pth2msh2,fields,xres,yres,grid_x,grid_y,0.05)
print(df1.shape)
df=np.concatenate((df,df2),axis=0)
print(df.shape)

if 'U'  in fields:
    print(len(fields))

CFDnet_plus.pred(mainfolder,data,'foil2')
CFDnet_plus.pred2OF2D(mainfolder,fields,xlim,ylim)
df=CFDnet_plus.extract2D(test_path2msh,fields,xres,yres,grid_x, grid_y, 0.05)
CFDnet_plus.extractInput2d(mainfolder,fields,xlim,ylim,xres,yres,0.05)

print(df.shape)

n=VTK2np(folder)
os.listdir('airfoil2d/airFoil_30')
#newFolder=newCase('airfoil2d/airFoil_400')
print(data.shape)