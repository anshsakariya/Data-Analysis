from prophet import Prophet
import pandas as pd

def train_prophet(data):
    """
    Trains a Facebook Prophet model on the closing price.
    """
    # Prepare data for Prophet (columns 'ds' and 'y')
    df = data[['Close']].copy()
    df.reset_index(inplace=True)
    # Ensure columns are exactly ds and y regardless of input names
    df = df.iloc[:, [0, 1]]
    df.columns = ['ds', 'y']
    # Remove timezone if present (Prophet doesn't support it)
    df['ds'] = pd.to_datetime(df['ds']).dt.tz_localize(None)
    
    # Initialize and fit model
    model = Prophet()
    model.fit(df)
    
    # Forecast for the next 7 days
    future = model.make_future_dataframe(periods=7)
    forecast = model.predict(future)
    
    return model, forecast

if __name__ == "__main__":
    # Example usage
    processed_data_file = "../Member1_Data_Collection/data/BTC-USD_processed.csv"
    import os
    if os.path.exists(processed_data_file):
        df = pd.read_csv(processed_data_file, index_col=0, parse_dates=True)
        model, forecast = train_prophet(df)
        print("Prophet Forecast for the next 7 days:")
        print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(7))
    else:
        print(f"Processed data file {processed_data_file} not found. Please run preprocessing.py first.")
