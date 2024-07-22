# Подключение из секретного файла
from dotenv import dotenv_values


def token(name: str) -> str:
    """Ф-я получает токен, по названию из файла .env"""
    config = dotenv_values(".env")
    return config[name]
