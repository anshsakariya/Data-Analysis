from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
import numpy as np

def train_arima(data, p=5, d=1, q=0):
    """
    Trains an ARIMA model on the closing price.
    """
    # Use closing price
    close_prices = data['Close']
    
    # Fit ARIMA model
    model = ARIMA(close_prices, order=(p, d, q))
    model_fit = model.fit()
    
    # Forecast for the next 7 days
    forecast = model_fit.forecast(steps=7)
    
    return model_fit, forecast

if __name__ == "__main__":
    # Example data
    raw_data_file = "../Member1_Data_Collection/data/BTC-USD_processed.csv"
    import os
    if os.path.exists(raw_data_file):
        df = pd.read_csv(raw_data_file, index_col=0, parse_dates=True)
        model, forecast = train_arima(df)
        print("ARIMA Forecast for the next 7 days:")
        print(forecast)
    else:
        print(f"Processed data file {raw_data_file} not found. Please run preprocessing.py first.")
