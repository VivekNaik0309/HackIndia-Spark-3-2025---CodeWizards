import os
import shutil
from fastapi import UploadFile

UPLOAD_FOLDER = "uploaded_docs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

async def save_uploaded_file(file: UploadFile):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path
