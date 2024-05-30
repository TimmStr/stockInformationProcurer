import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

stockprices = pd.read_csv("../stocks/AAPL.csv", index_col="Date")

test_ratio = 0.2
training_ratio = 1 - test_ratio

train_size = int(training_ratio * len(stockprices))
test_size = int(test_ratio * len(stockprices))
print(f"train_size: {train_size}, test_size: {test_size}")

train = stockprices[:train_size][["Close"]]
test = stockprices[train_size:][["Close"]]

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_training_set = scaler.fit_transform(train)
scaled_test_set = scaler.transform(test)


def create_dataset(dataset, look_back=1):
    X, y = [], []
    for i in range(len(dataset) - look_back):
        a = dataset[i:(i + look_back), 0]
        X.append(a)
        y.append(dataset[i + look_back, 0])
    return np.array(X), np.array(y)


look_back = 1
X_train, y_train = create_dataset(scaled_training_set, look_back)
X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))

X_test, y_test = create_dataset(scaled_test_set, look_back)
X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(1, look_back)))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50))
model.add(Dense(units=1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(X_train, y_train, epochs=100, batch_size=128)
model.save("lstm_model.h5")

predictions = model.predict(X_test)
plt.plot(predictions, label="Predictions")
plt.plot(y_test,label="Actual")
plt.legend()
plt.show()
print('pred',predictions)
print('y_true', y_test)
print(len(predictions))
print(len(y_test))