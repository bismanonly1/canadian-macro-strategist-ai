import yfinance as yf
import pandas as pd
from src.config import CANADIAN_ETFS


def fetch_etf_prices(start_date: str = "2020-01-01") -> pd.DataFrame:
    tickers = list(CANADIAN_ETFS.values())

    price_data = yf.download(
        tickers=tickers,
        start=start_date,
        auto_adjust=True,
        progress=False
    )

    close_prices = price_data["Close"]
    close_prices = close_prices.rename(
        columns={v: k for k, v in CANADIAN_ETFS.items()}
    )

    return close_prices


def calculate_returns(price_df: pd.DataFrame) -> pd.DataFrame:
    return price_df.pct_change().dropna()