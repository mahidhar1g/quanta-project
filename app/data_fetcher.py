import requests
import pandas as pd
from datetime import datetime

import os
from dotenv import load_dotenv

def fetch_historical_data(api_key, base_url, ticker, start_date, end_date):
    """
    Fetch historical stock data using the Polygon API.

    Args:
        api_key (str): API key for authentication.
        base_url (str): Base URL for the Polygon API.
        ticker (str): Stock ticker symbol.
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.

    Returns:
        pd.DataFrame: DataFrame containing historical stock data with columns [date, close, volume].
    """
    endpoint = f"{base_url}/v2/aggs/ticker/{ticker}/range/1/day/{start_date}/{end_date}"
    params = {
        "adjusted": "true",
        "sort": "asc",
        "apiKey": api_key,
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json().get("results", [])

        if not data:
            raise ValueError("No data found for the given ticker and dates.")

        # Transforming the data into a DataFrame
        df = pd.DataFrame(data)

        # Extract relevant columns and rename for consistency
        df["date"] = pd.to_datetime(df["t"], unit="ms")
        df = df.rename(columns={"v": "volume", "o": "open", "c": "close"})

        # Select only required columns
        df = df[["date", "open", "close", "volume"]]

        return df

    except requests.exceptions.RequestException as e:
        raise ValueError(f"Request Error: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")
    
# # Test function
# if __name__ == "__main__":
#     try:
#         # Fetch data using values from .env by default
#         from dotenv import load_dotenv
#         load_dotenv()
        
#         api_key = os.getenv("API_KEY")
#         base_url = os.getenv("BASE_URL")
#         ticker = os.getenv("TICKER")
#         start_date = os.getenv("START_DATE")
#         end_date = os.getenv("END_DATE")
#         df = fetch_historical_data(api_key, base_url, ticker, start_date, end_date)
#         print(df)
#     except Exception as e:
#         print("Error:", e)