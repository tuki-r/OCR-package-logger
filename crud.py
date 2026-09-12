from database import get_connection

def insert_package(image_bytes, package_image_bytes, name, unit, phone, delivery_company):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ExtractedDocs 
            (ImageData, PackageImage, ResidentName, Unit, PhoneNumber, DeliveryComp_Name)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (image_bytes, package_image_bytes, name, unit, phone, delivery_company))
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

def mark_as_collected(package_id, collected_by, relation):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE ExtractedDocs
        SET Status = 'Collected',
            CollectedBy = ?,
            Relation = ?
        WHERE ID = ?
        """, (collected_by, relation, package_id))
    conn.commit()
    conn.close()

def remove_package(package_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ExtractedDocs WHERE ID = ?", (package_id,))
    conn.commit()
    conn.close()

def get_package_image(package_id: int, type: str = "sticker"):
    conn = get_connection()
    cursor = conn.cursor()
    column = "ImageData" if type == "sticker" else "PackageImage"
    cursor.execute(f"SELECT {column} FROM ExtractedDocs WHERE ID = ?", (package_id,)) 
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None
