from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
import os
from bot import bot
from ocr import extract_text_from_image
from translator import detect_language
from menu_processor import process_menu
from html_generator import generate_html

router = Router()

def register_handlers(dp):
    dp.include_router(router)

@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer('Привет! Отправь мне фотографию меню на любом языке (кроме русского), и я переведу его для тебя.')

@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Этот бот переводит меню с фотографии. Просто отправь фото меню, и я верну тебе HTML-файл с переводом.')

@router.message(lambda message: message.photo)
async def handle_photo(message: Message):
    # Сообщаем пользователю, что начали обработку
    processing_msg = await message.answer('Обрабатываю фотографию меню...')
    
    # Получаем фото
    photo = message.photo[-1]  # Берем самое большое разрешение
    file_id = photo.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    
    # Создаем временную директорию, если её нет
    os.makedirs('temp', exist_ok=True)
    
    # Скачиваем фото
    download_path = f'temp/{file_id}.jpg'
    await bot.download_file(file_path, download_path)
    
    try:
        # Извлекаем текст
        await message.answer('Распознаю текст на изображении...')
        extracted_text = await extract_text_from_image(download_path)
        
        if not extracted_text:
            await message.answer('Не удалось распознать текст на изображении. Пожалуйста, отправьте более четкое фото.')
            return
        
        # Определяем язык
        language = await detect_language(extracted_text)
        
        if language == 'ru':
            await message.answer('Обнаружен русский язык. Пожалуйста, отправьте меню на другом языке.')
            return
        
        # Обрабатываем меню
        await message.answer('Анализирую и перевожу меню...')
        processed_menu = await process_menu(extracted_text, language)
        
        # Генерируем HTML
        html_path = f'temp/{file_id}_menu.html'
        await generate_html(processed_menu, html_path)
        
        # Отправляем результат
        await message.answer('Вот переведенное меню:')
        await message.answer_document(FSInputFile(html_path))
        
    except Exception as e:
        await message.answer(f'Произошла ошибка при обработке меню: {str(e)}')
    finally:
        # Удаляем временные файлы
        if os.path.exists(download_path):
            os.remove(download_path)
        if os.path.exists(f'temp/{file_id}_menu.html'):
            os.remove(f'temp/{file_id}_menu.html')
