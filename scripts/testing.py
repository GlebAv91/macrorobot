import pandas as pd
from fredapi import Fred

FRED_API_KEY = "354e347f2dd3acd6dbc7badfc7edd0c8"


class MacroDataFetcher:
    def __init__(self, api_key):
        """
        Initialize MacroDataFetcher with the provided FRED API key.
        """
        self.api_key = api_key
        self.fred = Fred(api_key=api_key)

    def fetch_last_12_unemployment_rates(self):
        """
        Fetch the last 12 data points of unemployment rate.
        Returns a Pandas DataFrame.
        """
        unemployment_data = self.fred.get_series("UNRATE")
        unemployment_last_12 = unemployment_data.tail(12)
        unemployment_df = pd.DataFrame(
            unemployment_last_12, columns=["Unemployment Rate"]
        )
        unemployment_df.index.name = "Date"
        unemployment_df.reset_index(inplace=True)
        return unemployment_df

    def fetch_last_12_inflation_rates(self):
        """
        Fetch the last 12 data points of inflation rate (CPI).
        Returns a Pandas DataFrame.
        """
        inflation_data = self.fred.get_series("CPIAUCSL")
        inflation_last_12 = inflation_data.tail(12)
        inflation_df = pd.DataFrame(inflation_last_12, columns=["Inflation Rate"])
        inflation_df.index.name = "Date"
        inflation_df.reset_index(inplace=True)
        return inflation_df

    def fetch_last_12_interest_rates(self):
        """
        Fetch the last 12 data points of interest rates (Federal Funds Rate).
        Returns a Pandas DataFrame.
        """
        interest_rate_data = self.fred.get_series("FEDFUNDS")
        interest_rate_last_12 = interest_rate_data.tail(12)
        interest_rate_df = pd.DataFrame(
            interest_rate_last_12, columns=["Interest Rate"]
        )
        interest_rate_df.index.name = "Date"
        interest_rate_df.reset_index(inplace=True)
        return interest_rate_df


# Example usage:
if __name__ == "__main__":
    # Replace 'your_api_key' with your actual FRED API key
    fetcher = MacroDataFetcher(FRED_API_KEY)

    # Fetch the last 12 data points for each indicator
    unemployment_rate_last_12 = fetcher.fetch_last_12_unemployment_rates()
    inflation_rate_last_12 = fetcher.fetch_last_12_inflation_rates()
    interest_rate_last_12 = fetcher.fetch_last_12_interest_rates()

    # Display the retrieved data
    print("Unemployment Rate (Last 12):\n", unemployment_rate_last_12)
    print("Inflation Rate (Last 12):\n", inflation_rate_last_12)
    print("Interest Rate (Last 12):\n", interest_rate_last_12)
