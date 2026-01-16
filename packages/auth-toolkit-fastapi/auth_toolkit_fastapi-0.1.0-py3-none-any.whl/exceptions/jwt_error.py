class JWTError(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)
        self.message = message
            
    def __reduce__(self):
        return (JWTError, (self.message,))