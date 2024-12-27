import os
from app.breakout_analyzer import detect_breakouts
from app.data_fetcher import fetch_historical_data
from app.export_to_excel import export_to_excel

def process_breakout_analysis(form_data):
    """
    Processes breakout analysis based on the input form data.

    Args:
        form_data (dict): Form inputs from the frontend.

    Returns:
        dict: Response containing success message, file link, and analyzed data.
    """
    ticker = form_data.get("ticker")
    start_date = form_data.get("start_date")
    end_date = form_data.get("end_date")
    volume_threshold = float(form_data.get("volume_threshold"))
    price_change_threshold = float(form_data.get("price_change_threshold"))
    holding_period = int(form_data.get("holding_period"))

    # Fetch historical data
    api_key = os.getenv("API_KEY")
    base_url = os.getenv("BASE_URL")
    data = fetch_historical_data(api_key, base_url, ticker, start_date, end_date)

    # Analyze breakouts
    breakouts = detect_breakouts(
        data, volume_threshold, price_change_threshold, holding_period
    )

    # Export results to Excel
    output_file = export_to_excel(breakouts)

    return {
        "message": "Analysis completed successfully!",
        "output_file": output_file,
        "data": breakouts.to_dict(orient="records"),
    }
