import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import keras
import matplotlib.pyplot as plt
from create_df_points import get_points
from sec_codes import sec_codes

model = keras.Sequential([
    keras.Input((7,)),
    keras.layers.Dense(16,activation='relu'),
    keras.layers.Dense(32,activation='relu'),
    keras.layers.Dense(16,activation='relu'),
    keras.layers.Dense(1,activation='linear')

])

model.compile(optimizer='adam',
             loss='mean_squared_error',
             metrics=['accuracy'])

model.summary()

train_codes = sec_codes[:-10]
test_codes = sec_codes[-10:]
if __name__ == '__main__':
    path_points = [
        './DataForLearning/10.07.24/points/',
        './DataForLearning/11.07.24/points/',
        './DataForLearning/12.07.24/points/']
    x_train_all,y_train_all,x_test_all,y_test_all = [],[],[],[]
    for points in path_points:
        for ticker in train_codes:
            try:
                x_tops_train,y_tops_train,x_bottoms_train,y_bottoms_train = get_points(ticker,points)
                print(ticker)
                if len(x_train_all) == 0:
                    x_train_all,y_train_all = x_tops_train,y_tops_train
                    x_train_all = np.concatenate((x_train_all,x_bottoms_train),axis=0)
                    y_train_all = np.concatenate((y_train_all,y_bottoms_train),axis=0)
                else:
                    x_train_all = np.concatenate((x_train_all,x_tops_train),axis=0)
                    x_train_all = np.concatenate((x_train_all,x_bottoms_train),axis=0)
                    y_train_all = np.concatenate((y_train_all,y_tops_train),axis=0)
                    y_train_all = np.concatenate((y_train_all,y_bottoms_train),axis=0)
            except Exception as err:
                print(err)
            for ticker in test_codes:
                try:
                    x_tops_test,y_tops_test,x_bottoms_test,y_bottoms_test = get_points(ticker,points)
                    print(ticker)
                    if len(x_test_all) == 0:
                        x_test_all,y_test_all = x_tops_test,y_tops_test
                        x_test_all = np.concatenate((x_test_all,x_bottoms_test),axis=0)
                        y_test_all = np.concatenate((y_test_all,y_bottoms_test),axis=0)
                    else:
                        x_test_all = np.concatenate((x_test_all,x_tops_test),axis=0)
                        x_test_all = np.concatenate((x_test_all,x_bottoms_test),axis=0)
                        y_test_all = np.concatenate((y_test_all,y_tops_test),axis=0)
                        y_test_all = np.concatenate((y_test_all,y_bottoms_test),axis=0)
                except Exception as err:
                    print(err)        
    # print(x_train_all.shape)
    # print(x_test_all.shape)
    # print(y_train_all.shape)
    # print(y_test_all.shape)
    history = model.fit(x_train_all, y_train_all, batch_size=8, epochs=2, validation_split=0.2)

    model.evaluate(x_test_all, y_test_all)
    # x_tt = np.array([x_test_all[0]])
    y_pred = model.predict(x_test_all[:400])
    print(x_test_all[:400].shape)
    # print(x_tt.shape)
    # print(x_tt[0])
    # print(y_p[0][0])
    # for i in range(100):
    #     x_tt = x_tt.tolist()
    #     x_tt[0] = x_tt[0][1:]
    #     x_tt[0].append(y_p[0][0])
    #     x_tt = np.array(x_tt)
    #     y_p = model.predict(x_tt)
    y_t = y_test_all[:400]
        # print(y_test_cat)
    # model.save('./Models/PointsReg1.h5')
    plt.subplot(211)
    plt.plot(y_pred)
    plt.grid(True)
    plt.subplot(212)
    plt.plot(y_t)
    plt.grid(True)

    # plt.plot(history.history['loss'])
    # plt.plot(history.history['val_loss'])
    plt.grid(True)
    plt.show()