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

# Query to fetch data dynamically
query = f"""
    SELECT date, index_name, close_price
    FROM public.index_data
    WHERE date >= '{start_date.strftime('%Y-%m-%d')}' AND date <= '{end_date.strftime('%Y-%m-%d')}'
    ORDER BY date;
"""

cursor.execute(query)
data = cursor.fetchall()

# Organize data into a format suitable for the model prompt
formatted_data = {}
for row in data:
    date, index_name, close_price = row
    if index_name not in formatted_data:
        formatted_data[index_name] = []
    formatted_data[index_name].append(close_price)

# Save the data to a JSON file
output = {"contents": ""}

for index_name, prices in formatted_data.items():
    prices_str = ", ".join(map(str, prices))
    output[
        "contents"
    ] += f"See latest 6 month close {index_name} index prices {prices_str} as of {last_day_of_finished_month.strftime('%Y-%m-%d')}. "

with open("output/index_data_prompt.json", "w") as json_file:
    json.dump(output, json_file, indent=4)

print("Data has been saved to output/index_data_prompt.json")
