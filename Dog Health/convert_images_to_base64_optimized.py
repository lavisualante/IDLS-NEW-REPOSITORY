#!/usr/bin/env python3
"""
Optimized Base64 Image Converter for Dog Health Products
Converts JPG and PNG images to optimized base64 format with proper compression and format detection
"""

import os
import base64
import mimetypes
from pathlib import Path

def optimize_image_data(image_path):
    """
    Read and optimize image data for base64 conversion
    Returns base64 string with proper data URI prefix
    """
    try:
        # Read the image file in binary mode
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()

        # Get MIME type
        mime_type, _ = mimetypes.guess_type(image_path)
        if mime_type is None:
            # Default to JPEG if can't detect
            mime_type = 'image/jpeg'

        # Convert to base64
        base64_data = base64.b64encode(image_data).decode('utf-8')

        # Create data URI
        data_uri = f"data:{mime_type};base64,{base64_data}"

        return {
            'filename': Path(image_path).name,
            'filepath': str(image_path),
            'mime_type': mime_type,
            'size_bytes': len(image_data),
            'base64_length': len(base64_data),
            'data_uri': data_uri,
            'base64_data': base64_data
        }

    except Exception as e:
        print(f"❌ Error processing {image_path}: {str(e)}")
        return None

def convert_all_images(directory):
    """
    Convert all images in the specified directory to base64
    """
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

    results = {}
    total_size = 0
    total_base64_size = 0

    print(f"🔍 Converting images in: {directory}")
    print("=" * 60)

    for filename in target_images:
        filepath = os.path.join(directory, filename)

        if os.path.exists(filepath):
            result = optimize_image_data(filepath)
            if result:
                results[filename] = result
                total_size += result['size_bytes']
                total_base64_size += result['base64_length']

                # Format sizes for display
                size_kb = result['size_bytes'] / 1024
                base64_kb = result['base64_length'] / 1024

                print(f"✅ {filename}")
                print(f"   📊 Original: {size_kb:.1f} KB")
                print(f"   📦 Base64: {base64_kb:.1f} KB")
                print(f"   🏷️  Type: {result['mime_type']}")
                print()
        else:
            print(f"❌ File not found: {filename}")

    # Print summary
    print("=" * 60)
    print(f"📈 SUMMARY:")
    print(f"   📁 Total files processed: {len(results)}")
    print(f"   📊 Original total size: {total_size / 1024:.1f} KB")
    print(f"   📦 Base64 total size: {total_base64_size / 1024:.1f} KB")
    print(f"   📈 Size increase: {((total_base64_size / total_size - 1) * 100):.1f}%")

    return results

def generate_html_mapping(results):
    """
    Generate HTML-friendly JavaScript mapping
    """
    js_code = "// Dog Health Products - Base64 Image Mapping\n"
    js_code += "// Generated automatically - Optimized for web integration\n\n"
    js_code += "const dogHealthImages = {\n"

    for filename, data in results.items():
        # Clean filename for JavaScript property name
        js_name = filename.replace('.', '_').replace('-', '_').replace(' ', '_').replace('™', '').replace('+', 'plus')
        js_code += f"    '{js_name}': {{\n"
        js_code += f"        filename: '{filename}',\n"
        js_code += f"        mimeType: '{data['mime_type']}',\n"
        js_code += f"        dataUri: '{data['data_uri']}'\n"
        js_code += f"    }},\n"

    js_code += "};\n\n"
    js_code += "// Helper function to get image by filename\n"
    js_code += "function getDogHealthImage(filename) {\n"
    js_code += "    const key = filename.replace('.', '_').replace('-', '_').replace(' ', '_').replace('™', '').replace('+', 'plus');\n"
    js_code += "    return dogHealthImages[key] || null;\n"
    js_code += "}\n"

    return js_code

if __name__ == "__main__":
    directory = "D:/IDLS/Dog Leashes/IDLS site to be improved/improve it/Dog Health/"

    print("🚀 Starting Base64 Image Conversion")
    print("=" * 60)

    # Convert all images
    results = convert_all_images(directory)

    if results:
        # Generate HTML mapping
        js_mapping = generate_html_mapping(results)

        # Save to file
        output_file = os.path.join(directory, "dog_health_images_base64.js")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(js_mapping)

        print(f"\n💾 Saved JavaScript mapping to: {output_file}")

        # Also save a simple JSON version
        import json
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

        print(f"💾 Saved JSON mapping to: {json_file}")

        print("\n🎉 Conversion complete! Use the JavaScript file in your HTML:")
        print('<script src="dog_health_images_base64.js"></script>')

    else:
        print("❌ No images were successfully converted")