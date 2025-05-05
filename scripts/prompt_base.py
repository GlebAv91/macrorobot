import os
import json
from google import genai

# Retrieve the API key from environment variables
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("The GOOGLE_API_KEY environment variable is not set.")

client = genai.Client(api_key=api_key)


# Load contents from index_data_prompt.json
def load_index_data_prompt():
    with open("output/index_data_prompt.json", "r") as file:
        data = json.load(file)
    return data["contents"]


contents = load_index_data_prompt()

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=(
        "You are experienced investment analyst. "
        + contents
        + "Predict next 6 months close prices starting from the current month for all indices. "
        + "Ensure that the predictions use only the last day of each month as the date, "
        + "and do not include any dates beyond the next 6 months. "
        + "Provide structured output in the format: date (YYYY-MM-DD), index_name, close_price. "
        + "Do not include any disclaimers, methodology, or recommendations in the response. Only provide the predictions in the specified format."
    ),
)

print(response.text)

# Save the model response to a file
output_file = "output/model_response.json"
with open(output_file, "w") as file:
    json.dump({"response": response.text}, file, indent=4)

print(f"Model response saved to {output_file}.")
