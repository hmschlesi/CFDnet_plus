def VTK2np(folders):
    import numpy as np
    import os
    from scipy.interpolate import griddata
    import meshio
    import re

    path_to_main= 'airfoil2d/'
    path_to_folder=[]
    for i in folders:
        path_to_folder.append(path_to_main+i+'/VTK/')

    for i in path_to_folder:
        subfolders = os.listdir(i)
        
        folder = []
        files = []
        
        for j in subfolders:
            #print(i+j)
            if os.path.isdir(i+j) == True: 
                folder.append(i+j+'/')
                files.append(i+j+'/'+'internal.vtu')
        
        x = np.arange(-50,50, 100/256)
        y = np.arange(-20,20, 40/66)

        U_list = []
        p_list = []

        for j in files:
            mesh=meshio.read(j)
            #print(j)
            points = mesh.points
            p_t=mesh.point_data['p']
            U_t=mesh.point_data['U']
            boolArr= points[:,2] == 0.05
            #print(boolArr)
            points_new=points[boolArr]
            points_new=points_new[:,[0,1]]
            p_new=p_t[boolArr]
            U_new=U_t[boolArr]
            #print(points_new.shape)
            grid_x, grid_y= np.meshgrid(x,y)
            p_grid_new = griddata(points_new, p_new, (grid_x, grid_y), method='nearest')
            U_grid_new = griddata(points_new, U_new, (grid_x, grid_y), method='nearest')
            p_list.append(p_grid_new)
            U_list.append(U_grid_new)
       
        p=np.array(p_list)
        [a,b,c]=p.shape
        print(p.shape)
        U=np.array(U_list)
        p=p.reshape(a,b,c,1)
        df=np.concatenate((U, p), axis=3)
        print(df.shape)
        [a,b,c,d]=df.shape

        #finding index of last simulation timestep
        idx = [j for j, item in enumerate(files) if re.search(str(a-1), item)]

        df_label= []

        for j in range(a):
            df_label.append(df[idx,:,:,:])
        df_label=np.array(df_label)
        df_label=df_label.reshape((a,b,c,d))
        print(df_label.shape)

        np.save(i+'df',df)
        np.save(i+'df_label',df_label)

    return path_to_folder

folder=['airFoil_30','airFoil_300','airFoil_3000']
n=VTK2np(folder)
print(n)