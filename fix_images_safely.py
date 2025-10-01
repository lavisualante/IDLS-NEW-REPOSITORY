#!/usr/bin/env python3
"""
Fix grooming and dental images using a memory-efficient approach
"""

import os
import base64
import re
from pathlib import Path

def image_to_base64(image_path):
    """Convert image file to base64 string"""
    try:
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read())
            # Get MIME type
            ext = Path(image_path).suffix.lower()
            if ext == '.jpg' or ext == '.jpeg':
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

def process_line_by_line():
    """Process the HTML file line by line to save memory"""
    html_file = "C:/Users/tsalt/IDLS-NEW-REPOSITORY/optimized_images.html"
    temp_file = "C:/Users/tsalt/IDLS-NEW-REPOSITORY/optimized_images_temp.html"
    base_image_dir = Path("C:/Users/tsalt/NEWEST_IDLS_HTML_FILE")

    # Track which section we're in
    in_grooming = False
    in_dental = False

    with open(html_file, 'r', encoding='utf-8') as infile, open(temp_file, 'w', encoding='utf-8') as outfile:
        for line_num, line in enumerate(infile, 1):
            # Check which section we're entering
            if 'id="dog-grooming"' in line:
                in_grooming = True
                in_dental = False
                print(f"\nEntered grooming section at line {line_num}")
            elif 'id="dog-dental"' in line:
                in_dental = True
                in_grooming = False
                print(f"\nEntered dental section at line {line_num}")
            elif 'id="dog-' in line and ('content-section' in line):
                # Left a section
                if in_grooming:
                    print(f"Left grooming section at line {line_num}")
                    in_grooming = False
                elif in_dental:
                    print(f"Left dental section at line {line_num}")
                    in_dental = False

            # Process images in grooming and dental sections
            if in_grooming or in_dental:
                # Look for image tags with file paths
                img_pattern = r'src="([^"]+\.(jpg|jpeg|png|webp))"'
                matches = re.finditer(img_pattern, line, re.IGNORECASE)

                for match in matches:
                    img_path = match.group(1)
                    # Skip if already base64
                    if img_path.startswith('data:image'):
                        continue

                    # Construct full path
                    full_path = base_image_dir / img_path
                    if full_path.exists():
                        print(f"  Converting: {img_path}")
                        base64_data = image_to_base64(full_path)

                        if base64_data:
                            # Replace in line
                            line = line.replace(f'src="{img_path}"', f'src="{base64_data}"')
                            print(f"    [OK] Converted successfully")
                        else:
                            print(f"    [ERROR] Failed to convert")
                    else:
                        print(f"  [NOT FOUND]: {full_path}")

            # Write the line (modified or not)
            outfile.write(line)

    # Replace original with temp file
    os.replace(temp_file, html_file)
    print("\n✅ HTML file updated successfully!")

if __name__ == "__main__":
    process_line_by_line()