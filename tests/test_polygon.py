import requests
import os
from dotenv import load_dotenv

# Loading environment variables from .env file
load_dotenv()

# Accessing API Key and Base URL from .env
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

def test_polygon_api(ticker="AAPL", date="2023-01-09"):
    """
    Test the Polygon API with the given ticker and date.
    Fetches open-close data for the specified date.
    """
    endpoint = f"{BASE_URL}/v1/open-close/{ticker}/{date}"
    params = {
        "adjusted": "true",
        "apiKey": API_KEY
    }
    
    # Making the API request
    response = requests.get(endpoint, params=params)
    
    # Handling response
    if response.status_code == 200:
        print("API is working. Sample data:", response.json())
    else:
        print("API Error:", response.json())

test_polygon_api()
