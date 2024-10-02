Requirements

Make sure to install the libraries:
bash

pip install Pillow piexif

Simple Python Script
python

from PIL import Image
import piexif

def analyze_image(file_path):
    print(f"Analyzing {file_path}...\n")

    # Open the image
    try:
        img = Image.open(file_path)
        print(f"Format: {img.format}, Size: {img.size}, Mode: {img.mode}")

        # Check basic properties
        if img.format not in ['JPEG', 'PNG']:
            print("Warning: Unrecognized image format!")
            
        # Check EXIF data
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
    file_path = input("Enter the path of the image file to analyze: ")
    analyze_image(file_path)
