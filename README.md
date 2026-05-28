
# Time Series Analysis with Cryptocurrency
**Created by Group 11 Amdox**

This project analyzes and forecasts cryptocurrency prices using historical data, sentiment analysis, and machine learning models (ARIMA, LSTM, Prophet).

## Project Overview
This project is developed by **Group 11 Amdox**.

### Team Members
- **Member 1 ([Shivampoonia04](https://github.com/Shivampoonia04/Shivam1309))**: Data Collection, Preprocessing & Sentiment Analysis
- **Member 2 ([anshsakariya](https://github.com/anshsakariya))**: Time Series Forecasting Models (ARIMA, LSTM, Prophet)
- **Member 3**: GUI and Visualization (Streamlit)

## Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run
### Option 1: Automatic Setup (Recommended)
Double-click the `setup_and_run.bat` file. This script will:
1. Check for Python (and install it via `winget` if missing).
2. Install all necessary libraries from `requirements.txt`.
3. Launch the Streamlit dashboard automatically.

### Option 2: Manual Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the main application:
   ```bash
   python main.py
   ```

## Project Structure
- `Member1_Data_Collection/`: Scripts for fetching and cleaning data.
- `Member2_Forecasting_Models/`: Implementation of ARIMA, LSTM, and Prophet.
- `Member3_GUI_Visualization/`: Streamlit app and Plotly visualizations.
- `main.py`: Entry point for the application.
- `requirements.txt`: List of dependencies.
