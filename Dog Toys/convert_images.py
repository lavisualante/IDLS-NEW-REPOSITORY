#!/usr/bin/env python3
import os
import base64
import csv

# Read CSV data
csv_path = "D:\\IDLS\\NEW ATTEMPT\\Dog Toys\\amazon_dog_toys_bestsellers.csv"
products = []
with open(csv_path, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        products.append(row)

# Create image mapping
image_dir = "D:\\IDLS\\NEW ATTEMPT\\Dog Toys\\extracted\\images"
image_mapping = {}

# Map CSV filenames to actual image filenames
file_mapping = {
    'benebone_wishbone.jpg': 'Benebone Wishbone Durable Dog Chew Toy Real Bacon Flavor.jpg',
    'nylabone_power_chew.jpg': 'Nylabone Original Power Chew Classic Bone Peanut Butter Flavor.jpg',
    'nylabone_textured_ring.jpg': 'Nylabone Power Chew Textured Ring Flavor Medley.jpg',
    'kong_classic.jpg': 'KONG Classic Stuffable Dog Toy Natural Rubber.jpg',
    'kong_extreme.jpg': 'KONG Extreme Dog Toy Black Power Chewers.jpg',
    'chuckit_ultra_ball.jpg': 'Chuckit Ultra Ball High-Bounce Fetch Ball.jpg',
    'wobble_wag_giggle.jpg': 'Wobble Wag Giggle Ball Interactive Noisy Fetch Ball.jpg',
    'mammoth_rope_tug.jpg': 'Mammoth Flossy Chews Cottonblend Rope Tug 3-Knot.jpg',
    'multipet_lamb_chop.jpg': 'Multipet Lamb Chop Plush Squeaky Dog Toy.jpg',
    'best_pet_stuffless.jpg': 'Best Pet Supplies 2-in-1 Stuffless Squeaky Toys Plush Raccoon Fox.jpg',
    'jalousie_5pack.jpg': 'Jalousie 5-Pack Plush Dog Toys Assorted Squeaky Toys.jpg',
    'outward_hound_brick.jpg': 'Outward Hound Nina Ottosson Dog Brick Puzzle Toy Interactive Treat Puzzle.jpg',
    'outward_hound_squirrel.jpg': 'Outward Hound Hide-A-Squirrel Puzzle Plush Hide and Seek Toy.jpg',
    'petstages_dogwood.jpg': 'Petstages Dogwood Chew Stick Wood Alternative Chew Toy.jpg',
    'smartpetlove_snuggle.jpg': 'SmartPetLove Snuggle Puppy Behavioral Aid Toy Comfort Plush.jpg',
    'chuckit_paraflight.jpg': 'Chuckit Paraflight Flyer Flying Disc Toy.jpg'
}

# Convert images to base64
for csv_filename, actual_filename in file_mapping.items():
    image_path = os.path.join(image_dir, actual_filename)
    if os.path.exists(image_path):
        with open(image_path, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            image_mapping[csv_filename] = encoded_string
            print(f"Converted: {actual_filename}")

# Generate product categories
categories = {
    'chew-toys': ['Benebone Wishbone', 'Nylabone', 'KONG', 'Petstages'],
    'fetch-toys': ['Chuckit', 'Wobble Wag'],
    'plush-toys': ['Lamb Chop', 'Stuffless', 'Jalousie', 'Snuggle'],
    'puzzle-toys': ['Outward Hound'],
    'rope-toys': ['Mammoth']
}

print(f"Converted {len(image_mapping)} images to base64")
print("Products loaded:", len(products))