

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
import os
import re
import asyncio
from datetime import datetime
from bot import bot
from ocr import extract_text_from_image
from menu_processor import process_menu_section
from image_generator import get_image_url
from html_generator import generate_html_menu

router = Router()

def register_handlers(dp):
    dp.include_router(router)

def split_text_into_sections(text: str) -> list[str]:
    """
    Разделяет текст меню на секции по заголовкам в верхнем регистре.
    """
    # Паттерн для поиска заголовков (2+ слова в верхнем регистре или одно длинное слово)
    pattern = r'\n([A-ZÁÉÍÓÚÑ]{2,}(?:\s[A-ZÁÉÍÓÚÑ]{2,})+)\n'
    
    # Находим все заголовки
    headers = re.findall(pattern, text)
    
    if not headers:
        # Если заголовки не найдены, считаем все меню одной секцией
        return [text]
    
    # Разделяем текст по найденным заголовкам
    sections = re.split(pattern, text)
    
    # Очищаем и собираем результат
    result = []
    # Первым элементом будет текст до первого заголовка (если он есть)
    if sections[0].strip():
        result.append(sections[0].strip())
        
    # Собираем заголовки с их содержимым
    for i in range(len(headers)):
        header = headers[i]
        content = sections[(i*2)+2].strip()
        result.append(f"{header}\n{content}")
        
    return [s for s in result if s]


@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer('Привет! Отправь мне фотографию меню, и я верну красивый HTML-файл с его содержимым.')

@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Этот бот анализирует фото меню и возвращает HTML-файл.')

@router.message(lambda message: message.photo)
async def handle_photo(message: Message):
    processing_msg = await message.answer('Принял! Начинаю обработку...')
    
    photo = message.photo[-1]
    file_id = photo.file_id
    
    temp_dir = os.path.join(os.path.dirname(__file__), '..', 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    
    # Генерируем читаемое имя файла
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    download_path = os.path.join(temp_dir, f'{file_id}.jpg')
    output_filename = f"menu_{timestamp}.html"
    output_path = os.path.join(temp_dir, output_filename)
    
    try:
        await bot.download(photo, destination=download_path)
        
        # Шаг 1: OCR
        await processing_msg.edit_text('Шаг 1/4: Распознаю текст с изображения...')
        extracted_text = await extract_text_from_image(download_path)
        
        if not extracted_text:
            await message.answer('Не удалось распознать текст. Пожалуйста, отправьте более четкое фото.')
            return
        
        # Шаг 2: Разделение на секции
        await processing_msg.edit_text('Шаг 2/4: Разделяю меню на секции...')
        sections = split_text_into_sections(extracted_text)
        
        if not sections:
            await message.answer('Не удалось найти секции в меню. Попробую обработать целиком...')
            sections = [extracted_text]

        all_dishes = []
        total_sections = len(sections)
        
        # Шаг 3: Поочередная обработка секций
        for i, section in enumerate(sections):
            await processing_msg.edit_text(f'Шаг 3/4: Анализирую секцию {i+1} из {total_sections}...')
            dishes = await process_menu_section(section)
            if dishes:
                all_dishes.extend(dishes)
            await asyncio.sleep(1) 

        if not all_dishes:
            await message.answer('Не удалось извлечь ни одного блюда из меню. Пожалуйста, проверьте качество фото или попробуйте другое меню.')
            return

        # Шаг 4: Получение изображений
        total_dishes = len(all_dishes)
        for i, dish in enumerate(all_dishes):
            await processing_msg.edit_text(f'Шаг 4/4: Ищу изображение для блюда {i+1} из {total_dishes}...')
            # Используем новый, более точный запрос. Если его нет, используем старую логику.
            query = dish.get("imageSearchQuery") or dish.get("originalName") or dish.get("translatedName")
            if query:
                image_url = await get_image_url(query)
                dish["image"] = image_url

        # Генерируем и сохраняем HTML
        html_content = generate_html_menu(all_dishes, title="Ваше меню")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        await processing_msg.delete()
        # Отправляем документ с новым, читаемым именем
        document = FSInputFile(output_path, filename=output_filename)
        await message.answer_document(document, caption="Ваше меню в формате HTML готово!")
        
    except Exception as e:
        await processing_msg.delete()
        await message.answer(f'Произошла критическая ошибка: {str(e)}')
    finally:
        # Удаляем временные файлы
        if os.path.exists(download_path):
            os.remove(download_path)
        if os.path.exists(output_path):
            os.remove(output_path)
