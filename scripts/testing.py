import pandas as pd
from scripts.macro_data import MacroDataFetcher
from scripts.indices import IndexDataFetcher
from scripts.database_connection import conn, cursor

# Initialize fetchers
macro_fetcher = MacroDataFetcher(api_key="354e347f2dd3acd6dbc7badfc7edd0c8")
index_fetcher = IndexDataFetcher()

# Fetch data
unemployment_data = macro_fetcher.fetch_last_12_unemployment_rates()
inflation_data = macro_fetcher.fetch_last_12_inflation_rates()
interest_rate_data = macro_fetcher.fetch_last_12_interest_rates()
indices_data = index_fetcher.fetch_last_12_months_close()


# Function to insert data into the database
def insert_data(table_name, data, date_column):
    for _, row in data.iterrows():
        # Check if the date already exists in the table
        cursor.execute(
            f"SELECT 1 FROM {table_name} WHERE {date_column} = %s", (row[date_column],)
        )
        if cursor.fetchone() is None:
            # Insert new data
            columns = ", ".join(data.columns)
            values = ", ".join(["%s"] * len(data.columns))
            cursor.execute(
                f"INSERT INTO {table_name} ({columns}) VALUES ({values})",
                tuple(row),
            )


# Insert macroeconomic data
insert_data("macro_data", unemployment_data, "Date")
insert_data("macro_data", inflation_data, "Date")
insert_data("macro_data", interest_rate_data, "Date")

# Insert indices data
for index_name, index_data in indices_data.items():
    table_name = index_name.lower().replace(" ", "_") + "_indices"
    insert_data(table_name, index_data, "Month-End Date")

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()
print("Data inserted successfully!")
