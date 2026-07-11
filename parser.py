import re

def parse_courier_text(text):
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    result = {
        'name': None,
        'unit': None,
        'phone': None
    }

    # NAME: find the line containing "ship to", grab the next solid-looking line after it
    for i, line in enumerate(lines):
        if re.search(r'ship\s*to', line, re.IGNORECASE):
            for candidate in lines[i+1:]:
                if re.search(r'[A-Za-z]{2,}\s+[A-Za-z]{2,}', candidate):
                    result['name'] = candidate
                    break
            break

    # UNIT: look for the word "Unit" followed by digits, anywhere in the text
    unit_match = re.search(r'unit\s*[:\-]?\s*(\d+)', text, re.IGNORECASE)
    if unit_match:
        result['unit'] = int(unit_match.group(1))

    # PHONE: South African mobile numbers - 10 digits starting with 0
    phone_match = re.search(r'\b0\d{9}\b', text)
    if phone_match:
        result['phone'] = phone_match.group(0)

    return result