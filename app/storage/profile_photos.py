from app.storage.utils import get_boto_client, validate_file_size, validate_image_file, BUCKET_NAME, PUBLIC_ENDPOINT
from fastapi import UploadFile
from uuid import uuid4

def upload_profile_photo(file: UploadFile, user_id: int) -> str:
    validate_file_size(file)
    extension = validate_image_file(file)

    client = get_boto_client()

    object_key = f"{user_id}_{uuid4()}{extension}"

    client.upload_fileobj(
        file.file,
        BUCKET_NAME,
        object_key,
        ExtraArgs={
            "ContentType": file.content_type
        }
    )

    return f"{PUBLIC_ENDPOINT}/{object_key}"

