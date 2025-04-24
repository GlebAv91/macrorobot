from google import genai

client = genai.Client(api_key="AIzaSyCKz2cv_gMZ0nFAwstNItzD2YaI5GKshR8")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Predict S&P 500 index closing price for the next month based on historical data. Provide only one numbers as a result",
)

print(response.text)
