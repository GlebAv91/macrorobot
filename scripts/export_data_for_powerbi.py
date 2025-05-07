import sys
import os
from datetime import datetime, timedelta  # Added import for timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import csv
from scripts.database_connection import conn, cursor

# Output CSV file with current date in the name
current_date = datetime.now().strftime("%Y-%m-%d")
output_file = f"D:/Projects/powerbi_data/index_data_for_powerbi_{current_date}.csv"

# SQL query to extract data
query = """
    SELECT 
        date, 
        index_name, 
        close_price, 
        'index_data' AS source_table
    FROM public.index_data
    WHERE date >= date_trunc('month', current_date) - INTERVAL '6 months'
      AND date <= date_trunc('month', current_date) - INTERVAL '1 day'
    UNION ALL
    SELECT 
        date, 
        index_name, 
        predicted_close_price AS close_price, 
        'index_data_prediction' AS source_table
    FROM public.index_data_prediction
    WHERE date >= date_trunc('month', current_date) - INTERVAL '6 months'
      AND date <= date_trunc('month', current_date) - INTERVAL '1 day'
    UNION ALL
    SELECT 
        date, 
        index_name, 
        predicted_close_price AS close_price, 
        'index_macro_data_prediction' AS source_table
    FROM public.index_macro_data_prediction
    WHERE date >= date_trunc('month', current_date) - INTERVAL '6 months'
      AND date <= date_trunc('month', current_date) - INTERVAL '1 day'
    ORDER BY date, index_name, source_table;
"""

try:
    # Execute the query
    cursor.execute(query)
    rows = cursor.fetchall()

    # Write the data to a CSV file
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["date", "index_name", "close_price", "source_table"])  # Header
        writer.writerows(rows)

    print(f"Data successfully exported to {output_file}.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    cursor.close()
    conn.close()
