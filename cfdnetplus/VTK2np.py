def VTK2np(path_to_main, folders, fields, mode, xres:int, yres:int, x_lim:float, y_lim:float,zcut):
    # Creates 2d images of multiple VTK meshs and saves them as one np.array
    # path_to_main is the main folder, i.e 'airfoil2d/' containing speciifed subfolder in 'folder'
    # still needs a field variable specifiying the data to get extracted

    import numpy as np
    import os
    from scipy.interpolate import griddata
    import meshio
    import re
    
    import cfdnetplus.extract2D_xy as extract2D_xy
    import cfdnetplus.extract2D_xz as extract2D_xz

    path_to_folder=[]
    for i in folders:
        path_to_folder.append(path_to_main+i+'/VTK/')

    for i in path_to_folder:
        print('processing data in '+i)
        subfolders = os.listdir(i)
        
        folder = []
        files = []
        
        if 'U' in fields:
            l=len(fields)+2
        else:
            l=len(fields)
    
        

        for j in subfolders:
            
            if os.path.isdir(i+j) == True: 
                folder.append(i+j+'/')
                files.append(i+j+'/'+'internal.vtu')
        
        x = np.arange(x_lim[0],x_lim[1], (x_lim[1]-x_lim[0])/xres)
        y = np.arange(y_lim[0],y_lim[1], (y_lim[1]-y_lim[0])/yres)
        grid_x, grid_y= np.meshgrid(x,y)

        df = np.empty((0,yres, xres,l))
        if mode == 'xy':
            for j in files:
                #print(j)
                df_t=extract2D_xy(j,fields,xres,yres,grid_x,grid_y,zcut)
                df=np.concatenate((df,df_t),axis=0)
        elif mode == 'xz':
            for j in files:
                #print(j)
                df_t=extract2D_xz(j,fields,xres,yres,grid_x,grid_y,zcut)
                df=np.concatenate((df,df_t),axis=0)
        else:
            print('please enter a valid mode like "xy" "xz".')
       
        
        print(df.shape)
        [a,b,c,d]=df.shape

        #Finding and extracting the right data to create the label dataframe
        #finding index of last simulation timestep
        idx = [j for j, item in enumerate(files) if re.search(str(a-1), item)]
        print(a)
        print(idx)

        df_label= []

        for j in range(a):
            df_label.append(df[idx,:,:,:])
        df_label=np.array(df_label)
        df_label=df_label.reshape((a,b,c,d))
        

        np.save(i+'df',df)
        np.save(i+'df_label',df_label)
        print('data written to'+i+'df')

    return path_to_folder