from app.storage.utils import get_boto_client, validate_file_size, validate_image_file, BUCKET_NAME, PUBLIC_ENDPOINT
from fastapi import HTTPException, UploadFile
from uuid import uuid4

DEFAULT_PROFILE_PHOTO = "https://images.lusparkl.foo/default_avatar.webp"

def build_profile_photo_url(object_key: str) -> str:
    if PUBLIC_ENDPOINT is None:
        raise HTTPException(status_code=500, detail="Public image endpoint is not configured.")
    
    return f"{PUBLIC_ENDPOINT.rstrip('/')}/{object_key}"

def upload_profile_photo(file: UploadFile, user_id: int, old_photo_url: str) -> str:
    validate_file_size(file)
    extension = validate_image_file(file)

    client = get_boto_client()

    object_key = f"{user_id}_{uuid4()}{extension}"

    if old_photo_url != DEFAULT_PROFILE_PHOTO:
        old_object_key = old_photo_url.split("/")[-1]
        client.delete_object(Bucket=BUCKET_NAME, Key=old_object_key)

    client.upload_fileobj(
        file.file,
        BUCKET_NAME,
        object_key,
        ExtraArgs={
            "ContentType": file.content_type
        }
    )

    return build_profile_photo_url(object_key)
