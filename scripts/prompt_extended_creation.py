import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from calendar import monthrange
from scripts.database_connection import cursor

# Calculate dynamic date range
current_date = datetime.now()
end_date = current_date - relativedelta(months=6)  # 6 months back
start_date = current_date - relativedelta(months=12)  # 12 months back

# Calculate the last day of the finished month before end_date
last_finished_month = end_date - relativedelta(months=1)
last_day_of_finished_month = last_finished_month.replace(
    day=monthrange(last_finished_month.year, last_finished_month.month)[1]
)

# Query to fetch index data dynamically
index_query = f"""
    SELECT date, index_name, close_price
    FROM public.index_data
    WHERE date >= '{start_date.strftime('%Y-%m-%d')}' AND date <= '{end_date.strftime('%Y-%m-%d')}'
    ORDER BY date;
"""

# Query to fetch macro data dynamically
macro_query = f"""
    SELECT date, unemployment_rate, inflation_rate, interest_rate
    FROM public.macro_data
    WHERE date >= '{start_date.strftime('%Y-%m-%d')}' AND date <= '{end_date.strftime('%Y-%m-%d')}'
    ORDER BY date;
"""

# Fetch index data
cursor.execute(index_query)
index_data = cursor.fetchall()

# Fetch macro data
cursor.execute(macro_query)
macro_data = cursor.fetchall()

# Organize index data into a format suitable for the model prompt
formatted_index_data = {}
for row in index_data:
    date, index_name, close_price = row
    if index_name not in formatted_index_data:
        formatted_index_data[index_name] = []
    formatted_index_data[index_name].append(close_price)

# Organize macro data into a format suitable for the model prompt
formatted_macro_data = []
for row in macro_data:
    date, unemployment_rate, inflation_rate, interest_rate = row
    formatted_macro_data.append(
        {
            "date": date.strftime("%Y-%m-%d"),
            "unemployment_rate": unemployment_rate,
            "inflation_rate": inflation_rate,
            "interest_rate": interest_rate,
        }
    )

# Save the data to a JSON file
output = {"contents": ""}

for index_name, prices in formatted_index_data.items():
    prices_str = ", ".join(map(str, prices))
    output[
        "contents"
    ] += f"See latest 6 month close {index_name} index prices {prices_str} as of {end_date.strftime('%Y-%m-%d')}. "

output["contents"] += "\nMacro data for the same period:\n"
for macro_entry in formatted_macro_data:
    output["contents"] += (
        f"Date: {macro_entry['date']}, Unemployment Rate: {macro_entry['unemployment_rate']}, "
        f"Inflation Rate: {macro_entry['inflation_rate']}, Interest Rate: {macro_entry['interest_rate']}.\n"
    )

with open("output/index_macro_data_prompt.json", "w") as json_file:
    json.dump(output, json_file, indent=4)

print("Data has been saved to output/index_macro_data_prompt.json")
