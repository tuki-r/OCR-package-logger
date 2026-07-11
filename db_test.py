from database import get_connection

try: 
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ExtractedDocs")
    print("Connection successful.")
    print("Rows in table:", cursor.rowcount)
    conn.close()
except Exception as e:
    print("Connection failed:", e)