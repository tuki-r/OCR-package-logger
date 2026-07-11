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
