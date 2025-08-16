import os
import google.generativeai as genai
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Убедитесь, что GEMINI_API_KEY установлен
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Please set the environment variable.")

# Конфигурируем API-ключ
genai.configure(api_key=api_key)

prompt = "Tell me a short, fun fact about the Roman Empire."

print("Initializing model and generating text...")

try:
    # 1. Создаем модель
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    # 2. Вызываем метод generate_content
    response = model.generate_content(prompt)

    # 3. Печатаем текстовый ответ
    if response.text:
        print("Generated text:")
        print(response.text)
    else:
        print("No text was generated.")
        if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
            print(f"Prompt feedback: {response.prompt_feedback}")

except Exception as e:
    print(f"An error occurred: {e}")
    print("Please check your API key, model access rights, and the model name.")