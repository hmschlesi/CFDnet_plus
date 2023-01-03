def pred2OF2D(mainfolder : str,fields : str, xlim:float,ylim:float):
    import numpy as np
    import os
    import meshio
    import re
    from scipy.interpolate import griddata
    from scipy import interpolate 

    from cfdnetplus.VTKlatestTime import VTKlatestTime

    main_split=mainfolder.split('/')
   

    folder_pred=mainfolder+'/pred.npy'
    pred=np.load(folder_pred)

    [a,y_steps, x_steps,layers]=pred.shape

    
    x = np.arange(xlim[0],xlim[1], (xlim[1]-xlim[0])/x_steps)
    y = np.arange(ylim[0],ylim[1], (ylim[1]-ylim[0])/y_steps)
    
    a,ts =VTKlatestTime(mainfolder)

    #path to the latest VTK mesh
    mainfolder_mesh=mainfolder+'/VTK/'+main_split[1]+'_'+str(ts)+'/internal.vtu'


    # loads the mesh and splits all relevant info into seperate variables
    mesh=meshio.read(mainfolder_mesh)

    cell_ptsid=mesh.cells_dict

    #what happens if the mesh is not only hexahedron?
    cell_ptsid=np.array(cell_ptsid['hexahedron'])

    points = mesh.points
    cell_pts=points[cell_ptsid[:,:]]
    # finds center of each cell
    centroids=np.average(cell_pts,axis=1)



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
                                    method='linear',
                                    fill_value=None,
                                    ))
                znew=np.array(znew)
                U=np.concatenate((U,znew),axis=2)
            
            #iterates through the vertices and saves the corresponding values
            string=''
            for j in range(centroids.shape[0]):
                #print(centroids[j])
                if centroids[j,0] > xlim[0] and centroids[j,0] < xlim[1] and centroids[j,1] > ylim[0] and centroids[j,1] < ylim[1]:
                    #print('in')
                    string = string +'('+ str(U[0,j,0]) + ' '+str(U[0,j,1])+ ' '+ str(U[0,j,2])+')''\n'
                else:
                    string = string +'('+str(np.array(mesh.cell_data[field])[0,j,0])+ ' '+str(np.array(mesh.cell_data[field])[0,j,1])+ ' '+str(np.array(mesh.cell_data[field])[0,j,2])+')''\n'
            # creates a complete list will all lines that need to be written in the field file
            contents[idx[0]]='internalField   nonuniform List<vector>'+'\n'+str(np.array(centroids).shape[0])+'\n'+'('+string+');'
            
        else:
            znew=[]
            znew.append( interpolate.interpn((x, y) , np.transpose(pred[:,:,:,i+2]), centroids[:,0:2],
                                    bounds_error=False,
                                    method='linear',
                                    fill_value=None,
                                    ))
            znew=np.array(znew)
            
            #iterates through the vertices and saves the corresponding values
            string=''
            for j in range(centroids.shape[0]):
                if centroids[j,0] > xlim[0] and centroids[j,0] < xlim[1] and centroids[j,1] > ylim[0] and centroids[j,1] < ylim[1]:
                    #center inside of pred-domain use pred values
                    string = string + str(znew[0,j,0]) + '\n'
                else:
                    #center outside of pred-domain use input values
                    string = string + str(np.array(mesh.cell_data[field])[0,j]) + '\n'
            
            # creates a complete list will all lines that need to be written in the field file
            contents[idx[0]]='internalField   nonuniform List<scalar>'+'\n'+str(np.array(centroids).shape[0])+'\n'+'('+string+');'
            
        with open(path2dst+'/'+field,"w") as f:
            f.writelines(contents)
        i=i+1