from google import genai

client = genai.Client(api_key="AIzaSyCKz2cv_gMZ0nFAwstNItzD2YaI5GKshR8")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="See latest month close S&P 500 index prices February: 5954.5, March: 5611.85. "
    "Predict S&P 500 index closing prices for the next 6 months(from April to October) based on provided data. Provide only numbers as a result and no other explanation.",
)

print(response.text)
