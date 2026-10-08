import psycopg2
from database import get_connection

def insert_package(image_bytes, package_image_bytes, name, unit, phone, delivery_company):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ExtractedDocs 
            (ImageData, PackageImage, ResidentName, Unit, PhoneNumber, DeliveryComp_Name)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (psycopg2.Binary(image_bytes), 
          psycopg2.Binary(package_image_bytes) if package_image_bytes else None,
          name, unit, phone, delivery_company))
    conn.commit()
    conn.close()

def get_all_packages():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id AS "ID", residentname AS "ResidentName", unit AS "Unit",
        phonenumber AS "PhoneNumber", deliverycomp_name AS "DeliveryComp_Name",
        status AS "Status", datelogged AS "DateLogged", datecollected AS "DateCollected", collectedby AS "CollectedBy",
        relation AS "Relation"
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
            CollectedBy = %s,
            Relation = %s
        WHERE ID = %s
        """, (collected_by, relation, package_id))
    conn.commit()
    conn.close()

def remove_package(package_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ExtractedDocs WHERE ID = %s", (package_id,))
    conn.commit()
    conn.close()

def get_package_image(package_id: int, type: str = "sticker"):
    conn = get_connection()
    cursor = conn.cursor()
    allowed_columns = {"sticker": "imagedata", "package": "packageimage"} 
    column = allowed_columns.get(type, "imagedata")  # Default to ImageData if type is invalid 
    cursor.execute(f"SELECT {column} FROM ExtractedDocs WHERE ID = %s", (package_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None
