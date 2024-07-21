import pandas as pd
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
import keras

import cv2

ticker = 'SBER'
path_images = './DataForLearning/9.07.24/images/'

df = pd.read_csv(f'./DataFrames/{ticker}.csv')
# df.info()

def change_img(img:str):
    image = cv2.imread(f'{path_images}{img}')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = np.array(cv2.resize(image,(300,200)))
    image = image/255
    return image

x_train = df['img'].iloc[0:100].to_numpy()
x_train=np.array([change_img(xi) for xi in x_train])

x_test = df['img'].iloc[100:].to_numpy()
x_test=np.array([change_img(xi) for xi in x_test])

y_train = df['direction'].iloc[0:100].to_numpy()
y_test = df['direction'].iloc[100:].to_numpy()

y_train_cat = keras.utils.to_categorical(y_train, 3)
y_test_cat = keras.utils.to_categorical(y_test, 3)



model = keras.models.load_model('./Models/Classificator3.h5')

# model.compile(optimizer='adam',
#              loss='categorical_crossentropy',
#              metrics=['accuracy'])

# his = model.fit(x_train, y_train_cat, batch_size=5, epochs=10, validation_split=0.2)
y = model.predict(x_train)

print(y_train)
print(np.round(y,2))
print(np.argmax(y,axis=1))
# model.evaluate(x_test, y_test_cat)
# model.save('./Models/Classificator1.keras')