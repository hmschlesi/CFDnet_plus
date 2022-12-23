

def newCase(folder_orig):
    import numpy as np
    import os, shutil

    if os.path.isdir(folder_orig) == False:
        print('path is not found or no folder')
        return
    #print(os.listdir(folder_orig))

    root_src_dir = folder_orig   #Path/Location of the source directory
    root_dst_dir =  folder_orig+'_pred'  #Path to the destination folder
    if os.path.isdir(root_dst_dir) == True:
        shutil.rmtree(root_dst_dir)
        print(root_dst_dir + ' was already existing and got deleted')
        

    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy(src_file, dst_dir)
    print(root_dst_dir + ' succesfully created')
    return(root_dst_dir)

def pred(mainfolder : str,data,mode :str):
    # loads a specified tf.model and tries to make a prediction for <data>
    # <data> has to be a np.array with the correct shape
    # foil model needs shape (n,66,256,6) which represent U, p, nut and nuTilda
    # prediciton gets saved as a npy array in the specified case directory
    import numpy as np
    import tensorflow as tf

    if mode == 'foil':
        modelfolder='cfdnetplus_models/model1/'
        normal=np.load(modelfolder+'normal.npy')
    elif mode == 'foil2':
        modelfolder='cfdnetplus_models/model2/'
        normal=np.load(modelfolder+'normal.npy')
    elif mode == 'foil3':
        modelfolder='cfdnetplus_models/model3/'
        normal=np.load(modelfolder+'normal.npy')    
    else:
        print('please select a valid model name for mode e.g. foil')
        return
    model = tf.keras.models.load_model(modelfolder)
    prediction=model.predict(data*1/normal)
    prediction=prediction*normal  
    np.save(mainfolder+'/pred',prediction)
    print('succesful prediction stored at '+mainfolder+'/pred'+'.npy')

def pred2OF2D(mainfolder : str,fields : str, pred_xlim:float,pred_ylim:float):
    import numpy as np
    import os
    import meshio
    import re
    from scipy.interpolate import griddata
    from scipy import interpolate 

    main_split=mainfolder.split('/')
    mainfolder_mesh=mainfolder+'/VTK/'+main_split[1]+'_0/'+'internal.vtu'

    folder_pred=mainfolder+'/pred.npy'
    pred=np.load(folder_pred)

    [a,y_steps, x_steps,layers]=pred.shape

    # loads the mesh and splits all relevant info into seperate variables
    mesh=meshio.read(mainfolder_mesh)

    cell_ptsid=mesh.cells_dict

    #what happens if the mesh is not only hexahedron?
    cell_ptsid=np.array(cell_ptsid['hexahedron'])

    points = mesh.points
    cell_pts=points[cell_ptsid[:,:]]
    # finds center of each cell
    centroids=np.average(cell_pts,axis=1)

    #export to Openfoam field files
    x = np.arange(pred_xlim[0],pred_xlim[1], (pred_xlim[1]-pred_xlim[0])/x_steps)
    y = np.arange(pred_ylim[0],pred_ylim[1], (pred_ylim[1]-pred_ylim[0])/y_steps)
    #!!!!!!!!!!ts is the last time step, here its still hardcoded in the code, needs to be dynamic!!
    ts=40

    path2folder=mainfolder+'/'+str(0)
    path2dst=mainfolder+'/'+str(ts+1)

    if os.path.isdir(path2dst)==False:
        os.mkdir(path2dst)
        print('folder '+ path2dst + ' was created')

    folders=os.listdir(path2dst)
    i=0
    for field in fields:
        print('write ' + path2dst+'/'+field)
        with open(path2folder+'/'+field,"r") as f:
            contents=f.readlines()
        idx = [j for j, item in enumerate(contents) if re.search('internalField   ', item)]
        
        if field == 'U':
            U=np.empty((1,centroids.shape[0],0))
            for it in range(3):
                
                znew=[]
                znew.append( interpolate.interpn((x, y) , np.transpose(pred[:,:,:,it]), centroids[:,0:2],
                                    bounds_error=False,
                                    method='nearest',
                                    fill_value=None,
                                    ))
                znew=np.array(znew)
                U=np.concatenate((U,znew),axis=2)
            
            #iterates through the vertices and saves the corresponding values
            string=''
            for j in range(centroids.shape[0]):
                string = string +'('+ str(U[0,j,0]) + ' '+str(U[0,j,1])+ ' '+ str(U[0,j,2])+')''\n'
            # creates a complete list will all lines that need to be written in the field file
            contents[idx[0]]='internalField   nonuniform List<vector>'+'\n'+str(np.array(centroids).shape[0])+'\n'+'('+string+');'
            
        else:
            znew=[]
            znew.append( interpolate.interpn((x, y) , np.transpose(pred[:,:,:,i+2]), centroids[:,0:2],
                                    bounds_error=False,
                                    method='nearest',
                                    fill_value=None,
                                    ))
            znew=np.array(znew)
            
            #iterates through the vertices and saves the corresponding values
            string=''
            for j in range(centroids.shape[0]):
                string = string + str(znew[0,j,0]) + '\n'
            
            # creates a complete list will all lines that need to be written in the field file
            contents[idx[0]]='internalField   nonuniform List<scalar>'+'\n'+str(np.array(centroids).shape[0])+'\n'+'('+string+');'
            
        with open(path2dst+'/'+field,"w") as f:
            f.writelines(contents)
        i=i+1

def extract2D(path2msh, fields,xres:int,yres:int,grid_x,grid_y,z_cut):
    #general extraction routine to interpolate point field data onto 2d image data
    import meshio
    import numpy as np
    from scipy.interpolate import griddata

    mesh=meshio.read(path2msh)
    points = mesh.points
    boolArr= points[:,2] == z_cut

    points_new=points[boolArr]
    points_new=points_new[:,[0,1]]

    if 'U' in fields:
        l=len(fields)+2
    else:
        l=len(fields)
    
    df = np.empty((1,yres, xres,0))
    [a,b,c,d]=df.shape

    for field in fields:
            #print(field)
            df_temp=mesh.point_data[field]
            df_temp=df_temp[boolArr]
            df_temp=griddata(points_new, df_temp, (grid_x, grid_y), method='nearest')
            df_temp=np.array(df_temp)
            #print(df_temp.shape)
            if field != 'U':
                df_temp=df_temp.reshape(a,b,c,1)
            if field == 'U':
                df_temp=df_temp.reshape(a,b,c,3)
            df=np.concatenate((df,df_temp),axis=3)
    return df

def extractInput2d(mainfolder : str, fields :str, xlim:float, ylim:float, xres:int, yres:int, ycut:float):
    import numpy as np
    import os
    from scipy.interpolate import griddata
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
    df=extract2D(path2msh,fields,xres,yres,grid_x, grid_y, ycut)
    np.save(mainfolder+'/input',df)
    print('write '+mainfolder+'/input.npy')

def VTK2np(path_to_main, folders, fields, xres:int, yres:int, x_lim:float, y_lim:float,zcut):
    # Creates 2d images of multiple VTK meshs and saves them as one np.array
    # path_to_main is the main folder, i.e 'airfoil2d/' containing speciifed subfolder in 'folder'
    # still needs a field variable specifiying the data to get extracted

    import numpy as np
    import os
    from scipy.interpolate import griddata
    import meshio
    import re

    path_to_folder=[]
    for i in folders:
        path_to_folder.append(path_to_main+i+'/VTK/')

    for i in path_to_folder:
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
        for j in files:
            print(j)
            df_t=extract2D(j,fields,xres,yres,grid_x,grid_y,zcut)
            df=np.concatenate((df,df_t),axis=0)
       
        
        print(df.shape)
        [a,b,c,d]=df.shape

        #Finding and extracting the right data to create the label dataframe
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