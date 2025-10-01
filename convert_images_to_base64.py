#!/usr/bin/env python3
import re
import json

def extract_image_data():
    # Read the JS file
    with open('Dog Health/dog_health_images_base64.js', 'r', encoding='utf-8') as f:
        js_content = f.read()

    # Find all image entries using a more flexible pattern
    image_pattern = r"filename:\s*'([^']*?)'[^}]*?dataUri:\s*'([^']*?)'"
    matches = re.findall(image_pattern, js_content, re.DOTALL)

    # Create mapping
    image_map = {}
    for filename, data_uri in matches:
        image_map[filename] = data_uri
        # Also map by clean name
        clean_name = filename.replace('.jpg', '').replace('.png', '').replace('_', ' ')
        image_map[clean_name] = data_uri

    return image_map

def fix_html_images():
    # Read HTML file
    with open('optimized_images.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Get image data
    image_map = extract_image_data()

    # Images to replace
    replacements = [
        ('Dog Health/Purina Pro Plan Fortiflora Canine Probiotic Supplement.jpg', 'Purina Pro Plan Fortiflora Canine Probiotic'),
        ('Dog Health/Grizzly Salmon Oil for Dogs.jpg', 'Grizzly Salmon Oil for Dogs'),
        ('Dog Health/VetriScience GlycoFlex 3 Hip and Joint Support.jpg', 'VetriScience GlycoFlex 3 Hip and Joint Support'),
        ('Dog Health/Iams Minichunks Dog Food.jpg', 'Iams Minichunks Dog Food'),
        ('Dog Health/TruDog Dog Food.jpg', 'TruDog Dog Food'),
        ('../../../Product_images/Precision Pet Log Cabin Dog House.png', 'Precision Pet Log Cabin Dog House')
    ]

    # Replace each image
    for file_path, clean_name in replacements:
        if file_path in html_content:
            # Try to find base64 data
            base64_data = None

            # Try exact filename match
            if file_path in image_map:
                base64_data = image_map[file_path]
            # Try clean name match
            elif clean_name in image_map:
                base64_data = image_map[clean_name]
            # Try partial matches
            else:
                for key, value in image_map.items():
                    if clean_name.lower() in key.lower() or key.lower() in clean_name.lower():
                        base64_data = value
                        break

            if base64_data:
                old_pattern = f'src="{file_path}"'
                new_pattern = f'src="{base64_data}"'
                html_content = html_content.replace(old_pattern, new_pattern)
                print(f"+ Replaced {file_path}")
            else:
                print(f"- Could not find base64 data for {file_path}")

    # Write fixed HTML
    with open('optimized_images.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("Image conversion completed!")

if __name__ == '__main__':
    fix_html_images()