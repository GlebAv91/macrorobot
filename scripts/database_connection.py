import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="Nemamcas418",  # Replace with your actual password
    host="localhost",
    port="5432",
)
cursor = conn.cursor()
print("Connected to PostgreSQL successfully!")
