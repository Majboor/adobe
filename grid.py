import os
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime

def chop_and_save_images(image_url):
    # Check and create the next directory within the "output" folder
    output_dir = create_next_directory("output")

    # Check and create the "bk" directory
    bk_dir = create_bk_directory()

    # Download the image from the URL
    response = requests.get(image_url)
    if response.status_code == 200:
        image_data = BytesIO(response.content)
        img = Image.open(image_data)

        # Get image dimensions
        width, height = img.size
        img_aspect_ratio = round(float(width) / float(height), 2)

        # Calculate dimensions of 4 images based on aspect ratio
        new_width = int(width / 2)
        new_height = int(new_width / img_aspect_ratio)

        # Create a subfolder in the output directory
        output_subdir = os.path.join(output_dir, "processed_images")
        os.makedirs(output_subdir, exist_ok=True)

        # Crop the image and save 4 new images in the subfolder
        for i in range(4):
            if i == 0:
                box = (0, 0, new_width, new_height)
            elif i == 1:
                box = (new_width, 0, width, new_height)
            elif i == 2:
                box = (0, new_height, new_width, height)
            elif i == 3:
                box = (new_width, new_height, width, height)
            img_crop = img.crop(box)
            new_filename = f"chopped_image_{i + 1}.png"
            img_crop.save(os.path.join(output_subdir, new_filename))

        # Also save backup images in the "bk" directory
        for i in range(4):
            bk_date_subdir = os.path.join(bk_dir, datetime.now().strftime("%Y-%m-%d"))
            os.makedirs(bk_date_subdir, exist_ok=True)
            img_crop.save(os.path.join(bk_date_subdir, f"backup_image_{i + 1}.png"))

        print("Done chopping and saving files in directory:", output_subdir)
    else:
        print("Failed to download the image. Please check the URL.")

def create_next_directory(base_dir):
    i = 1
    while True:
        dir_name = str(i)
        new_dir_path = os.path.join(base_dir, dir_name)
        if not os.path.exists(new_dir_path):
            os.makedirs(new_dir_path)
            return new_dir_path
        i += 1

def create_bk_directory():
    bk_dir = "bk"  # The "bk" directory outside of "output"
    return bk_dir

# Example usage:

