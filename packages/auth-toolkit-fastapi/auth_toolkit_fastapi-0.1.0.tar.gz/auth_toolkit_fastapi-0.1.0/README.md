# Auth Toolkit

Flexible authentication module for Python applications.

Гибкий модуль аутентификации для Python приложений.

## Installation / Установка

```bash
pip install auth-toolkit-fastapi
```

For WebSocket support / С поддержкой WebSocket:

```bash
pip install auth-toolkit-fastapi[websocket]
```

## Quick Start / Быстрый старт

```python
from auth_toolkit_fastapi import Auth, DefaultMethods

# Create your own methods class
# Создайте собственный класс методов
class MyMethods(DefaultMethods):
    @staticmethod
    def get_user(username: str):
        # Your user retrieval logic
        # Ваша логика получения пользователя
        return user_object

# Initialize
# Инициализация
auth = Auth(
    methods=MyMethods(),
    secret_key="your-secret-key",
    access_token_expire_minutes=60
)

# Login
# Логин
result = auth.login({"email": "user@example.com", "password": "password"})
# Returns: {"access_token": "...", "token_type": "bearer"}

# Get user from token
# Получение пользователя из токена
user_id = auth.get_user_from_token(token)
```

## Features / Возможности

- 🔐 JWT token authentication
- 🔑 Flexible password hashing with pwdlib
- 🔌 Plugin system (WebSocket support included)
- ⚙️ Configurable authentication methods
- 🎯 Easy to extend and customize

## Project Structure / Структура проекта

- `core/` - Core authentication classes
- `exceptions/` - Custom exceptions
- `plugins/` - Plugins (e.g., WebSocket)

## Requirements / Требования

- Python >= 3.8
- jwt >= 2.0.0
- pwdlib >= 1.0.0
- fastapi >= 0.100.0 (optional, for WebSocket plugin)

## License

MIT License - see LICENSE file for details.
