import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

def train_lstm(data, n_steps=60):
    """
    Trains an LSTM model on the closing price.
    """
    # Scale data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))
    
    # Prepare training data
    x_train, y_train = [], []
    for i in range(n_steps, len(scaled_data)):
        x_train.append(scaled_data[i-n_steps:i, 0])
        y_train.append(scaled_data[i, 0])
        
    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    
    # Build LSTM model
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, epochs=5, batch_size=32, verbose=0)
    
    # Predict next 7 days
    last_60_days = scaled_data[-n_steps:]
    predictions = []
    current_batch = last_60_days.reshape((1, n_steps, 1))
    
    for i in range(7):
        current_pred = model.predict(current_batch, verbose=0)[0]
        predictions.append(current_pred)
        # Reshape current_pred to (1, 1, 1) for concatenation
        new_pred = np.reshape(current_pred, (1, 1, 1))
        current_batch = np.append(current_batch[:, 1:, :], new_pred, axis=1)
        
    forecast = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
    
    return model, forecast

if __name__ == "__main__":
    # Example usage
    processed_data_file = "../Member1_Data_Collection/data/BTC-USD_processed.csv"
    import os
    if os.path.exists(processed_data_file):
        df = pd.read_csv(processed_data_file, index_col=0, parse_dates=True)
        model, forecast = train_lstm(df)
        print("LSTM Forecast for the next 7 days:")
        print(forecast)
    else:
        print(f"Processed data file {processed_data_file} not found. Please run preprocessing.py first.")
