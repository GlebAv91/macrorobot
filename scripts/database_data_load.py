import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from scripts.macro_data import MacroDataFetcher
from scripts.indices import IndexDataFetcher
from scripts.database_connection import conn, cursor

# Add a debug flag to control whether to execute or just print SQL queries
debug_mode = False  # Set to True to print SQL queries instead of executing

# Initialize fetchers
macro_fetcher = MacroDataFetcher(api_key="354e347f2dd3acd6dbc7badfc7edd0c8")
index_fetcher = IndexDataFetcher()

# Fetch data
macro_data = macro_fetcher.fetch_last_12_macro_data()
indices_data = index_fetcher.fetch_last_12_months_close()


# Function to insert data into the database
def insert_data(table_name, data, date_column):
    for _, row in data.iterrows():
        # Convert Timestamp to date for the date column
        row[date_column] = row[date_column].date()

        # Dynamically adjust the SELECT condition based on the table name
        if table_name == "public.index_data":
            # Check if the combination of Date and Index_Name exists
            cursor.execute(
                f"SELECT 1 FROM {table_name} WHERE {date_column} = %s AND Index_Name = %s",
                (row[date_column], row["Index_Name"]),
            )
        else:
            # Check if the Date exists (for macro_data)
            cursor.execute(
                f"SELECT 1 FROM {table_name} WHERE {date_column} = %s",
                (row[date_column],),
            )

        if cursor.fetchone() is None:
            # Prepare SQL query
            columns = ", ".join(data.columns)
            values = ", ".join(["%s"] * len(data.columns))
            sql_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
            sql_values = tuple(row)

            if debug_mode:
                # Print the query and values instead of executing
                print("SQL Query:", sql_query)
                print("Values:", sql_values)
            else:
                # Execute the query if not in debug mode
                cursor.execute(sql_query, sql_values)


# Insert macro data into the database
insert_data("public.macro_data", macro_data, "Date")

# Insert indices data into the correct table
for index_name, index_data in indices_data.items():
    # Ensure the "Index_Name" column is included in the data
    index_data["Index_Name"] = index_name

    # Use the correct table name for indices data
    table_name = "public.index_data"
    insert_data(table_name, index_data, "Date")

# Commit changes and close connection
if not debug_mode:
    conn.commit()
cursor.close()
conn.close()
print("Data processing completed!")
