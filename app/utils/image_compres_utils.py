from PIL import Image
import os
import shutil
from werkzeug.utils import secure_filename
import uuid


MEDIA_FOLDER = 'app/static/media'

def generate_unique_filename(filename):
    ext = os.path.splitext(filename)[1]   # .jpg, .png etc.
    unique_name = f"{uuid.uuid4().hex}{ext}"   # e.g. "a3f1c2d9e8.jpg"
    return unique_name



def compress_image(image_file,user_id, output_size=(800, 800), quality=70):
    
    user_folder = os.path.join(MEDIA_FOLDER, f"user_{user_id}")
    os.makedirs(user_folder, exist_ok=True)
    
    
    filename = generate_unique_filename(secure_filename(image_file.filename))
    filepath = os.path.join(user_folder, filename)
    

    # Open the image
    image = Image.open(image_file)

    # Convert to RGB if not already
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    # Resize (optional)
    image.thumbnail(output_size)

    # Save compressed
    image.save(filepath, optimize=True, quality=quality)
    return filename


def delete_folder(user_id):
    user_folder = os.path.join(MEDIA_FOLDER, f"user_{user_id}")
    if os.path.exists(user_folder):
        shutil.rmtree(user_folder)
        
    
def delete_old_img(user_id, old_filename):
    if not old_filename:
        return
    
    filepath = os.path.join(MEDIA_FOLDER, f"user_{user_id}", old_filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    