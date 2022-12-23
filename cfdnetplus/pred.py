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