def VTKlatestTime(mainfolder):
    import os
    import numpy as np

    #print(mainfolder)
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

    return path2msh, id[index_max]