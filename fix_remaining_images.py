#!/usr/bin/env python3
import re
import json

def fix_images():
    # Read the HTML file
    with open('optimized_images.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Read the base64 data from the JS file
    with open('Dog Health/dog_health_images_base64.js', 'r', encoding='utf-8') as f:
        js_content = f.read()

    # Extract the JSON data from the JS file (it's an object, not array)
    json_match = re.search(r'const dogHealthImages = (\{.*?\});', js_content, re.DOTALL)
    if not json_match:
        print("Could not find JSON data in JS file")
        return

    try:
        images_data = json.loads(json_match.group(1))
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return

    # Create a mapping of filename to base64 data
    image_map = {}
    for filename, data in images_data.items():
        base64_data = data['dataUri']
        # Also map by clean filename
        clean_filename = filename.replace('_', ' ').replace('.jpg', '').replace('.png', '').replace('.jpeg', '')
        image_map[filename] = base64_data
        image_map[clean_filename] = base64_data

    # Replace file path images with base64
    replacements = [
        ('Dog Health/Purina Pro Plan Fortiflora Canine Probiotic Supplement.jpg', 'Purina Pro Plan Fortiflora Canine Probiotic'),
        ('Dog Health/Grizzly Salmon Oil for Dogs.jpg', 'Grizzly Salmon Oil for Dogs'),
        ('Dog Health/VetriScience GlycoFlex 3 Hip and Joint Support.jpg', 'VetriScience GlycoFlex 3 Hip and Joint Support'),
        ('Dog Health/Iams Minichunks Dog Food.jpg', 'Iams Minichunks Dog Food'),
        ('Dog Health/TruDog Dog Food.jpg', 'TruDog Dog Food')
    ]

    for file_path, alt_text in replacements:
        if file_path in image_map:
            # Replace the src attribute
            old_pattern = f'src="{file_path}"'
            new_src = image_map[file_path]
            html_content = html_content.replace(old_pattern, f'src="{new_src}"')
            print(f"Replaced {file_path} with base64 data")
        else:
            print(f"Warning: Could not find base64 data for {file_path}")

    # Also fix the Precision Pet Log Cabin image if it exists
    if '../../../Product_images/Precision Pet Log Cabin Dog House.png' in html_content:
        print("Found Precision Pet Log Cabin image with relative path - this needs to be handled separately")

    # Write the fixed HTML
    with open('optimized_images.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("Image conversion completed!")

if __name__ == '__main__':
    fix_images()