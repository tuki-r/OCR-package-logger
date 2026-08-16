from PIL import Image, ImageDraw, ImageFont
import os
import random


first_names = [
    "Thabo", "Mia", "Lisa", "Zanele", "Ruan",
    "Vaughn", "Sipho", "Hendrik", "Fatima", "Nicole", 
    "Tariq", "Shaun", "Yusuf", "Nikita", "Lamar", 
    "Peter", "Peggy", "Lerato", "Marco", "Davina",
    "Jean-Pierre", "Ntombi", "Paul", "Hendrik", 
    "Blessing", "Simone", "Mandela", "Chantel"
]

last_names = [
    "Naidoo", "Dlamini", "van der Berg", "Patel", "Khumalo",
    "Mokoena", "Botha", "Essa", "Adams", "Zulu", "de Villiers",
    "Rousseu", "Mthembu", "Abrahams", "Fortune", "Sithole", "Arendse",
    "Shabala", "Louw", "Fransman", "Williams", "Moore",
    "Blake", "Kruger", "Green", "Yamala", "Indiko", 
]

streets = [
    "Sylvia Street", "Buitenkant Street", "Voortrekker Road",
    "Main Road", "Kloof Street", "Durban Road", "Beach Road",
    "Bree Street", "Koeberg Road", "Adderley Street", "Ocean View Drive",
    "Somerset Road", "Lond Street", "Dorchester Road"
]

suburbs = [
    "Gardens", "Bellville", "Claremont", "Milnerton", "Green Point",
    "Cape Town CBD", "Mouille Point", "Woodstock", "Observatory",
    "Parow"
]

couriers = [
    "DHL", "Aramex", "PostNet", "The Courier Guy", "Fastway", 
    "RAM", "Buffalo", "Pargo", "Skynet", "Internet Express"
]


def generate_sticker_data(count=25):
    stickers = []
    for _ in range(count):
        stickers.append({
            "name": f"{random.choice(first_names)} {random.choice(last_names)}",
            "unit": random.randint(1,999),
            "phone": f"0{random.choice(['6','7','8'])}{random.randint(10000000,99999999)}",
            "street": f"{random.randint(1,99)} {random.choice(streets)}",
            "suburb": random.choice(suburbs),
            "city": "Cape Town",
            "postal": str(random.choice([8001, 7530, 7708, 7441, 8005, 7500, 7925])),
            "courier": random.choice(couriers)
        })

    return stickers

def make_sticker(data, index):
    W, H = 500, 320
    img = Image.new('RGB', (W,H), color='white')
    draw = ImageDraw.Draw(img)

    draw.rectangle([4, 4, W-5, H-5], outline = 'black', width = 2)
    draw.rectangle([4, 4, W-5, 40], fill='black')

    try:
        font_bold = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 16)
        font_large = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 18)
        font_med = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 14)
        font_small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 12)
    except:
        font_bold = font_large = font_med = font_small = ImageFont.load_default()

    tracking = f"CPT{index:03d}{data['unit']:04d}ZA"

    draw.text((12,12), data['courier'], fill='white', font=font_bold)
    draw.text((W-160, 12), tracking, fill='white', font= font_small)
    draw.text((12, 50), "SHIP TO:", fill = 'black', font=font_large)
    draw.line([(12, 70), (W-12, 70)], fill ='black', width=1)

    y = 80
    draw.text((12, y), data['name'], fill='black', font=font_large); y += 28
    draw.text((12, y), data['street'], fill='black', font=font_med); y += 22
    draw.text ((12, y), f"Unit {data['unit']}, {data['suburb']}", fill='black', font=font_med); y += 22
    draw.text ((12, y), f"{data['city']}, {data['postal']}", fill='black', font=font_med); y+=22
    draw.text ((12, y), f"Tel:{data['phone']}", fill='black', font=font_med)

    draw.line ([(12, H-45), (W-12, H-45)], fill='black', width=1)
    draw.text ((12, H-38), f"||| |||| {tracking}|||| |||", fill='black', font=font_small)

    output_dir = os.path.join(os.path.dirname(__file__), 'test_stickers')
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"sticker_{index:02d}_{data['name'].replace(' ','_')}.png")
    img.save(path)
    print(f"Created: {path}")

stickers = generate_sticker_data(25)


for i, s in enumerate(stickers, 1):
    make_sticker(s, i)

print(f"\nDone - {len(stickers)} stickers saved to tests/test_stickers/")