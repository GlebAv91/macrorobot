import psycopg2


def get_historical_index_data():
    conn = psycopg2.connect(
        dbname="macro_analysis",
        user="postgres",
        password="your_password",
        host="localhost",
        port="5432",
    )
    cursor = conn.cursor()
    # Adjust the query based on your needs
    cursor.execute(
        "SELECT date, index_name, close_price FROM index_data ORDER BY date ASC"
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


# Example usage:
data = get_historical_index_data()
# Format the data into a string/JSON for the prompt
formatted = "\n".join(f"{row[0]}: {row[1]} closed at {row[2]}" for row in data)
