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

    def fetch_last_12_macro_data(self):
        """
        Fetch the last 12 data points for unemployment rate, inflation rate, and interest rate.
        Returns a Pandas DataFrame with all three series aligned by date.
        """
        # Fetch all series
        unemployment_data = self.fred.get_series("UNRATE")
        inflation_data = self.fred.get_series("CPIAUCSL")
        interest_rate_data = self.fred.get_series("FEDFUNDS")

        # Combine into a single DataFrame
        combined_df = pd.DataFrame(
            {
                "Unemployment_Rate": unemployment_data,
                "Inflation_Rate": inflation_data,
                "Interest_Rate": interest_rate_data,
            }
        )

        # Drop rows with missing values and keep the last 12 rows
        combined_df.dropna(inplace=True)
        combined_df = combined_df.tail(12)

        # Reset index for better readability
        combined_df.index.name = "Date"
        combined_df.reset_index(inplace=True)

        return combined_df


# Example usage:
if __name__ == "__main__":
    # Replace 'your_api_key' with your actual FRED API key
    fetcher = MacroDataFetcher(FRED_API_KEY)

    # Fetch the last 12 data points for all indicators
    macro_data_last_12 = fetcher.fetch_last_12_macro_data()

    # Display the retrieved data
    print("Macro Data (Last 12):\n", macro_data_last_12)
