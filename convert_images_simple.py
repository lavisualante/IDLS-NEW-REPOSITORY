import os
import base64
import re
from pathlib import Path

def convert_image_to_base64(image_path, quality=85):
    """Convert an image file to optimized base64"""
    try:
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
            # Get file extension for mime type
            ext = Path(image_path).suffix.lower()
            if ext == '.png':
                mime_type = 'image/png'
            elif ext in ['.jpg', '.jpeg']:
                mime_type = 'image/jpeg'
            elif ext == '.webp':
                mime_type = 'image/webp'
            else:
                mime_type = 'image/jpeg'  # default

            # Encode to base64
            base64_data = base64.b64encode(image_data).decode('utf-8')
            return f"data:{mime_type};base64,{base64_data}"
    except Exception as e:
        print(f"Error converting {image_path}: {e}")
        return None

def process_html_file(html_file, output_file):
    """Convert all file-path images to base64 in HTML file"""

    # Read HTML file
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all image tags with file paths (not base64)
    # Pattern to match src attributes that don't start with "data:"
    img_pattern = r'<img[^>]*src="([^"]*(?:\.jpg|\.jpeg|\.png|\.webp))"[^>]*>'
    images = re.findall(img_pattern, content, re.IGNORECASE)

    print(f"Found {len(images)} images to convert:")

    converted_count = 0
    for img_path in images:
        # Skip if already base64 or data URI
        if img_path.startswith('data:') or img_path.startswith('http'):
            continue

        # Try different base paths
        base_paths = [
            "C:/Users/tsalt/IDLS-NEW-REPOSITORY/",
            "C:/Users/tsalt/NEWEST_IDLS_HTML_FILE/",
            "C:/Users/tsalt/",
            ""
        ]

        found_path = None
        for base_path in base_paths:
            test_path = os.path.join(base_path, img_path.replace('/', os.sep))
            if os.path.exists(test_path):
                found_path = test_path
                break

        if found_path:
            print(f"Converting: {img_path}")
            base64_data = convert_image_to_base64(found_path)
            if base64_data:
                # Replace the src attribute
                old_img_tag = f'src="{img_path}"'
                new_img_tag = f'src="{base64_data}"'
                content = content.replace(old_img_tag, new_img_tag)
                converted_count += 1
                print(f"  Converted successfully")
            else:
                print(f"  Failed to convert")
        else:
            print(f"  File not found: {img_path}")

    # Write updated HTML
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\nConversion complete! Converted {converted_count} images.")
    return converted_count

if __name__ == "__main__":
    html_file = "C:/Users/tsalt/IDLS-NEW-REPOSITORY/optimized_images.html"
    output_file = "C:/Users/tsalt/IDLS-NEW-REPOSITORY/optimized_images.html"

    process_html_file(html_file, output_file)