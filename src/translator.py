def detect_language(extracted_text) -> str:
    """
    Определяет язык текста с помощью библиотеки langdetect.
    
    :param extracted_text: Извлеченный текст.
    :return: Код языка (например, 'en', 'fr', 'de').
    """
    try:
        from langdetect import detect
        return detect(extracted_text)
    except Exception as e:
        print(f"Ошибка при определении языка: {e}")
        return "unknown"

