import pandas as pd
import numpy as np

# Загрузка данных
data = pd.read_csv('data.csv')

# Создание технических индикаторов
data['SMA_30'] = data['Close'].rolling(window=30).mean()
data['RSI'] = calculate_rsi(data)  # Используйте функцию из предыдущего примера
data['MACD'], data['Signal_Line'] = calculate_macd(data)  # Используйте функцию из предыдущего примера

# Создание признаков и меток
data['Price_Change'] = data['Close'].shift(-1) - data['Close']
data['Label'] = np.where(data['Price_Change'] > 0, 1, 0)  # 1 для роста, 0 для падения

# Удаление пропусков
data.dropna(inplace=True)

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Выбор признаков и меток
features = ['SMA_30', 'RSI', 'MACD', 'Volume']
X = data[features]
y = data['Label']

# Разделение данных
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Обучение модели
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Оценка модели
y_pred = model.predict(X_test)
print(f'Accuracy: {accuracy_score(y_test, y_pred)}')
print(classification_report(y_test, y_pred))

# Прогнозирование на новых данных
new_data = pd.read_csv('new_data.csv')
new_data['SMA_30'] = new_data['Close'].rolling(window=30).mean()
new_data['RSI'] = calculate_rsi(new_data)
new_data['MACD'], new_data['Signal_Line'] = calculate_macd(new_data)
new_data.dropna(inplace=True)

X_new = new_data[features]
predictions = model.predict(X_new)

# Принятие торговых решений на основе предсказаний
new_data['Prediction'] = predictions
