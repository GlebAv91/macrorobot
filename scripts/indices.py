import pandas as pd
import calendar
from datetime import datetime, timedelta
import yfinance as yf


class IndexDataFetcher:
    def __init__(self):
        """
        Initialize the IndexDataFetcher.
        """
        # Define indices
        self.indices = {"S&P 500": "^GSPC", "Dow Jones": "^DJI", "Nasdaq": "^IXIC"}

    def fetch_last_12_months_close(self):
        """
        Fetch the closing prices for the last day of the month for the past 12 months.
        Returns a dictionary of DataFrames, one for each index.
        """
        # Get the current date
        end_date = datetime.today()

        # Calculate 12 months back
        start_date = end_date - timedelta(days=365)  # Approximation for 1 year

        # Dictionary to store the results
        indices_data = {}

        for index_name, index_symbol in self.indices.items():
            # Fetch historical data for the index
            data = yf.Ticker(index_symbol).history(start=start_date, end=end_date)

            # Filter data for the last day of each month
            monthly_data = self._get_monthly_closing_prices(data, index_name)

            # Add to the dictionary
            indices_data[index_name] = monthly_data

        return indices_data

    def _get_monthly_closing_prices(self, data, index_name):
        """
        Extract the closing prices for the last day of each month,
        excluding the current month if it has not finished yet,
        and limit the result to the last 12 months.
        """
        # Get the current date as a pandas Timestamp
        today = pd.Timestamp(datetime.today())

        # Ensure the index is timezone-naive
        data.index = data.index.tz_localize(None)

        # Group data by month and select the last entry
        monthly_closing = data.groupby(data.index.to_period("M")).tail(1)

        # Exclude the current month if it has not finished
        monthly_closing = monthly_closing[
            monthly_closing.index.to_period("M") < today.to_period("M")
        ]

        # Limit to the last 12 months
        monthly_closing = monthly_closing.tail(12)

        # Format the data
        monthly_closing = monthly_closing[["Close"]].reset_index()
        monthly_closing.rename(
            columns={"Close": "Close_Price", "Date": "Date"},
            inplace=True,
        )

        # Add the index name as a separate column
        monthly_closing["Index_Name"] = index_name

        return monthly_closing


# Example usage:
if __name__ == "__main__":
    # Initialize the fetcher
    index_fetcher = IndexDataFetcher()

    # Fetch the last 12 months' close prices for all indices
    indices_close_data = index_fetcher.fetch_last_12_months_close()

    # Print the data
    for index_name, index_data in indices_close_data.items():
        print(f"{index_name} (Last 12 Months):")
        print(index_data)
        print("\n")
