import streamlit as st
import pandas as pd
import os
import sys

# Add other member directories to sys.path to import their modules
sys.path.append(os.path.abspath("../Member1_Data_Collection"))
sys.path.append(os.path.abspath("../Member2_Forecasting_Models"))

from data_fetcher import fetch_crypto_data
from preprocessing import clean_data
from sentiment import get_sentiment_data
from charts import plot_price_trends, plot_volatility, plot_forecast

st.set_page_config(page_title="Crypto Insights Dashboard", page_icon="📈", layout="wide")

# Custom CSS for modern look
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
    }
    .stMetric {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
    }
    .stSidebar {
        background-color: #1E1E1E;
    }
    h1, h2, h3 {
        color: #FFFFFF;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📈 Crypto Time Series Analysis")
st.markdown("---")

# User Inputs
st.sidebar.header("🛠️ Settings")
ticker = st.sidebar.selectbox("Select Cryptocurrency", ("BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD"))
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2021-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("today"))

st.sidebar.markdown("---")
st.sidebar.header("🔮 Forecasting")
forecast_model = st.sidebar.selectbox("Select Prediction Model", ("ARIMA", "LSTM", "Prophet"))

@st.cache_data(ttl=3600)
def get_processed_data(ticker, start_date, end_date):
    fetch_result = fetch_crypto_data(ticker, str(start_date), str(end_date))
    if fetch_result is not None:
        raw_data, raw_file = fetch_result
        df_cleaned = clean_data(raw_file)
        if df_cleaned is None:
            return None, None
        processed_file = raw_file.replace('_raw.csv', '_processed.csv')
        return pd.read_csv(processed_file, index_col=0, parse_dates=True), raw_file
    return None, None

@st.cache_resource
def get_forecast(df, model_name):
    try:
        if model_name == "ARIMA":
            from arima_forecast import train_arima
            _, forecast = train_arima(df)
            return forecast
        elif model_name == "LSTM":
            from lstm_forecast import train_lstm
            _, forecast = train_lstm(df)
            return forecast
        elif model_name == "Prophet":
            from prophet_forecast import train_prophet
            _, forecast = train_prophet(df)
            return forecast['yhat'].tail(7).values
    except ImportError as e:
        st.error(f"Module not found: {e.name}. Please ensure all dependencies are installed.")
        st.stop()
    return None

# Initialize session state for analysis
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False
if 'data' not in st.session_state:
    st.session_state.data = None
if 'ticker' not in st.session_state:
    st.session_state.ticker = ""

# Fetch Data Button
if st.sidebar.button("Analyze Data"):
    try:
        with st.spinner("Fetching and processing data..."):
            df, raw_file = get_processed_data(ticker, start_date, end_date)
            
            if df is not None:
                st.session_state.analyzed = True
                st.session_state.data = df
                st.session_state.ticker = ticker
                st.sidebar.success(f"📂 Data loaded: {ticker}")
            else:
                st.session_state.analyzed = False
                st.error("Could not fetch or process data. Check your internet connection or ticker symbol.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        st.exception(e)

if st.session_state.analyzed and st.session_state.data is not None:
    df = st.session_state.data
    current_ticker = st.session_state.ticker
    
    # Member 1: Sentiment Analysis
    sentiment_score = get_sentiment_data(current_ticker)
    
    # Display Dashboard Metrics
    st.header("📊 Key Metrics")
    col1, col2, col3 = st.columns(3)
    
    # Use standard column names
    current_price = df['Close'].iloc[-1]
    volatility = df['Volatility'].iloc[-1]
    
    col1.metric("💰 Current Price", f"${current_price:,.2f}")
    col2.metric("📉 Annual Volatility", f"{volatility*100:.2f}%")
    col3.metric("🧠 Sentiment Score", f"{sentiment_score:.4f}")
    
    # Member 3: Visualization
    st.markdown("---")
    st.header("📈 Historical Trends")
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.plotly_chart(plot_price_trends(df, current_ticker), use_container_width=True)
    with col_chart2:
        st.plotly_chart(plot_volatility(df, current_ticker), use_container_width=True)
    
    # Member 2: Forecasting
    st.markdown("---")
    st.header(f"🔮 {forecast_model} AI Forecast (Next 7 Days)")
    
    with st.spinner(f"Running {forecast_model} model..."):
        forecast = get_forecast(df, forecast_model)
        st.plotly_chart(plot_forecast(df, forecast, current_ticker, forecast_model), use_container_width=True)
    
    st.success("Analysis and Forecasting complete!")

else:
    st.info("Select a cryptocurrency and date range to start analysis.")

st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #888888;'>
        <p>Created by Group 11 Amdox</p>
        <p style='font-size: 0.8em;'>
            Member 1: <a href='https://github.com/Shivampoonia04/Shivam1309' style='color: #17BECF;'>Shivampoonia04</a> | 
            Member 2: <a href='https://github.com/anshsakariya' style='color: #17BECF;'>anshsakariya</a> | 
            Member 3: Group Member
        </p>
    </div>
    """, unsafe_allow_html=True)
