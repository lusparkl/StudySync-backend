import jwt
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
import os


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

config_data = {"GOOGLE_CLIENT_ID": GOOGLE_CLIENT_ID, "GOOGLE_CLIENT_SECRET": GOOGLE_CLIENT_SECRET}
starlete_config = Config(environ=config_data)

oauth = OAuth(starlete_config)

oauth.register(
    name = "google",
    server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"}
              )

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def hash_password(password: str) -> str:
    password_hash = PasswordHash.recommended()

    return password_hash.hash(password)

def verify_password(password: str, hash: str) -> bool:
    password_hash = PasswordHash.recommended()

    return password_hash.verify(password, hash)

def create_access_token(user_id: int) -> str:
    data = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(days=10)
    }

    return jwt.encode(data, SECRET_KEY, ALGORITHM) 
    
def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, ALGORITHM)
    except jwt.ExpiredSignatureError:
        return None
    
