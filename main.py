#pip install realesrgan numpy  paramiko Pillow
import os
import requests
import re
import json
import os
import requests
from PIL import Image
from io import BytesIO
import pandas as pd
import requests
import time 
from ai import ai
# from api2 import ai
from notifications import post
from api import get_image_url
from api import get_task_id
from api import get_image
from api import fetchtask
from grid import chop_and_save_images
from grid import create_next_directory
import os
import shutil
from io import BytesIO
import io
import tarfile
from PIL import Image
from RealESRGAN import RealESRGAN
from PIL import Image
import numpy as np
import torch
from upscale import image_to_tar_format
from upscale import process_tar
from upscale import  process_input
from upscale import  process_folder
from upscale import  process_input
import os
import paramiko

directory = "output"

if not os.path.exists(directory):
    os.mkdir(directory)

categories = [
    'business',
    'finance',
    'AI Ml',
    'smart home',
    'future homes',
    'IOT',
    'architecture',
    'esthetics',
    'futuristic architecture',
    'AI effect on industries',
    'Neural networks',
    'IT future',
    'AI taking over',
    'AI chatbot',
    'food edible items',
    'health and hygiene',
    'fresh organic',
    'agriculture',
    'dream living',
    'luxury living',
    'travel vacation',
    'No Human',
    'water splash',
    'splashes color splash isolated on a white background',
    'microscopic bloop cells biology',
    'modern interior designs',
    'cars',
    'computers chips etc',
    'seasonal shots',
    'diseases',
    'world famous destinations',
    'weddings',
    'lungs',
    'time'
]


# Loop through the categories and call the function
prompts = []
for category in categories:
    raw_output = ai(category)
    prompts.append(raw_output)

print(prompts)
post(f"\n\n\n\n\n created all prompts sample prompt {prompts[0]}")

print("\n\n\n\n\nSample prompt", prompts[0])




def main():
    task_ids = []
    allimages = []
    # Assuming you populate 'task_ids' here.
    
    for query in prompts:
        print(query)
        task_id = get_task_id(query)
        time.sleep(45)
        print(task_id, "\n\n\n\n\nTaskID")
        task_ids.append(task_id)
    
    for i in task_ids:
        final_image = get_image_url(i)
        print(final_image, "\n\n\n\n\nTaskID")
        allimages.append(final_image)
        
    for o in allimages:
        chop_and_save_images(o)
    post(f"all image url {allimages[0]}")
    post(f"all task ids {task_ids[0]}")
    
        
main()

print("starting with image upscale")
folder_path = 'output'
process_folder(folder_path)





# hostname = "sftp.contributor.adobestock.com"
# port = 22
# username = "211732533"
# password = "+L;1uOoK"

# from PIL import Image
# import os

# Set the path to the folder containing the images
# folder_path = "results"

# # Define the target aspect ratio (16:9)
# target_aspect_ratio = 16 / 9

# # Iterate through all files in the folder
# for filename in os.listdir(folder_path):
#     if filename.endswith(".png"):
#         # Open the image using Pillow
#         image_path = os.path.join(folder_path, filename)
#         img = Image.open(image_path)

#         # Get the current image's width and height
#         width, height = img.size

#         # Calculate the new height to maintain the target aspect ratio
#         new_height = int(width / target_aspect_ratio)

#         # Resize the image to the new dimensions while maintaining the aspect ratio
#         img = img.resize((width, new_height), Image.ANTIALIAS)

#         # Save the modified image with the same filename
#         img.save(image_path)

# print("Images resized to 16:9 aspect ratio.")




import os
import requests
import re
import json
from PIL import Image
from io import BytesIO
import pandas as pd
import time
import shutil
import io
import tarfile
import numpy as np
import torch
import paramiko
import pickle
from notifications import post

# Replace with your SFTP server credentials
hostname = "sftp.contributor.adobestock.com"
port = 22
username = "211506274"
password = "{'rrB9oJ"

# Define the source folder containing the PNG files
source_folder = "results"
file_extension = ".png"
cache_file = "cache.pkl"

# Initialize an SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the SFTP server
ssh.connect(hostname, port, username, password)

# Create an SFTP client
sftp = ssh.open_sftp()

# Function to send files to the SFTP server
def send_file_to_sftp(file_path, remote_folder):
    remote_path = os.path.join(remote_folder, os.path.basename(file_path))
    sftp.put(file_path, remote_path)

try:
    # Check if the cache file exists. If it does, load the cache. If not, create an empty cache.
    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as cache_file:
            cache = pickle.load(cache_file)
    else:
        cache = set()

    # Iterate over files in the source folder
    for root, _, files in os.walk(source_folder):
        for file in files:
            if file.endswith(file_extension):
                file_path = os.path.join(root, file)

                # Check if the file is in the cache. If not, upload it and add it to the cache. If it's in the cache, skip it.
                if os.path.basename(file_path) not in cache:
                    # Send the file to the SFTP server
                    send_file_to_sftp(file_path, "/")

                    # Add the uploaded file to the cache
                    cache.add(os.path.basename(file_path))
                    print(f"Uploaded: {os.path.basename(file_path)}")
                else:
                    print(f"Skipping already uploaded: {os.path.basename(file_path)}")

finally:
    sftp.close()
    ssh.close()

# Save the updated cache to the cache file.
with open("cache.pkl", 'wb') as cache_file:
    pickle.dump(cache, cache_file)

post("All images uploaded to Adobe Stock")
   


