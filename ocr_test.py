import pytesseract
from PIL import Image
from pillow_heif import register_heif_opener

from parser import parse_courier_text

register_heif_opener()

# point pytesseract to the tesseract install location(safety net, incase PATH isnt picked up)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load image
image = Image.open('test2.HEIC')
image = image.convert('RGB')  # Convert to RGB if needed


# Run OCR
text = pytesseract.image_to_string(image)

print("Extracted Text:")
print(text)
parsed = parse_courier_text(text)
print("Parsed result:", parsed)