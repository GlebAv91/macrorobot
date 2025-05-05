import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from scripts.database_connection import conn, cursor


# Load model output dynamically from a JSON file
def load_model_output(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    # Extract and parse the response string into structured data
    response = data["response"].strip("`\n")
    parsed_data = []
    for line in response.split("\n"):
        try:
            date, index_name, close_price = line.split(", ")
            parsed_data.append(
                {
                    "date": date.strip(),
                    "index_name": index_name.strip(),
                    "predicted_close_price": float(close_price.strip()),
                }
            )
        except ValueError as e:
            print(f"Skipping malformed line: {line}. Error: {e}")
    return parsed_data


# Paths to the JSON files containing model output
model_output_file = os.getenv("MODEL_OUTPUT_FILE", "output/model_response.json")
model_extended_output_file = os.getenv(
    "MODEL_EXTENDED_OUTPUT_FILE", "output/model_extended_response.json"
)

# Load and parse the data
model_output = load_model_output(model_output_file)
model_extended_output = load_model_output(model_extended_output_file)

# Prepare data for insertion
insert_data = []
for entry in model_output:
    insert_data.append(
        (entry["date"], entry["index_name"], entry["predicted_close_price"])
    )

insert_extended_data = []
for entry in model_extended_output:
    insert_extended_data.append(
        (entry["date"], entry["index_name"], entry["predicted_close_price"])
    )

# Modify the insert query to use the correct column name `predicted_close_price`
insert_query = """
    INSERT INTO public.index_data_prediction (date, index_name, predicted_close_price)
    SELECT * FROM (VALUES (%s::DATE, %s, %s)) AS new_data(date, index_name, predicted_close_price)
    WHERE NOT EXISTS (
        SELECT 1 FROM public.index_data_prediction
        WHERE public.index_data_prediction.date = new_data.date
          AND public.index_data_prediction.index_name = new_data.index_name
    );
"""

insert_extended_query = """
    INSERT INTO public.index_macro_data_prediction (date, index_name, predicted_close_price)
    SELECT * FROM (VALUES (%s::DATE, %s, %s)) AS new_data(date, index_name, predicted_close_price)
    WHERE NOT EXISTS (
        SELECT 1 FROM public.index_macro_data_prediction
        WHERE public.index_macro_data_prediction.date = new_data.date
          AND public.index_macro_data_prediction.index_name = new_data.index_name
    );
"""

try:
    cursor.executemany(insert_query, insert_data)
    cursor.executemany(insert_extended_query, insert_extended_data)
    conn.commit()
    print("Data successfully inserted into the database.")
except Exception as e:
    print(f"An error occurred during database insertion: {e}")
    conn.rollback()
finally:
    cursor.close()
    conn.close()
