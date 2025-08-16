from typing import List, Dict

def generate_html_menu(dishes: List[Dict], title: str = "Меню") -> str:
    """
    Генерирует HTML-страницу с карточками блюд.
    """
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f4f4f9;
                color: #333;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
            }}
            h1 {{
                text-align: center;
                color: #4a4a4a;
            }}
            .category-section {{
                margin-bottom: 40px;
            }}
            .category-title {{
                font-size: 2em;
                border-bottom: 2px solid #ddd;
                padding-bottom: 10px;
                margin-bottom: 20px;
                color: #333;
            }}
            .dish-card {{
                display: flex;
                background-color: #fff;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                margin-bottom: 20px;
                overflow: hidden;
                transition: transform 0.2s;
            }}
            .dish-card:hover {{
                transform: translateY(-5px);
            }}
            .dish-image {{
                width: 200px;
                height: 200px;
                object-fit: cover;
            }}
            .dish-info {{
                padding: 20px;
                flex-grow: 1;
                display: flex;
                flex-direction: column;
            }}
            .dish-name {{
                font-size: 1.5em;
                margin: 0 0 10px;
                color: #d35400;
            }}
            .dish-description {{
                font-size: 1em;
                margin: 0 0 15px;
                color: #555;
                flex-grow: 1;
            }}
            .dish-ingredients {{
                font-style: italic;
                color: #777;
                margin-bottom: 15px;
            }}
            .dish-details {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: auto;
            }}
            .dish-price {{
                font-size: 1.2em;
                font-weight: bold;
                color: #27ae60;
                margin: 0;
            }}
            .dish-allergens {{
                font-size: 0.8em;
                text-align: right;
                color: #888;
            }}
            .dish-allergens span {{
                display: block;
            }}
            .allergen-yes {{ color: #c0392b; font-weight: bold; }}
            .allergen-no {{ color: #27ae60; }}
            .allergen-unknown {{ color: #7f8c8d; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{title}</h1>
    """

    # Группируем блюда по категориям
    categories = {}
    for dish in dishes:
        # Принудительно преобразуем категорию в строку, чтобы избежать ошибки
        category_val = dish.get("category", "Без категории")
        if not isinstance(category_val, str):
            category = str(category_val)
        else:
            category = category_val

        if category not in categories:
            categories[category] = []
        categories[category].append(dish)

    # Создаем секции для каждой категории
    for category, cat_dishes in categories.items():
        html_content += f"""
        <div class="category-section">
            <h2 class="category-title">{category}</h2>
        """
        for dish in cat_dishes:
            image_url = dish.get("image") or "https://via.placeholder.com/200"
            
            # Получаем цену как есть
            price_str = dish.get('price', '')

            # Определяем классы для аллергенов
            gluten_status = dish.get('containsGluten', 'unknown')
            milk_status = dish.get('containsMilk', 'unknown')
            gluten_class = f"allergen-{gluten_status.lower()}"
            milk_class = f"allergen-{milk_status.lower()}"

            html_content += f"""
            <div class="dish-card">
                <img src="{image_url}" alt="{dish.get('translatedName', '')}" class="dish-image">
                <div class="dish-info">
                    <h3 class="dish-name">{dish.get('translatedName', 'Название не указано')}</h3>
                    <p class="dish-description">{dish.get('shortDescription', '')}</p>
                    <p class="dish-ingredients"><strong>Состав:</strong> {', '.join(dish.get('ingredients', []))}</p>
                    <div class="dish-details">
                        <p class="dish-price">{price_str}</p>
                        <div class="dish-allergens">
                            <span class="{gluten_class}">Глютен: {gluten_status}</span>
                            <span class="{milk_class}">Молоко: {milk_status}</span>
                        </div>
                    </div>
                </div>
            </div>
            """
        html_content += "</div>"

    html_content += """
        </div>
    </body>
    </html>
    """
    return html_content