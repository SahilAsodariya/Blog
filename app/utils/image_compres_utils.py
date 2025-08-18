from flask import request
from PIL import Image
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'app/static/uploads'
PROFILE_PICTURES_FOLDER = 'app/static/profile_pictures'

def compress_image(image_file, output_size=(800, 800), quality=70):
    filename = secure_filename(image_file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)

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

def compress_profile_pic(image_file, output_size=(800, 800), quality=70):
    filename = secure_filename(image_file.filename)
    filepath = os.path.join(PROFILE_PICTURES_FOLDER, filename)

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
