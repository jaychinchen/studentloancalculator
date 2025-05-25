import yfinance as yf
from datetime import datetime, timedelta
import streamlit as st
import numpy as np

INVESTMENT_OPTIONS = {
    "S&P 500 (US)": "SPY", 
    "FTSE All-World": "VWRL.L",
    "Vanguard FTSE 100 ETF": "VUKE.L",  
    "Custom": "CUSTOM"
}

def calculate_historical_returns(ticker, years):
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=years*365)
        
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        
        price_col = 'Adj Close' if 'Adj Close' in data.columns else 'Close'
        
        yearly_returns = []
        for i in range(len(data)-252, 0, -252):
            if i >= 252:
                yearly_return = (data[price_col].iloc[i+251] - data[price_col].iloc[i]) / data[price_col].iloc[i]
                yearly_returns.append(yearly_return)
        
        if not yearly_returns:
            raise Exception("Not enough historical data available")
            
        mean_return = np.mean(yearly_returns)
        return_std = np.std(yearly_returns)
        
        return {
            'mean_return': mean_return * 100,
            'variation': return_std * 2 * 100
        }
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {str(e)}")
        return None 
