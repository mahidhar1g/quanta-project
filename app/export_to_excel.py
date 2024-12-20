import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill

def export_to_excel(data, output_file="breakout_analysis.xlsx"):
    """
    Export the DataFrame to a styled Excel file with additional details.

    Args:
        data (pd.DataFrame): DataFrame containing the breakout analysis results.
        output_file (str): Name of the output Excel file.

    Returns:
        str: Path to the generated Excel file.
    """
    # Create a writer object
    writer = pd.ExcelWriter(output_file, engine="openpyxl")
    
    # Add introductory details
    intro_data = {
        "Column Name": [
            "date", 
            "volume", 
            "close", 
            "price_change_pct_to_prev_day", 
            "closing_date_after_holding", 
            "close_after_holding", 
            "holding_return"
        ],
        "Description": [
            "Date of the breakout event",
            "Trading volume on the breakout day",
            "Closing price on the breakout day",
            "Percentage change in price compared to the previous day",
            "Date after the specified holding period",
            "Closing price after the holding period",
            "Percentage return after the holding period"
        ]
    }
    intro_df = pd.DataFrame(intro_data)
    intro_df.to_excel(writer, sheet_name="Details", index=False)
    
    # Write the data to a separate sheet
    data.to_excel(writer, sheet_name="Breakout Analysis", index=False)

    # Apply styling to the sheet
    workbook = writer.book
    analysis_sheet = writer.sheets["Breakout Analysis"]

    # Style headers
    for col in analysis_sheet.iter_cols(min_row=1, max_row=1, min_col=1, max_col=len(data.columns)):
        for cell in col:
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")

    # Style alternating rows
    for row in analysis_sheet.iter_rows(min_row=2, max_row=data.shape[0] + 1, min_col=1, max_col=len(data.columns)):
        for cell in row:
            cell.alignment = Alignment(horizontal="center", vertical="center")
            if cell.row % 2 == 0:
                cell.fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")

    # Save the file
    writer.save()
    return output_file
