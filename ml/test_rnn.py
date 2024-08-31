import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

import matplotlib.pyplot as plt
# Определение модели LSTM для предсказания следующей точки
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_layers=1):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])  # Используем последний выход LSTM
        return out

# Генерация синтетических данных (например, движения по синусоиде)
def generate_data(seq_length, num_sequences):
    data = []
    for _ in range(num_sequences):
        x = np.linspace(0, np.pi * 4, seq_length)
        y = np.sin(x) + np.random.normal(0, 0.1, seq_length)
        sequence = np.stack((x, y), axis=1)
        data.append(sequence)
    return np.array(data)

# Подготовка данных
seq_length = 50  # Длина последовательности
num_sequences = 1000  # Количество последовательностей
data = generate_data(seq_length, num_sequences)
print(data)
print(data.shape)
X = data[:, :-1, :]  # Все точки последовательности, кроме последней
y = data[:, -1, :]   # Последняя точка последовательности

# Преобразование данных в тензоры PyTorch
X = torch.tensor(X, dtype=torch.float32)
y = torch.tensor(y, dtype=torch.float32)

# Параметры модели
input_size = 2  # x и y координаты
hidden_size = 50
output_size = 2  # x и y координаты следующей точки
num_layers = 2
learning_rate = 0.001
num_epochs = 100

# Инициализация модели, функции потерь и оптимизатора
model = LSTMModel(input_size, hidden_size, output_size, num_layers)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Обучение модели
for epoch in range(num_epochs):
    model.train()
    outputs = model(X)
    optimizer.zero_grad()
    loss = criterion(outputs, y)
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

# Пример предсказания
model.eval()
with torch.no_grad():
    test_input = X[0].unsqueeze(0)  # Берем первую последовательность из данных для теста
    predicted = model(test_input)
    print(f'Настоящая точка: {y[0].numpy()}, Предсказанная точка: {predicted.numpy()}')

     # Отрисовка
    plt.figure(figsize=(10, 5))
    plt.plot(X[0][:, 0], X[0][:, 1], label='История (предыдущие точки)', marker='o', color='blue')
    plt.plot(y[0][0].item(), y[0][1].item(), label='Реальная следующая точка', marker='o', color='green', markersize=10)
    plt.plot(predicted[0][0].item(), predicted[0][1].item(), label='Предсказанная следующая точка', marker='x', color='red', markersize=10)
    plt.legend()
    plt.title('Предсказание следующей точки на основе предыдущих')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.show()