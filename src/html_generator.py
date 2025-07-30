def generate_html(processed_menu, html_path):
    """
    Генерирует HTML-файл из обработанного меню.
    
    :param processed_menu: Обработанное меню в виде строки.
    :param html_path: Путь к выходному HTML-файлу.
    """
    try:
        from src.html_generator import generate_html  # Импортируем функцию из модуля html_generator.py
        return generate_html(processed_menu, html_path)
    except Exception as e:
        print(f"Ошибка при генерации HTML: {e}")
        return ""
        