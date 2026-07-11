from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional
import pytesseract
from PIL import Image
from pillow_heif import register_heif_opener
import io

from parser import parse_courier_text
from crud import insert_package


register_heif_opener()

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    delivery_company: Optional[str] = Form(None)
):
    # Read image
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    image = image.convert('RGB')

    # Run OCR
    extracted_text = pytesseract.image_to_string(image)

    # Parse the text
    parsed = parse_courier_text(extracted_text)

    # Insert into database
    insert_package(
        image_bytes=contents,
        name=parsed['name'],
        unit=parsed['unit'],
        phone=parsed['phone'],
        delivery_company=delivery_company
    )

    return {
        "message": "Package logged successfully",
        "name": parsed['name'],
        "unit": parsed['unit'],
        "phone": parsed['phone'],
        "delivery_company": delivery_company
    }
    
@app.get("/")
def serve_frontend():
    return FileResponse("index.html")

