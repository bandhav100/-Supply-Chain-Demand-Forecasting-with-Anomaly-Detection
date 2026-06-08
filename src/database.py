import psycopg2

try:
    conn = psycopg2.connect(
        database="github_trends",
        user="postgres",
        password="bandhav1",
        host="localhost",
        port="5432"
    )

    print("Database Connected Successfully!")

    conn.close()

except Exception as e:
    print("Error:", e)
