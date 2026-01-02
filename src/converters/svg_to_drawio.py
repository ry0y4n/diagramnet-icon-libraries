#!/usr/bin/env python3
"""
SVG to diagrams.net Custom Library Converter

Converts SVG files to diagrams.net custom library XML format.
"""

import base64
import json
import re
import zlib
from pathlib import Path
from urllib.parse import quote
from xml.etree import ElementTree as ET


def get_svg_dimensions(svg_content: str) -> tuple[int, int]:
    """
    Extract width and height from SVG content.
    
    Args:
        svg_content: SVG file content as string
        
    Returns:
        Tuple of (width, height) in pixels. Defaults to (48, 48) if not found.
    """
    try:
        # Remove XML declaration for parsing
        svg_content_clean = re.sub(r'<\?xml[^>]*\?>', '', svg_content)
        root = ET.fromstring(svg_content_clean)

        # Get width/height attributes
        width_str = root.get('width', '48')
        height_str = root.get('height', '48')

        # Remove units and convert to int
        width = int(float(re.sub(r'[^0-9.]', '', width_str) or 48))
        height = int(float(re.sub(r'[^0-9.]', '', height_str) or 48))

        return width, height
    except Exception:
        return 48, 48


def svg_to_mxgraph_xml(svg_content: str, width: int, height: int) -> str:
    """
    Convert SVG content to mxGraph XML format.
    
    Args:
        svg_content: SVG file content as string
        width: Icon width in pixels
        height: Icon height in pixels
        
    Returns:
        mxGraph XML string
    """
    # Base64 encode SVG
    svg_base64 = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')

    # URL encode for draw.io format
    svg_data = quote(svg_base64, safe='')

    # Create mxGraph XML structure
    mxgraph_xml = f'''<mxGraphModel>
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    <mxCell id="2" value="" style="shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image=data:image/svg+xml,{svg_data};" vertex="1" parent="1">
      <mxGeometry width="{width}" height="{height}" as="geometry"/>
    </mxCell>
  </root>
</mxGraphModel>'''

    return mxgraph_xml


def compress_and_encode(xml_content: str) -> str:
    """
    Compress XML using deflate and encode to Base64.
    
    Args:
        xml_content: XML string to compress
        
    Returns:
        Base64-encoded compressed string
    """
    # Deflate compression (raw deflate, no header)
    compressed = zlib.compress(xml_content.encode('utf-8'), level=9)[2:-4]
    # Base64 encode
    encoded = base64.b64encode(compressed).decode('utf-8')
    return encoded


def create_library_entry(
    svg_content: str,
    title: str,
    max_size: int = 80
) -> dict:
    """
    Create a single library entry from SVG content.
    
    Args:
        svg_content: SVG file content as string
        title: Display title for the icon
        max_size: Maximum icon size (will scale down if larger)
        
    Returns:
        Dictionary representing a library entry
    """
    # Get dimensions
    width, height = get_svg_dimensions(svg_content)

    # Scale down if too large
    if width > max_size or height > max_size:
        scale = max_size / max(width, height)
        width = int(width * scale)
        height = int(height * scale)

    # Convert to mxGraph XML
    mxgraph_xml = svg_to_mxgraph_xml(svg_content, width, height)

    # Compress and encode
    encoded_xml = compress_and_encode(mxgraph_xml)

    return {
        "xml": encoded_xml,
        "w": width,
        "h": height,
        "title": title,
        "aspect": "fixed"
    }


def create_library_entry_from_file(
    svg_path: Path,
    max_size: int = 80
) -> dict:
    """
    Create a library entry from an SVG file.
    
    Args:
        svg_path: Path to SVG file
        max_size: Maximum icon size
        
    Returns:
        Dictionary representing a library entry
    """
    svg_content = svg_path.read_text(encoding='utf-8')
    
    # Generate title from filename
    title = svg_path.stem.replace('-', ' ').replace('_', ' ').title()
    
    return create_library_entry(svg_content, title, max_size)


def create_library_xml(entries: list[dict]) -> str:
    """
    Generate Draw.io library XML from entries.
    
    Args:
        entries: List of library entry dictionaries
        
    Returns:
        Complete library XML string
    """
    # JSON array format (draw.io format)
    json_content = json.dumps(entries, ensure_ascii=False, separators=(',', ':'), sort_keys=True)

    # Wrap in mxlibrary format
    library_xml = f'<mxlibrary>{json_content}</mxlibrary>'

    return library_xml


def convert_svg_folder_to_library(
    svg_folder: Path,
    output_path: Path,
    max_size: int = 80
) -> list[str]:
    """
    Convert all SVG files in a folder to a Draw.io library.
    
    Args:
        svg_folder: Path to folder containing SVG files
        output_path: Path to save the library XML
        max_size: Maximum icon size
        
    Returns:
        List of successfully converted file names
    """
    svg_files = sorted(svg_folder.glob('*.svg'))
    
    if not svg_files:
        raise ValueError(f"No SVG files found in {svg_folder}")
    
    entries = []
    converted = []
    
    for svg_file in svg_files:
        try:
            entry = create_library_entry_from_file(svg_file, max_size)
            entries.append(entry)
            converted.append(svg_file.name)
        except Exception as e:
            print(f"  ✗ {svg_file.name}: {e}")
    
    # Generate and save library
    library_xml = create_library_xml(entries)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(library_xml, encoding='utf-8')
    
    return converted


if __name__ == "__main__":
    # Simple test
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python svg_to_drawio.py <svg_folder> <output.xml>")
        sys.exit(1)
    
    svg_folder = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    
    print(f"Converting SVGs from {svg_folder}...")
    converted = convert_svg_folder_to_library(svg_folder, output_path)
    print(f"✓ Converted {len(converted)} icons to {output_path}")
