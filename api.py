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
def get_image_url(task_id):
    url = "https://midjourney-experience.p.rapidapi.com/task/"
    querystring = {"taskId": f"{task_id}"}

    headers = {
        "X-RapidAPI-Key": "786537afe1msh93a10609dcf7592p170f93jsn1bebd7133045",
        "X-RapidAPI-Host": "midjourney-experience.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=45)
        response_data = response.json()
        image_url = response_data.get("imageUrl")  # Use .get() to avoid KeyError
        return image_url
    except requests.exceptions.Timeout:
        # Handle timeout
        return None
    except KeyError:
        # Handle KeyErrors by returning None
        return None
        

def get_task_id(prompt):
    url = "https://midjourney-experience.p.rapidapi.com/imagine"

    payload = {"prompt": f"{prompt}"}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "786537afe1msh93a10609dcf7592p170f93jsn1bebd7133045",
        "X-RapidAPI-Host": "midjourney-experience.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()
    task_id = response_data["taskId"]

    return task_id
    

def get_image(i):
    retry_count = 0
    while retry_count < 3:
        print("Loop begin")  # Retry up to 3 times
        try:
            image_url = get_image_url(i)
            print(image_url)
            if image_url is None:
                print("Error: image_url is None")
                print("Skipping to the next task.")
                break
            print("Got image")
            # Perform your image processing logic here
        except Exception as e:
            print(f"Error while fetching image for task {i}: {str(e)}")
            if retry_count < 2:
                retry_count += 1
                wait_time = 75 if retry_count == 1 else 120  # 75 seconds for 1st retry, 120 seconds for 2nd retry
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print("Max retries reached for task {i}. Moving to the next task.")
                break

def fetchtask(query):
    retry_count = 0
    while retry_count < 3:  # Retry up to 3 times
        try:
            task_ids = get_task_id(query)  # Replace with your actual method for fetching task IDs
            return task_ids
        except Exception as e:
            print(f"Error while fetching task IDs for query '{query}': {str(e)}")
            if retry_count < 2:
                retry_count += 1
                wait_time = 75 if retry_count == 1 else 120  # 75 seconds for 1st retry, 120 seconds for 2nd retry
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"Max retries reached for query '{query}'. Skipping this query.")
                return []