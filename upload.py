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
