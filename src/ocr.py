def extract_text_from_image(image_path: str) -> str:
    """
    Извлекает текст из изображения с помощью OCR.
    
    :param image_path: Путь к изображению.
    :return: Извлеченный текст.
    """
    try:
        from src.ocr import ocr_image  # Импортируем функцию из модуля ocr.py
        return ocr_image(image_path)
    except Exception as e:
        print(f"Ошибка при извлечении текста: {e}")
        return ""
