from .defaults import AuthDefaults

password_hash = AuthDefaults.password_hash

class DefaultMethods:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return password_hash.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return password_hash.hash(password)

    @staticmethod
    def get_user(username: str):
        raise NotImplementedError('')
    
