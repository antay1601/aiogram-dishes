import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# Путь к вашему JSON-ключу
SERVICE_ACCOUNT_FILE = 'aiogram-dishes-6bacb9c855e0.json'

# Создание OAuth-токена

SCOPES = ['https://www.googleapis.com/auth/generative-language']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

credentials.refresh(Request())
token = credentials.token

# Пример запроса — список моделей
headers = {
    'Authorization': f'Bearer {token}',
}

response = requests.get(
    'https://generativelanguage.googleapis.com/v1beta/models',
    headers=headers
)

print("Доступные модели:")
print(json.dumps(response.json(), indent=2))
