# OCR-package-logger
A web app for concierges to streamline package management. Scan or photograph a courier sticker and the application automatically extracts recipient details using OCR. Data is stored and displayed in a table, organised by status — Waiting and Collected. 
Built with **FastAPI**, **Python**, **Tesseract OCR** and **SQL Server**.

---
## Features
- OCR-based automatic extraction of name, unit number and phone from courier sticker photos
- Support for standard image formats (JPEG, PNG) and iPhone HEIC format
- Dual image capture — courier sticker photo and package photo
- Package log table with filter tabs (All / Waiting / Collected)
- Manage modal to mark packages as collected, view images and delete records
- Automatic DateCollected timestamp via SQL Server trigger
- POPIA-compliant test sticker generator for testing without real personal data

---
## Tech stack
| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python) |
| OCR | Tesseract OCR + pytesseract |
| Image handling | Pillow, pillow-heif |
| Database | SQL Server |
| Frontend | HTML, CSS, JavaScript |

---
## How to run
### Prerequisites
- Python 3.10+
- SQL Server
- Tesseract OCR installed at `C:\Progarm Files\Tesseract OCR`
- OBDC Driver 17 fro SQL Server 

### Setup
1. Clone the repository
2.Create and activate a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database — open SQL Server Management Studio and run:
```sql
CREATE DATABASE ImageOCRApp;
USE ImageOCRApp;

CREATE TABLE ExtractedDocs (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    ImageData VARBINARY(MAX),
    PackageImage VARBINARY(MAX),
    DateLogged DATETIME DEFAULT GETDATE(),
    DeliveryComp_Name NVARCHAR(100),
    ResidentName VARCHAR(100),
    Unit INT,
    PhoneNumber NVARCHAR(100),
    Status NVARCHAR(20) DEFAULT 'Waiting',
    DateCollected DATETIME NULL,
    CollectedBy NVARCHAR(100) NULL,
    Relation NVARCHAR(50) NULL
);

CREATE TRIGGER trg_DateCollected
ON ExtractedDocs
AFTER UPDATE
AS
BEGIN
    IF UPDATE(Status)
    BEGIN
        UPDATE ExtractedDocs
        SET DateCollected = GETDATE()
        FROM ExtractedDocs ED
        INNER JOIN inserted I ON ED.ID = I.ID
        WHERE I.Status = 'Collected'
        AND ED.DateCollected IS NULL;
    END
END;
```

5. Start the server:
```bash
uvicorn main:app --reload
```

6. Open your browser and go to:
http://localhost:8000

---

## Testing

To generate fake courier sticker images for OCR testing:
```bash
python tests/generate_stickers.py
```

This creates 25 sample stickers in `tests/test_stickers/`. All data is fictional and generated for POPIA compliance — no real personal information is used.

To run unit tests:
```bash
python tests/test_parser.py
```

---

## Licence

Copyright (c) 2026 Ontoketje Ramoroko. All Rights Reserved.

No part of this software may be reproduced, distributed, or used without explicit written permission from the author.
