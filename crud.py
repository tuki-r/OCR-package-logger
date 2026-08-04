from database import get_connection

def insert_package(image_bytes, name, unit, phone, delivery_company):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ExtractedDocs 
            (ImageData, ResidentName, Unit, PhoneNumber, DeliveryComp_Name)
        VALUES (?, ?, ?, ?, ?)
    """, (image_bytes, name, unit, phone, delivery_company))
    conn.commit()
    conn.close()

def get_all_packages():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ID, ResidentName, Unit, PhoneNumber, DeliveryComp_Name, 
               Status, DateLogged, DateCollected, CollectedBy, Relation
        FROM ExtractedDocs
        ORDER BY DateLogged DESC
    """)
    columns = [col[0] for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()

    for row in rows:
        if row['DateLogged']:
            row['DateLogged'] = row['DateLogged'].strftime('%Y-%m-%d %H:%M')
        if row['DateCollected']:
            row['DateCollected'] = row['DateCollected'].strftime('%Y-%m-%d %H:%M')
    return rows
