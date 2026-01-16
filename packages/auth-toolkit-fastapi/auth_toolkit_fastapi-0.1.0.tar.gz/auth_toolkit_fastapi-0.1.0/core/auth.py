from .defaults import AuthDefaults
from .config import merge_defaults
from .methods import DefaultMethods
from .tokens import JWTBackend

class Auth:
    def __init__(
        self,
        *,
        methods: DefaultMethods = None,
        token_backend=None,
        **overrides
    ):
        self.config = merge_defaults(AuthDefaults(), overrides)

        self.methods = methods or DefaultMethods()

        self.token_backend = token_backend or JWTBackend(
            secret_key=self.config.secret_key,
            algorithm=self.config.algorithm,
            expire_minutes=self.config.access_token_expire_minutes,
        )
    
    def login(self, data: dict):
        login_value = data.get(self.config.login_field)
        password = data.get(self.config.password_field)

        user = self.methods.get_user(login_value)
        if not user:
            return None

        if not self.methods.verify_password(password, user.password):
            return None

        token = self.create_access_token(user)
        return {"access_token": token, "token_type": "bearer"}

    # ---------------- TOKENS ----------------

    def create_access_token(self, user):
        user_id = getattr(user, self.config.user_id_field)

        return self.token_backend.encode(
            {"sub": str(user_id)}
        )

    def get_user_from_token(self, token: str):
        payload = self.token_backend.decode(token)
        user_id = payload.get("sub")
        return user_id