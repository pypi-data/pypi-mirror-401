from datetime import datetime, timedelta
try:
    import jwt 
    from jwt.exceptions import InvalidTokenError 
except ImportError as exc:
    raise ImportError("jwt is required. Install it with: pip install jwt") from exc

from ..exceptions import JWTError

class JWTBackend:
    def __init__(self, secret_key, algorithm="HS256", expire_minutes=60):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def encode(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=self.expire_minutes))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode(self, token: str):
        try:

            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except InvalidTokenError as e:
            raise JWTError(f"Invalid token: {str(e)}") from e
    
