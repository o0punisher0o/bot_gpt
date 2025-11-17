# Telegram ChatGPT Bot

Телеграм-бот на Python, который использует API ChatGPT для генерации ответов с учётом контекста диалога.

## Возможности
- Команды `/start` и `/help`
- Генерация ответов через OpenAI ChatGPT
- Хранение контекста диалога для каждого пользователя
- Сброс контекста при `/start` и по кнопке **Новый запрос**
- Простая и расширяемая архитектура

## Стек
- Python 3.10+
- python-telegram-bot (v20+)
- OpenAI API (официальная библиотека)
- python-dotenv

## Установка
```bash

git clone <repository_url>
cd <project_folder>
pip install -r requirements.txt

```

Настройка
Создайте файл .env:

```bash

BOT_TOKEN=ваш_telegram_bot_token
OPENAI_API_KEY=ваш_openai_api_key

```

Запуск

```bash
python bot.py

```

Структура проекта
```
project/
│── bot.py
│── requirements.txt
│── .env
```
Примечания
Модель можно заменить в параметре model="gpt-4o-mini".

При необходимости контекст можно хранить в SQLite/Redis.
