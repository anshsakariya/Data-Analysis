import plotly.graph_objects as go
import plotly.express as px

def plot_price_trends(data, ticker):
    """
    Plots historical price trends using Plotly with enhanced styling.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Closing Price', line=dict(color='#17BECF', width=2)))
    fig.add_trace(go.Scatter(x=data.index, y=data['MA7'], name='7-day MA', line=dict(color='#FF7F0E', width=1.5, dash='dash')))
    fig.add_trace(go.Scatter(x=data.index, y=data['MA30'], name='30-day MA', line=dict(color='#2CA02C', width=1.5, dash='dot')))
    
    fig.update_layout(
        title=f'<b>{ticker} Price Trends</b>',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        template='plotly_dark',
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=60, b=20)
    )
    return fig

def plot_volatility(data, ticker):
    """
    Plots annualized volatility with enhanced styling.
    """
    fig = px.line(data, x=data.index, y='Volatility', title=f'<b>{ticker} Annualized Volatility</b>')
    fig.update_traces(line_color='#FF4B4B', line_width=2)
    fig.update_layout(
        template='plotly_dark',
        xaxis_title='Date',
        yaxis_title='Volatility',
        margin=dict(l=20, r=20, t=60, b=20)
    )
    return fig

def plot_forecast(historical_data, forecast_data, ticker, model_name):
    """
    Plots historical price and forecasted price with enhanced styling.
    """
    fig = go.Figure()
    
    # Last 60 days of history
    hist_subset = historical_data.tail(60)
    fig.add_trace(go.Scatter(x=hist_subset.index, y=hist_subset['Close'], name='Historical', line=dict(color='#17BECF', width=2)))
    
    import pandas as pd
    import numpy as np
    forecast_dates = pd.date_range(start=historical_data.index[-1], periods=len(forecast_data) + 1)[1:]
    
    # Ensure forecast_data is a flat numpy array
    if hasattr(forecast_data, 'values'):
        y_data = forecast_data.values.flatten()
    else:
        y_data = np.array(forecast_data).flatten()
    
    # Add a connecting line from the last historical point
    all_dates = [historical_data.index[-1]] + list(forecast_dates)
    all_preds = [historical_data['Close'][-1]] + list(y_data)
    
    fig.add_trace(go.Scatter(
        x=all_dates, 
        y=all_preds, 
        name=f'{model_name} Forecast', 
        line=dict(color='#FFD700', width=3, dash='solid'),
        mode='lines+markers'
    ))
    
    fig.update_layout(
        title=f'<b>{ticker} {model_name} Prediction</b>',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        template='plotly_dark',
        hovermode='x unified',
        showlegend=True,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    return fig
