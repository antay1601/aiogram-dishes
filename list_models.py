import os
import google.generativeai as genai
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Убедитесь, что GOOGLE_API_KEY установлен
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Please set the environment variable.")

# Конфигурируем API-ключ
genai.configure(api_key=api_key)

print("Fetching available models...\n")

try:
    # Получаем и выводим список моделей
    for m in genai.list_models():
        # Проверяем, поддерживает ли модель метод 'generateContent'
        if 'generateContent' in m.supported_generation_methods:
            print(f"Model name: {m.name}")
            print(f"  Display name: {m.display_name}")
            print(f"  Description: {m.description}")
            print("-" * 20)

except Exception as e:
    print(f"An error occurred while fetching models: {e}")

