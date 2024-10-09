import jwt
from datetime import datetime, timedelta, timezone

def create_access_token(data: dict,  expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, "secret_key", algorithm='HS256')
    return encoded_jwt

def validate_token(headers):
    authorization_header = headers.get('authorization')
    token = authorization_header[7:] if authorization_header and authorization_header.startswith("Bearer ") else None
    return token