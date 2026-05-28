import jwt
from app.auth.helpers import SECRET_KEY, ALGORITHM

def create_invite_token(workspace_id: int) -> str:
    return jwt.encode(
        {"workspace_id": workspace_id},
        SECRET_KEY,
        ALGORITHM
    )

def encode_invite_token(token):
    return jwt.decode(token, SECRET_KEY, ALGORITHM)