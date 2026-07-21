import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import code_generator

TOKEN = os.environ.get("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👾 Привет! Я нейросеть для генерации идеального кода.\n"
        "Пришли мне описание задачи, и я сгенерирую код.\n"
        "Например: 'напиши функцию быстрой сортировки на Python'"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    await update.message.reply_text("⏳ Генерирую код через API...")
    try:
        code = code_generator.generate_code(prompt, max_length=600)
        if len(code) > 4000:
            code = code[:4000] + "\n... (обрезано)"
        await update.message.reply_text(f"```\n{code}\n```", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")

def run_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущен и работает в режиме polling...")
    app.run_polling()
