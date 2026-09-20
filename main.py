# Imports
# FastAPI and related modules
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional
import pytesseract
from PIL import Image
from pillow_heif import register_heif_opener
from fastapi.responses import JSONResponse
import io
import base64

from parser import parse_courier_text
from crud import insert_package, get_all_packages, mark_as_collected, remove_package, get_package_image

# register HEIF opener for handling HEIC/HEIF images
register_heif_opener()

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    package_image: Optional[UploadFile] = File(None),
    delivery_company: Optional[str] = Form(None)
):
    # Read image 
    # Convert to RGB if necessary
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    image = image.convert('RGB')

    # Run OCR
    extracted_text = pytesseract.image_to_string(image)

    # Parse the text
    parsed = parse_courier_text(extracted_text)

    package_image_bytes = None
    if package_image:
        package_image_bytes = await package_image.read()

    # Insert into database
    insert_package(
        image_bytes=contents,
        package_image_bytes=package_image_bytes,
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

@app.get("/packages")
def list_packages():
    return get_all_packages()


@app.put("/packages/{package_id}/collect")
def collect_package(package_id: int, collected_by: str = Form(...), relation: str = Form(...)):
    from crud import mark_as_collected
    # SQL trigger trg_DateCollected will automatically set the date_collected field to the current timestamp
    mark_as_collected(package_id, collected_by, relation)
    return {"message": "Package marked as collected"}

@app.delete("/packages/{package_id}")
def delete_package(package_id: int):
    from crud import remove_package
    remove_package(package_id)
    return {"message": "Package removed successfully"}

@app.get("/packages/{package_id}/image")
def get_image(package_id: int, type: str = "sticker"):
    from crud import get_package_image
    # type='sticker' or 'package' returns the corresponding image bytes from the database
    # Images stored as VARBINARY in SQL Server, returned as base64 for JSON transport
    image_bytes = get_package_image(package_id, type)
    if not image_bytes:
        return JSONResponse(status_code=404, content={"error": "Image not found"})
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    return {"image": encoded}


# Production entry point for devlopment use: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0", 
        port=8000, 
        reload=False, 
        workers=4
    )

