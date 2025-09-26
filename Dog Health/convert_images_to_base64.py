#!/usr/bin/env python3
"""
Convert all product images to optimized base64 format for web integration
"""

import os
import base64
from PIL import Image
import io

def image_to_base64(image_path, max_size=(400, 400), quality=85):
    """
    Convert image to optimized base64 string
    """
    try:
        # Open and optimize image
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            # Maintain aspect ratio while resizing
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            # Save to buffer with optimization
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=quality, optimize=True)
            buffer.seek(0)

            # Convert to base64
            base64_string = base64.b64encode(buffer.read()).decode('utf-8')
            return f"data:image/jpeg;base64,{base64_string}"

    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def process_images():
    """
    Process all product images in the Dog Health directory
    """
    dog_health_dir = r"D:\IDLS\Dog Leashes\IDLS site to be improved\improve it\Dog Health"

    # Image files mapping (filename in HTML -> actual filename)
    image_mapping = {
        "Zesty Paws 8-in-1 Multifunctional Bites.png": "Zesty Paws 8-in-1 Multifunctional Bites.png",
        "Purina Pro Plan Fortiflora Canine Probiotic Supplement.jpg": "Purina Pro Plan Fortiflora Canine Probiotic.jpg",
        "Nutramax Cosequin Maximum Strength Joint Support.jpg": "Nutramax Cosequin Maximum Strength Joint Support.jpg",
        "Nutramax Dasuquin with MSM Soft Chews.jpg": "Nutramax Dasuquin with MSM Soft Chews.jpg",
        "Nutramax Proviable-DC Digestive Health Supplement.jpg": "Nutramax Proviable-DC Digestive Health Supplement.jpg",
        "Native Pet Probiotic for Dogs.jpg": "Native Pet Probiotic for Dogs.jpg",
        "Dog Is Human DM-01™ Daily Multivitamin.jpg": "Dog Is Human DM-01™ Daily Multivitamin.jpg",
        "VetIQ Multivitamin Supplement for Dogs.jpg": "VetIQ Multivitamin Supplement for Dogs.jpg",
        "NaturVet All-in-One Dog Supplement.jpg": "NaturVet All-in-One Dog Supplement.jpg",
        "PetHonesty 10-for-1 Multivitamin with Glucosamine.jpg": "PetHonesty 10-for-1 Multivitamin with Glucosamine.jpg",
        "Doggie Dailies Glucosamine for Dogs.jpg": "Doggie Dailies Glucosamine for Dogs.jpg",
        "Grizzly Salmon Oil for Dogs.jpg": "Grizzly Salmon Oil.jpg",
        "VetriScience GlycoFlex 3 Hip and Joint Support.jpg": "VetriScience GlycoFlex 3.jpg",
        "Greenies Dental Dog Treats.jpg": "Greenies Dental Dog Treats.jpg",
        "Hills Science Diet Dog Food.jpg": "Hills Science Diet Dog Food.jpg",
        "Iams Minichunks Dog Food.jpg": "Iams Minichunks Dog Food.jpg",
        "Rachael Ray Nutrish Dog Food.jpg": "Rachael Ray Nutrish Dog Food.jpg",
        "TruDog Dog Food.jpg": "TruDog Dog Food.jpg",
        "Kin+Kind Dog Shampoo.jpg": "Kin+Kind Dog Shampoo.jpg",
        "Wild One Treat Pouch.jpg": "Wild One Treat Pouch.jpg"
    }

    base64_images = {}

    for html_filename, actual_filename in image_mapping.items():
        image_path = os.path.join(dog_health_dir, actual_filename)
        if os.path.exists(image_path):
            print(f"Processing: {actual_filename}")
            base64_data = image_to_base64(image_path)
            if base64_data:
                base64_images[html_filename] = base64_data
                print(f"+ Converted {actual_filename}")
            else:
                print(f"- Failed to convert {actual_filename}")
        else:
            print(f"- File not found: {actual_filename}")

    return base64_images

def update_html_with_base64():
    """
    Update the comprehensive HTML file with base64 images
    """
    # Get base64 images
    base64_images = process_images()

    # Read the comprehensive HTML file
    input_file = r"D:\IDLS\Dog Leashes\IDLS site to be improved\improve it\Dog Health\comprehensive_dog_health_section.html"
    output_file = r"D:\IDLS\Dog Leashes\IDLS site to be improved\improve it\Dog Health\comprehensive_dog_health_section_base64.html"

    with open(input_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Replace image paths with base64 data
    for html_filename, base64_data in base64_images.items():
        old_src = f'src="Dog Health/{html_filename}"'
        new_src = f'src="{base64_data}"'
        html_content = html_content.replace(old_src, new_src)

    # Write the updated HTML
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"\n+ Updated HTML with base64 images saved to: {output_file}")
    print(f"+ Processed {len(base64_images)} images successfully")

    return output_file

if __name__ == "__main__":
    update_html_with_base64()