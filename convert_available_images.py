#!/usr/bin/env python3
"""
Convert available grooming and dental images to base64
"""

import os
import base64
from pathlib import Path

def image_to_base64(image_path):
    """Convert image file to base64 string"""
    try:
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read())
            # Get MIME type
            ext = Path(image_path).suffix.lower()
            if ext in ['.jpg', '.jpeg']:
                mime_type = 'image/jpeg'
            elif ext == '.png':
                mime_type = 'image/png'
            elif ext == '.webp':
                mime_type = 'image/webp'
            else:
                mime_type = 'image/jpeg'  # default

            return f"data:{mime_type};base64,{encoded.decode('utf-8')}"
    except Exception as e:
        print(f"Error converting {image_path}: {e}")
        return None

def convert_images():
    """Convert all available images in grooming and dental folders"""
    base_dir = Path("C:/Users/tsalt/NEWEST_IDLS_HTML_FILE")

    # Process grooming images
    grooming_dir = base_dir / "Dog Grooming/Top_20_Dog_Grooming_Products/dog_grooming_product_images"
    if grooming_dir.exists():
        print(f"Converting grooming images from: {grooming_dir}")
        for img_file in grooming_dir.glob("*.jpg"):
            print(f"  - {img_file.name}")
            base64_data = image_to_base64(img_file)
            if base64_data:
                # Save base64 to a temp file for later use
                with open(f"C:/Users/tsalt/IDLS-NEW-REPOSITORY/grooming_images/{img_file.name}.b64", 'w') as f:
                    f.write(base64_data)

    # Process dental images
    dental_dir = base_dir / "Dog Dental/Top_20_Dog_Dental_Products/dog_dental_product_images"
    if dental_dir.exists():
        print(f"\nConverting dental images from: {dental_dir}")
        for img_file in dental_dir.glob("*.jpg"):
            print(f"  - {img_file.name}")
            base64_data = image_to_base64(img_file)
            if base64_data:
                # Save base64 to a temp file for later use
                with open(f"C:/Users/tsalt/IDLS-NEW-REPOSITORY/dental_images/{img_file.name}.b64", 'w') as f:
                    f.write(base64_data)

    print("\nDone converting images!")

if __name__ == "__main__":
    # Create directories for base64 files
    os.makedirs("C:/Users/tsalt/IDLS-NEW-REPOSITORY/grooming_images", exist_ok=True)
    os.makedirs("C:/Users/tsalt/IDLS-NEW-REPOSITORY/dental_images", exist_ok=True)

    convert_images()