import os
import random
from PIL import Image, ImageDraw
from django.conf import settings

def create_sample_image(prompt, num_images, folder_name, location):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    images = []
    for i in range(num_images):
        img = Image.new('RGB', (300, 300), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        d = ImageDraw.Draw(img)
        d.text((10, 10), f"{prompt} {i+1}", fill=(255, 255, 255))
        img_path = os.path.join(folder_name, f"{prompt}_{i+1}.png")
        img.save(img_path)
        imag_location = os.path.join(location, f"{prompt}_{i+1}.png")
        images.append(imag_location)
    
    return images
