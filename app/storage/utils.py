import boto3
from dotenv import load_dotenv
from os import getenv
from fastapi import UploadFile, HTTPException
from pathlib import Path

load_dotenv()
ENDPOINT = getenv("CLOUDFLARE_ENDPOINT")
ACCESS_KEY_ID = getenv("CLOUDFLARE_ACCESS_KEY_ID")
ACCESS_KEY = getenv("CLOUDFLARE_ACCESS_KEY")
BUCKET_NAME = getenv("BUCKET_NAME")
PUBLIC_ENDPOINT = getenv("PUBLIC_ENDPOINT")

ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp"
}

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
}

def get_boto_client():
    return boto3.client(
    service_name="s3",
    endpoint_url=ENDPOINT,
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_KEY,
    region_name="auto"
)

def validate_file_size(file: UploadFile) -> str:
    MAX_SIZE = 5 * 1024 * 1024 #5 MB

    if file.size is not None and file.size > MAX_SIZE:
        raise HTTPException(status_code=413, detail="File is too large.")
    
def validate_image_file(file: UploadFile) -> str:
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Invalid image type")
    
    extension = Path(file.filename or "").suffix.lower

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file extension.")
    
    return extension
