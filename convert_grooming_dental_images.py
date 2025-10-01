#!/usr/bin/env python3
"""
Convert grooming and dental images from file paths to base64 encoding
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

def process_html_file():
    """Process the HTML file and convert image paths to base64"""
    html_file = Path("C:/Users/tsalt/IDLS-NEW-REPOSITORY/optimized_images.html")
    base_image_dir = Path("C:/Users/tsalt/NEWEST_IDLS_HTML_FILE")

    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find grooming and dental sections
    sections = [
        ('dog-grooming', 'Dog Grooming'),
        ('dog-dental', 'Dog Dental')
    ]

    for section_id, section_name in sections:
        print(f"\nProcessing {section_name} section...")

        # Find the section
        start_marker = f'<div id="{section_id}" class="content-section hidden">'
        end_marker = '<div id="'

        start_idx = content.find(start_marker)
        if start_idx == -1:
            print(f"Section {section_id} not found!")
            continue

        # Find end of section (next section starts)
        search_start = start_idx + len(start_marker)
        next_section_idx = content.find(end_marker, search_start)
        if next_section_idx == -1:
            # If no next section, look for closing divs
            next_section_idx = content.find('</div>', search_start + 1000)

        if next_section_idx == -1:
            print(f"Could not find end of {section_id} section")
            continue

        section_content = content[start_idx:next_section_idx]

        # Find all image tags with file paths
        import re
        img_pattern = r'<img[^>]+src="([^"]+\.jpg|[^"]+\.png|[^"]+\.jpeg|[^"]+\.webp)"[^>]*>'

        images = re.findall(img_pattern, section_content, re.IGNORECASE)
        print(f"Found {len(images)} images in {section_name} section")

        # Convert each image
        for img_path in images:
            # Skip if already base64
            if img_path.startswith('data:image'):
                continue

            # Construct full path
            full_path = base_image_dir / img_path

            if full_path.exists():
                print(f"  Converting: {img_path}")
                base64_data = image_to_base64(full_path)

                if base64_data:
                    # Replace in content
                    old_src = f'src="{img_path}"'
                    new_src = f'src="{base64_data}"'
                    content = content.replace(old_src, new_src)
                    print(f"    ✓ Converted successfully")
                else:
                    print(f"    ✗ Failed to convert")
            else:
                print(f"  ✗ File not found: {full_path}")

    # Write the updated content
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print("\n✅ HTML file updated successfully!")

if __name__ == "__main__":
    process_html_file()