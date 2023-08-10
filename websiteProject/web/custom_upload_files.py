import os
import datetime


def upload_file(instance, filename):
    # Get the original filename and extension
    original_name, extension = os.path.splitext(filename)

    # Create a new filename based on your logic
    new_filename = f"{instance.author_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}{extension}"

    if extension == ".docx":
        return os.path.join('static/books/', new_filename)
    else:
        return os.path.join('static/covers/', new_filename)
