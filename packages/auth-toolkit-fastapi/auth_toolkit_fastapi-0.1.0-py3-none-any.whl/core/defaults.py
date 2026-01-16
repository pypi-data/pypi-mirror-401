from dataclasses import dataclass
from pwdlib import PasswordHash

@dataclass
class AuthDefaults:
    secret_key: str = "CHANGE_ME"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    login_field: str = "email"
    password_field: str = "password"
    
    password_hash: PasswordHash = PasswordHash.recommended()

    user_id_field: str = "id"