#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Base64 Image Converter for Dog Health Products
Converts JPG and PNG images to base64 format
"""

import os
import base64
import mimetypes
import json
from pathlib import Path

def convert_image_to_base64(image_path):
    """Convert image to base64 data URI"""
    try:
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()

        # Get MIME type
        mime_type, _ = mimetypes.guess_type(image_path)
        if mime_type is None:
            mime_type = 'image/jpeg'

        # Convert to base64
        base64_data = base64.b64encode(image_data).decode('utf-8')
        data_uri = f"data:{mime_type};base64,{base64_data}"

        return {
            'filename': Path(image_path).name,
            'mime_type': mime_type,
            'size_bytes': len(image_data),
            'base64_length': len(base64_data),
            'data_uri': data_uri,
            'base64_data': base64_data
        }

    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return None

def main():
    directory = "D:/IDLS/Dog Leashes/IDLS site to be improved/improve it/Dog Health/"

    target_images = [
        "Dog Is Human DM-01™ Daily Multivitamin.jpg",
        "Doggie Dailies Glucosamine for Dogs.jpg",
        "Greenies Dental Dog Treats.jpg",
        "Grizzly Salmon Oil.jpg",
        "Hills Science Diet Dog Food.jpg",
        "Kin+Kind Dog Shampoo.jpg",
        "Native Pet Probiotic for Dogs.jpg",
        "NaturVet All-in-One Dog Supplement.jpg",
        "Nutramax Cosequin Maximum Strength Joint Support.jpg",
        "Nutramax Dasuquin with MSM Soft Chews.jpg",
        "Nutramax Proviable-DC Digestive Health Supplement.jpg",
        "PetHonesty 10-for-1 Multivitamin with Glucosamine.jpg",
        "Purina Pro Plan Fortiflora Canine Probiotic.jpg",
        "Rachael Ray Nutrish Dog Food.jpg",
        "VetIQ Multivitamin Supplement for Dogs.jpg",
        "VetriScience GlycoFlex 3.jpg",
        "Wild One Treat Pouch.jpg",
        "Zesty Paws 8-in-1 Multifunctional Bites.png",
        "Zesty Paws Dog Multivitamin.jpg"
    ]

    print("Converting images to base64...")
    print("=" * 50)

    results = {}
    total_original = 0
    total_base64 = 0

    for filename in target_images:
        filepath = os.path.join(directory, filename)

        if os.path.exists(filepath):
            result = convert_image_to_base64(filepath)
            if result:
                results[filename] = result
                total_original += result['size_bytes']
                total_base64 += result['base64_length']

                print(f"[OK] {filename}")
                print(f"     Original: {result['size_bytes'] / 1024:.1f} KB")
                print(f"     Base64: {result['base64_length'] / 1024:.1f} KB")
                print(f"     Type: {result['mime_type']}")
                print()
            else:
                print(f"[FAIL] {filename}")
        else:
            print(f"[MISSING] {filename}")

    print("=" * 50)
    print(f"SUMMARY:")
    print(f"Files processed: {len(results)}")
    print(f"Total original size: {total_original / 1024:.1f} KB")
    print(f"Total base64 size: {total_base64 / 1024:.1f} KB")
    print(f"Size increase: {((total_base64 / total_original - 1) * 100):.1f}%")

    if results:
        # Generate JavaScript mapping
        js_code = "// Dog Health Products - Base64 Image Mapping\n"
        js_code += "// Generated automatically\n\n"
        js_code += "const dogHealthImages = {\n"

        for filename, data in results.items():
            js_name = filename.replace('.', '_').replace('-', '_').replace(' ', '_').replace('™', '').replace('+', 'plus')
            js_code += f"    '{js_name}': {{\n"
            js_code += f"        filename: '{filename}',\n"
            js_code += f"        mimeType: '{data['mime_type']}',\n"
            js_code += f"        dataUri: '{data['data_uri']}'\n"
            js_code += f"    }},\n"

        js_code += "};\n\n"
        js_code += "function getDogHealthImage(filename) {\n"
        js_code += "    const key = filename.replace('.', '_').replace('-', '_').replace(' ', '_').replace('™', '').replace('+', 'plus');\n"
        js_code += "    return dogHealthImages[key] || null;\n"
        js_code += "}\n"

        # Save JavaScript file
        js_file = os.path.join(directory, "dog_health_images_base64.js")
        with open(js_file, 'w', encoding='utf-8') as f:
            f.write(js_code)
        print(f"\nSaved JavaScript mapping to: {js_file}")

        # Save JSON file
        json_output = {}
        for filename, data in results.items():
            json_output[filename] = {
                'dataUri': data['data_uri'],
                'mimeType': data['mime_type'],
                'sizeBytes': data['size_bytes']
            }

        json_file = os.path.join(directory, "dog_health_images_base64.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_output, f, indent=2, ensure_ascii=False)
        print(f"Saved JSON mapping to: {json_file}")

        print("\nTo use in HTML:")
        print('<script src="dog_health_images_base64.js"></script>')
        print("Then use: getDogHealthImage('filename.jpg').dataUri")

if __name__ == "__main__":
    main()