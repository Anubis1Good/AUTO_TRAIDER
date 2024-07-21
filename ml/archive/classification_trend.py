import pandas as pd
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
import keras
import cv2
import matplotlib.pyplot as plt
from sec_codes import sec_codes
ticker = 'ABIO'
path_images = './DataForLearning/9.07.24/images/'
# df = pd.read_json('./DataFrames/ABIO.json')

# df.info()

def change_img(img:str):
    image = cv2.imread(f'{path_images}{img}')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = np.array(cv2.resize(image,(300,200)))
    image = image/255
    return image

def create_train_test(ticker):
    df = pd.read_csv(f'./DataFrames/{ticker}.csv')
    train = int(df.shape[0]*0.8)
    x_train = df['img'].iloc[0:train].to_numpy()
    x_train=np.array([change_img(xi) for xi in x_train])

    x_test = df['img'].iloc[train:].to_numpy()
    x_test=np.array([change_img(xi) for xi in x_test])

    y_train = df['direction'].iloc[0:train].to_numpy()
    y_test = df['direction'].iloc[train:].to_numpy()

    y_train_cat = keras.utils.to_categorical(y_train, 3)
    y_test_cat = keras.utils.to_categorical(y_test, 3)
    return x_train,y_train_cat,x_test,y_test_cat

# print(x_test[0].shape)

# model = keras.Sequential([
#     keras.layers.Input((60000,)),
#     keras.layers.Flatten(),
#     keras.layers.Dense(500, activation='relu'),
#     keras.layers.Dense(3,  activation='softmax')

# ])
model = keras.Sequential([
    keras.layers.Input((200,300,1)),
    keras.layers.Conv2D(32, (3,3), padding='same', activation='relu'),
    keras.layers.MaxPooling2D((2, 2), strides=2),
    keras.layers.Conv2D(64, (3,3), padding='same', activation='relu'),
    keras.layers.MaxPooling2D((2, 2), strides=2),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(3,  activation='softmax')
    # keras.layers.Flatten(),
    # keras.layers.Dense(500, activation='relu'),
    # keras.layers.Dense(3,  activation='softmax')

])

model.compile(optimizer='adam',
             loss='categorical_crossentropy',
             metrics=['accuracy'])

model.summary()

if __name__ == '__main__':
    x_train_all,y_train_cat_all,x_test_all,y_test_cat_all = [],[],[],[]
    for ticker in sec_codes:
        try:
            x_train,y_train_cat,x_test,y_test_cat = create_train_test(ticker)
            print(ticker)
            if len(x_train_all) == 0:
                 x_train_all,y_train_cat_all,x_test_all,y_test_cat_all = x_train,y_train_cat,x_test,y_test_cat
            else:
                x_train_all = np.concatenate((x_train_all,x_train),axis=0)
                y_train_cat_all = np.concatenate((y_train_cat_all,y_train_cat),axis=0)
                x_test_all = np.concatenate((x_test_all,x_test),axis=0)
                y_test_cat_all = np.concatenate((y_test_cat_all,y_test_cat),axis=0)
        except Exception as err:
            print(err)
    print(x_test_all.shape)
    history = model.fit(x_train_all, y_train_cat_all, batch_size=32, epochs=10, validation_split=0.2)

    model.evaluate(x_test_all, y_test_cat_all)
        # print(model.predict(x_test))
        # print(y_test)
        # print(y_test_cat)
    # model.save('./Models/Classificator2.h5')
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.grid(True)
    plt.show()
    # keras.saving.save_model(model,'./Models/PredictorDirection.h5')
# x = df['img'].to_numpy()
# print(x[0:1])

# cv2.imshow('test',img)
# cv2.waitKey(0)