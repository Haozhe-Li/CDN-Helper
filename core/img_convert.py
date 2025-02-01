from PIL import Image
import os

def is_image_file(file_path):
    """
    Check if a file is an image file.
    """
    try:
        Image.open(file_path)
        return True
    except:
        return False
    
def convert_to_webp(file_path):
    """
    convert common image jpg, jpeg, png to webp
    """
    if not is_image_file(file_path):
        return file_path
    
    img = Image.open(file_path)
    img = img.convert("RGB")

    img.save(file_path.replace(".jpg", ".webp").replace(".jpeg", ".webp").replace(".png", ".webp"), 'webp', quality=30)
    return file_path.replace(".jpg", ".webp").replace(".jpeg", ".webp").replace(".png", ".webp")