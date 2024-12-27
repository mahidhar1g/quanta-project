import os
import sys
from dotenv import load_dotenv
import pandas as pd

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.data_fetcher import fetch_historical_data
from app.export_to_excel import export_to_excel

# Load environment variables
load_dotenv()

def detect_breakouts(data, volume_threshold, price_change_threshold, holding_period):
    """
    Detect breakout days based on volume and price change thresholds.

    Args:
        data (pd.DataFrame): DataFrame containing historical stock data.
        volume_threshold (float): Minimum percent increase in volume compared to the 20-day average.
        price_change_threshold (float): Minimum percent increase in closing price compared to the previous day.
        holding_period (int): Number of days to hold the stock after buying on a breakout day.

    Returns:
        pd.DataFrame: DataFrame with breakout days and their subsequent returns.
    """
    if len(data) < 20:
        raise ValueError("Not enough data to calculate a 20-day rolling average. Please provide a larger date range.")

    # Calculate 20-day rolling average of volume
    data["20_day_avg_volume"] = data["volume"].rolling(window=20).mean()

    # Calculate volume change percentage
    data["volume_change_pct"] = (data["volume"] / data["20_day_avg_volume"] - 1) * 100

    # Calculate daily price change percentage
    data["price_change_pct_to_prev_day"] = (data["close"] / data["close"].shift(1) - 1) * 100

    # Identify breakout days
    data["is_breakout"] = (data["volume_change_pct"] > volume_threshold) & (data["price_change_pct_to_prev_day"] > price_change_threshold)
    breakout_days = data[data["is_breakout"].fillna(False)].copy()

    closing_prices_after_holding = []
    closing_dates_after_holding = []

    for index in breakout_days.index:
        future_index = index + holding_period
        if future_index < len(data):
            closing_prices_after_holding.append(data.loc[future_index, "close"])
            closing_dates_after_holding.append(data.loc[future_index, "date"])
        else:
            closing_prices_after_holding.append(None)
            closing_dates_after_holding.append(None)

    breakout_days["close_after_holding"] = closing_prices_after_holding
    breakout_days["closing_date_after_holding"] = closing_dates_after_holding
    breakout_days = breakout_days.dropna(subset=["close_after_holding"])
    
    # Calculate return
    breakout_days["holding_return"] = (
        (breakout_days["close_after_holding"] - breakout_days["close"]) / breakout_days["close"]
    ) * 100

    return breakout_days[["date", "volume", "close", "price_change_pct_to_prev_day", "closing_date_after_holding", "close_after_holding", "holding_return"]]


# # Test function
# if __name__ == "__main__":
#     try:
#         # Load environment variables
#         api_key = os.getenv("API_KEY")
#         base_url = os.getenv("BASE_URL")
#         ticker = os.getenv("TICKER")
#         start_date = os.getenv("START_DATE")
#         end_date = os.getenv("END_DATE")
#         volume_threshold = float(os.getenv("VOLUME_THRESHOLD"))
#         price_change_threshold = float(os.getenv("PRICE_CHANGE_THRESHOLD"))
#         holding_period = int(os.getenv("HOLDING_PERIOD"))

#         # Fetch historical data
#         data = fetch_historical_data(api_key, base_url, ticker, start_date, end_date)

#         # Detect breakouts
#         breakouts = detect_breakouts(data, volume_threshold, price_change_threshold, holding_period)

#         # Print results
#         print("Breakout Days and Returns:")
#         print(breakouts)

#     except Exception as e:
#         print("Error:", e)
