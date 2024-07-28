import os
import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
import numpy as np
import pandas as pd 
from sec_codes import sec_codes
i = 14
ticker = sec_codes[i]
print(ticker)
path_bars = f'./Data/TQBR.{ticker}_T1.txt'
df = pd.read_csv(path_bars,sep='\t')
# print(df.head())
df.drop(['datetime','open','close'],axis=1,inplace=True)
k_norm = df.max().to_numpy()


def xy_generator(df:pd.DataFrame):
    for step in range(df.shape[0]-50):
        X = df.iloc[step:step+50].to_numpy()/k_norm
        Y = df.iloc[step+50].to_numpy()/k_norm
        X = torch.tensor(X, dtype=torch.float32)
        Y = torch.tensor(Y, dtype=torch.float32)
        X = X.flatten()
        # print(X.shape)
        # print(Y.shape)
        yield X,Y
    return


# Генерация случайных данных
X = np.random.rand(1000, 5)  # 1000 образцов, 5 признаков
Y = np.random.rand(1000, 3)  # 1000 образцов, 3 целевых значения (регрессия)

# Преобразуем данные в тензоры PyTorch
X = torch.tensor(X, dtype=torch.float32)
Y = torch.tensor(Y, dtype=torch.float32)

# Определение датасета и загрузчика данных
dataset = data.TensorDataset(X, Y)
data_loader = data.DataLoader(dataset, batch_size=32, shuffle=True)

# Определение нейронной сети
class RegressionModel(nn.Module):
    def __init__(self):
        super(RegressionModel, self).__init__()
        self.fc1 = nn.Linear(150, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, 3)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x
    def save(self, file_name='LR_model.pth'):
        model_folder_path = './Models'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)

# Создание модели
model = RegressionModel()
model.load_state_dict(torch.load('./Models/LR_model.pth'))
# Определение функции потерь и оптимизатора
criterion = nn.MSELoss()  # MSE (Mean Squared Error) для регрессии
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Обучение модели
num_epochs = 10
for epoch in range(num_epochs):
    for batch_x, batch_y in xy_generator(df):
        # Прямой проход
        outputs = model(batch_x)
        loss = criterion(outputs, batch_y)

        # Обратный проход и оптимизация
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item()}')
    # Печать состояния обучения
    # if (epoch+1) % 10 == 0:
model.save()
# Пример предсказания на новых данных
gen = xy_generator(df)
X,Y = next(gen)
# new_data = torch.tensor([[0.5, 0.2, 0.3, 0.1, 0.4]], dtype=torch.float32)
prediction = model(X)
print(ticker)
print(f'Prediction: {prediction.detach().numpy()*k_norm}')
print(Y*k_norm)
