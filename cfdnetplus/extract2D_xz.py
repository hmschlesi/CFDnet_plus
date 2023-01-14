def extract2D_xz(path2msh, fields,xres:int,zres:int,grid_x,grid_z,ycut):
    #general extraction routine to interpolate point field data onto 2d image data
    import meshio
    import numpy as np
    from scipy.interpolate import griddata

    mesh=meshio.read(path2msh)
    points = mesh.points
    boolArr= points[:,1] >= ycut

    points_new=points[boolArr]
    points_new=points_new[:,[0,2]]

    if 'U' in fields:
        l=len(fields)+2
    else:
        l=len(fields)
    
    df = np.empty((1,zres, xres,0))
    [a,b,c,d]=df.shape

    for field in fields:
            #print(field)
            df_temp=mesh.point_data[field]
            df_temp=df_temp[boolArr]
            df_temp=griddata(points_new, df_temp, (grid_x, grid_z), method='nearest')
            df_temp=np.array(df_temp)
            #print(df_temp.shape)
            if field != 'U':
                df_temp=df_temp.reshape(a,b,c,1)
            if field == 'U':
                df_temp=df_temp.reshape(a,b,c,3)
            df=np.concatenate((df,df_temp),axis=3)
    return df