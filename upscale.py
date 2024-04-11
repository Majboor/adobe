print("hello")
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

upload_folder = 'inputs'
result_folder = 'results'

os.makedirs(upload_folder, exist_ok=True)
os.makedirs(result_folder, exist_ok=True)

IMAGE_FORMATS = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')

device = torch.device('cpu')
print('device initialized before run:', device)

model_scale = "2" #@param ["2", "4", "8"] {allow-input: false}

model = RealESRGAN(device, scale=int(model_scale))
model.load_weights(f'weights/RealESRGAN_x{model_scale}.pth')

def image_to_tar_format(img, image_name):
    buff = BytesIO()
    if '.png' in image_name.lower():
        img = img.convert('RGBA')
        img.save(buff, format='PNG')
    else:
        img.save(buff, format='JPEG')
    buff.seek(0)
    fp = io.BufferedReader(buff)
    img_tar_info = tarfile.TarInfo(name=image_name)
    img_tar_info.size = len(buff.getvalue())
    return img_tar_info, fp

def process_tar(path_to_tar):
    processing_tar = tarfile.open(path_to_tar, mode='r')
    result_tar_path = os.path.join('results/', os.path.basename(path_to_tar))
    save_tar = tarfile.open(result_tar_path, 'w')

    for c, member in enumerate(processing_tar):
        print(f'{c}, processing {member.name}')

        if not member.name.endswith(IMAGE_FORMATS):
            continue

        try: 
            img_bytes = BytesIO(processing_tar.extractfile(member.name).read())
            img_lr = Image.open(img_bytes, mode='r').convert('RGB')
        except Exception as err:
            print(f'Unable to open file {member.name}, skipping')
            continue

        img_sr = model.predict(np.array(img_lr))
        # adding to save_tar
        img_tar_info, fp = image_to_tar_format(img_sr, member.name)
        save_tar.addfile(img_tar_info, fp)

    processing_tar.close()
    save_tar.close()    
    print(f'Finished! Archive saved to {result_tar_path}')
aspect_ratio = (16, 9)

def process_input(filename, image_counter):
    result_folder = 'results'
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    # Ensure that the image counter is unique
    while os.path.exists(os.path.join(result_folder, f'{image_counter}.png')):
        image_counter += 1

    result_image_path = os.path.join(result_folder, f'{image_counter}.png')

    try:
        image = Image.open(filename).convert('RGB')
        # Perform image processing operations here

        # Calculate new dimensions to maintain the specified aspect ratio
        width, height = image.size
        new_width = int((height / aspect_ratio[1]) * aspect_ratio[0])
        new_height = height
        image = image.resize((new_width, new_height))

        sr_image = model.predict(np.array(image))
        sr_image.save(result_image_path)
        print(f'Finished! Image saved to {result_image_path}')
    except Exception as e:
        print(f"Error: {e}")

def process_folder(input_folder):
    print("start processing")
    image_counter = 1  # Initialize the image counter to 1
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(".png"):
                filename = os.path.join(root, file)
                process_input(filename, image_counter)
                image_counter += 1  # Increment the image counter

# Specify the folder path you want to process
# folder_path = 'output'
# process_folder(folder_path)

# Specify the folder path you want to process
# folder_path = 'output'
# process_folder(folder_path)