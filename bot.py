import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_KEY)


# Хранилище контекстов
user_contexts = {}

# Кнопка "Новый запрос"
keyboard = ReplyKeyboardMarkup(
    [["Новый запрос"]], resize_keyboard=True
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_contexts[update.effective_user.id] = []
    await update.message.reply_text(
        "Привет! Я бот, который использует ChatGPT.\nВведи запрос.",
        reply_markup=keyboard
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = (
        "Я генерирую ответы через ChatGPT.\n"
        "Команды:\n"
        "/start — сбросить контекст\n"
        "/help — помощь\n"
        "Кнопка 'Новый запрос' — очистка контекста\n"
    )
    await update.message.reply_text(txt)


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    # Очистка контекста
    if text.lower() == "новый запрос":
        user_contexts[user_id] = []
        await update.message.reply_text("Контекст очищен. Введите новый запрос.")
        return

    # Инициализация контекста
    if user_id not in user_contexts:
        user_contexts[user_id] = []

    # Добавляем сообщение пользователя
    user_contexts[user_id].append({"role": "user", "content": text})

    # Отправка запроса к ChatGPT
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=user_contexts[user_id],
            temperature=0.7
        )

        reply = completion.choices[0].message.content

        user_contexts[user_id].append({
            "role": "assistant",
            "content": reply
        })

        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text(f"Ошибка при обращении к ChatGPT: {e}")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    app.run_polling()


if __name__ == "__main__":
    main()
