# bot_main.py
import os
import logging
import asyncio
import asyncpg
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Импортируем конфигурацию
from config import (
    TOKEN, ADMIN_ID, NOTIFY_CHAT, BOT_NAME, DATABASE_URL,
    REFERRAL_BONUS, MIN_WITHDRAW, PAYMENT, PAYMENT_LINK, TARIFFS
)

# Импортируем хендлеры
from handlers import (
    start, catalog, about, referral, withdraw, select_tariff,
    process_order, handle_sex, skip_promo, admin_panel, stats,
    approve_order, home, button_handler, error_handler
)

# Импортируем функции базы данных
from database import init_db

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

async def main_async():
    """Асинхронный запуск бота"""
    # Инициализируем базу данных
    await init_db()
    logger.info("✅ База данных готова")
    
    # Создаем приложение
    app = Application.builder().token(TOKEN).build()
    
    # Регистрируем команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    
    # Регистрируем callback обработчики
    app.add_handler(CallbackQueryHandler(button_handler))
    
    # Регистрируем обработчики сообщений
    app.add_handler(MessageHandler(filters.PHOTO, process_order))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_order))
    
    # Обработчик ошибок
    app.add_error_handler(error_handler)
    
    logger.info("🚀 Бот запущен")
    await app.run_polling()

def main():
    """Точка входа"""
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
