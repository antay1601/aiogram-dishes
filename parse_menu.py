import json
from pathlib import Path
from src.prompt_generator import generate_image_prompt

def parse_menu_data(file_path: str = "menu.json") -> list | None:
    """
    Читает JSON-файл с меню и возвращает его как список словарей.
    """
    menu_file = Path(file_path)
    if not menu_file.exists():
        print(f"Ошибка: Файл '{file_path}' не найден.")
        return None

    try:
        with open(menu_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content:
                print(f"Ошибка: Файл '{file_path}' пуст.")
                return None
            return json.loads(content)
    except json.JSONDecodeError:
        print(f"Ошибка: Не удалось декодировать JSON из файла '{file_path}'.")
        return None
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        return None

def update_menu_with_prompts(menu_data: list, menu_path: str = "menu.json"):
    """
    Обновляет меню, генерируя промпты для изображений для блюд.
    """
    if not isinstance(menu_data, list):
        print("Неверный формат данных меню.")
        return

    updated = False
    for dish in menu_data:
        # Генерируем промпт, если его нет, а картинка - плейсхолдер
        if dish.get("image") == "placeholder" and not dish.get("image_prompt"):
            description = dish.get("shortDescription")
            if description:
                prompt = generate_image_prompt(description)
                if prompt:
                    dish["image_prompt"] = prompt
                    updated = True
    
    if updated:
        try:
            with open(menu_path, 'w', encoding='utf-8') as f:
                json.dump(menu_data, f, ensure_ascii=False, indent=4)
            print(f"Файл меню '{menu_path}' обновлен с новыми промптами для изображений.")
        except Exception as e:
            print(f"Ошибка при сохранении обновленного меню: {e}")

def generate_html_menu(menu_data: list, output_path: str = "menu.html"):
    """
    Генерирует красивый и адаптивный HTML-файл из данных меню.
    """
    if not isinstance(menu_data, list) or not menu_data:
        print("Данные для генерации HTML отсутствуют или имеют неверный формат.")
        return

    from collections import defaultdict
    grouped_menu = defaultdict(list)
    for dish in menu_data:
        category = dish.get("category", "другое").capitalize()
        grouped_menu[category].append(dish)
    
    sorted_grouped_menu = dict(sorted(grouped_menu.items()))

    html_template = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Меню Ресторана</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; background-color: #f8f9fa; color: #343a40; }
        .container { max-width: 900px; margin: auto; background-color: #ffffff; padding: 20px 40px; border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.1); }
        h1 { text-align: center; color: #e63946; font-size: 2.8em; margin-bottom: 25px; font-weight: 700; }
        h2 { color: #1d3557; border-bottom: 3px solid #457b9d; padding-bottom: 10px; margin-top: 45px; font-size: 2.2em; }
        .dish { border-bottom: 1px solid #dee2e6; padding: 25px 10px; margin-bottom: 0; }
        .dish:last-child { border-bottom: none; }
        .dish-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px; flex-wrap: wrap; gap: 10px; }
        .dish-name { font-size: 1.6em; font-weight: 600; color: #005f73; }
        .dish-price { font-size: 1.5em; font-weight: 700; color: #343a40; white-space: nowrap; margin-left: 20px; }
        .original-name { font-style: italic; color: #6c757d; font-size: 0.95em; margin-bottom: 12px; }
        .description { font-size: 1.1em; margin-bottom: 15px; }
        .ingredients { font-size: 1em; color: #495057; }
        .allergens { margin-top: 15px; display: flex; gap: 20px; font-size: 0.9em; }
        .allergen-tag { background-color: #fff0f3; color: #d90429; padding: 4px 10px; border-radius: 15px; font-weight: 500; }
        .prompt-box { background-color: #e9ecef; border: 1px solid #ced4da; border-radius: 8px; padding: 15px; margin-top: 20px; font-family: 'Courier New', Courier, monospace; white-space: pre-wrap; word-wrap: break-word; }
        .prompt-title { font-weight: bold; color: #495057; margin-bottom: 10px; }
        @media (max-width: 600px) {
            .container { padding: 15px 20px; }
            h1 { font-size: 2.2em; }
            h2 { font-size: 1.8em; }
            .dish-name { font-size: 1.3em; }
            .dish-price { font-size: 1.2em; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Меню</h1>
        {% for category, dishes in menu.items() %}
            <section id="{{ category.lower() }}">
                <h2>{{ category }}</h2>
                {% for dish in dishes %}
                    <div class="dish">
                        <div class="dish-header">
                            <span class="dish-name">{{ dish.translatedName }}</span>
                            <span class="dish-price">{{ dish.price }}</span>
                        </div>
                        <p class="original-name">({{ dish.originalName }})</p>
                        <p class="description">{{ dish.shortDescription }}</p>
                        {% if dish.ingredients %}
                        <div class="ingredients">
                            <strong>Состав:</strong> {{ ", ".join(dish.ingredients) }}
                        </div>
                        {% endif %}
                        <div class="allergens">
                            {% if dish.containsMilk == 'yes' %}<span class="allergen-tag">🥛 Содержит молоко</span>{% endif %}
                            {% if dish.containsGluten == 'yes' %}<span class="allergen-tag">🌾 Содержит глютен</span>{% endif %}
                        </div>
                        {% if dish.image_prompt %}
                        <div class="prompt-box">
                            <div class="prompt-title">Промпт для генерации изображения:</div>
                            <code>{{ dish.image_prompt }}</code>
                        </div>
                        {% endif %}
                    </div>
                {% endfor %}
            </section>
        {% endfor %}
    </div>
</body>
</html>
    """
    
    from jinja2 import Template
    template = Template(html_template)
    html_content = template.render(menu=sorted_grouped_menu)
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML-меню успешно сохранено в файл: '{output_path}'")
    except Exception as e:
        print(f"Ошибка при сохранении HTML-файла: {e}")

if __name__ == "__main__":
    menu_items = parse_menu_data()
    
    if menu_items:
        update_menu_with_prompts(menu_items)
        updated_menu_items = parse_menu_data()
        if updated_menu_items:
            generate_html_menu(updated_menu_items)
