
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройка Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in ocr.py. Please set the environment variable.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

async def extract_text_from_image(image_path: str) -> str:
    """
    Извлекает весь видимый текст из изображения с помощью Gemini API.
    """
    try:
        print(f"Extracting text from: {image_path}")
        
        image_part = {
            "mime_type": "image/jpeg",
            "data": open(image_path, "rb").read()
        }
        
        # Простой промпт только для извлечения текста
        prompt = "Извлеки весь текст с этого изображения меню. Не делай ничего больше, просто верни сплошной текст."
        
        response = await model.generate_content_async([prompt, image_part])
        
        extracted_text = response.text
        print(f"Text extracted successfully. Length: {len(extracted_text)} chars.")
        return extracted_text.strip()

    except Exception as e:
        print(f"Error in OCR: {str(e)}")
        return ""
