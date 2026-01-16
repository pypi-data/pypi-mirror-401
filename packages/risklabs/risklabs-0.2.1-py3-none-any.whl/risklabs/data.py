import yfinance as yf
import pandas as pd
from datetime import date, timedelta
from typing import List, Optional

class DataIngestion:
    def __init__(self) -> None:
        pass

    def fetch_data(self, tickers: List[str], start_date: date, end_date: date) -> pd.DataFrame:
        """
        Fetches historical data for the given tickers.
        Returns a DataFrame of daily returns.
        """
        print(f"Fetching data for {tickers} from {start_date} to {end_date}...")
        
        if not tickers:
            return pd.DataFrame()

        # Download data
        # auto_adjust=True accounts for splits and dividends
        data = yf.download(
            tickers, 
            start=start_date, 
            end=end_date, 
            auto_adjust=True, 
            group_by='ticker',
            progress=False
        )
        
        if data.empty:
            print("Warning: No data fetched.")
            return pd.DataFrame()

        # Extract Close prices
        # Structure depends on number of tickers:
        # If 1 ticker: columns are [Open, High, Low, Close, Volume]
        # If >1 ticker: MultiIndex columns (Ticker, OHLCV)
        
        prices = pd.DataFrame()
        
        if len(tickers) == 1:
            ticker = tickers[0]
            # yfinance sometimes returns a flat DF for single ticker with just columns
            # We want to normalize to be consistent
            if isinstance(data.columns, pd.MultiIndex):
                 prices[ticker] = data[ticker]['Close']
            else:
                 prices[ticker] = data['Close']
        else:
            # Flatten MultiIndex
            # data.columns levels: (Ticker, PriceType) or (PriceType, Ticker) - check yfinance version
            # Usually with group_by='ticker', it's Ticker first
            for ticker in tickers:
                try:
                    prices[ticker] = data[ticker]['Close']
                except KeyError:
                    print(f"Warning: Could not find Close for {ticker}")
        
        # Calculate daily returns
        returns = prices.pct_change().dropna()
        
        return returns

data_service = DataIngestion()
