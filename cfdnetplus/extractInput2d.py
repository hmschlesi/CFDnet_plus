def extractInput2d(mainfolder : str, fields :str, xlim:float, ylim:float, xres:int, yres:int, ycut:float):
    #cfdnetplus extractInput2d functionS
    #extracts the field data as 2d image data of the latest timestep in the VTK folder
    import numpy as np
    import os
    from scipy.interpolate import griddata

    import cfdnetplus.extract2D_xy as extract2D_xy
    
    print(mainfolder)
    mainfolderV=mainfolder+'/VTK/'
    subfolders = os.listdir(mainfolderV)

    folder = []
    files = []

    for j in subfolders:
        #print(mainfolder+'VTK/'+j)
        if os.path.isdir(mainfolderV+j) == True: 
            print(j)
            folder.append(j)
            files.append(j+'/'+'internal.vtu')
    id=[]
    for txt in folder:
        t=txt.split('_')
        id.append(int(t[len(t)-1]))
    index_max=np.argmax(id)
    path2msh=mainfolderV+files[index_max]

    x = np.arange(xlim[0],xlim[1], (xlim[1]-xlim[0])/xres)
    y = np.arange(ylim[0],ylim[1], (ylim[1]-ylim[0])/yres)
    grid_x, grid_y= np.meshgrid(x,y)
    df=extract2D_xy(path2msh,fields,xres,yres,grid_x, grid_y, ycut)
    np.save(mainfolder+'/input',df)
    print('write '+mainfolder+'/input.npy')