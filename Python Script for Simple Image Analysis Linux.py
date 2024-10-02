Here’s a Python script that uses PIL, Piexif, and subprocess to analyze images on Linux.
Requirements

Make sure you have the required libraries:
bash

pip install Pillow piexif

Python Script
python

from PIL import Image
import piexif
import subprocess
import sys

def analyze_image(file_path):
    print(f"Analyzing {file_path}...\n")

    # Verify the file type
    print("Checking file type...")
    file_type = subprocess.run(['file', file_path], capture_output=True, text=True)
    print(file_type.stdout)

    # Open the image
    try:
        img = Image.open(file_path)
        print(f"Format: {img.format}, Size: {img.size}, Mode: {img.mode}")

        # Check for EXIF data
        exif_data = piexif.load(img.info["exif"]) if "exif" in img.info else None
        if exif_data:
            print("EXIF data:")
            for ifd in exif_data:
                for tag in exif_data[ifd]:
                    print(f"  {piexif.TAGS[ifd][tag]['name']}: {exif_data[ifd][tag]}")
        else:
            print("No EXIF data found.")

    except Exception as e:
        print(f"Error analyzing image: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python image_analyzer.py <path_to_image>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    analyze_image(file_path)
