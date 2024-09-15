import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests

TELEGRAM_BOT_TOKEN = '1623596838:AAEweOyaeJI6AZ-wpDnreZ8q91elbNLtigw'
API_KEY = 'AIzaSyBV4iuPJAD9w9hl07lCwg8bM4xw7rzupPU'

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Я бот, который может общаться с нейросетью через API Gemini.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = await get_gemini_response(user_message)
    await update.message.reply_text(response)

async def get_gemini_response(message: str) -> str:
    url = "https://api.gemini.com/v1/your_endpoint"  # Замените на нужный вам эндпоинт
    headers = {
        'Content-Type': 'application/json',
        'API-Key': API_KEY
    }
    payload = {
        'message': message
    }

    # Отправка запроса к API
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get('response', 'Не удалось получить ответ.')
    else:
        return f'Ошибка при запросе к API: {response.status_code}'

def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
