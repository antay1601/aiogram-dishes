def process_menu(extracted_text, language) -> str:
    """
    Обрабатывает меню, переводит его и возвращает в виде HTML.
    
    :param extracted_text: Извлеченный текст меню.
    :param language: Код языка текста.
    :return: Путь к сгенерированному HTML-файлу.
    """
    try:
        from src.menu_processor import process_menu  # Импортируем функцию из модуля menu_processor.py
        return process_menu(extracted_text, language)
    except Exception as e:
        print(f"Ошибка при обработке меню: {e}")
        return ""
        