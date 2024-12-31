import requests
from telebot import TeleBot, types
from decouple import config
from config import settings

bot = TeleBot(settings.TELEGRAM_BOT_TOKEN)

API_BASE_URL = f"http://{config('DB_HOST')}:8000"

# Функция для запуска бота
def start_bot():
    bot.polling()

@bot.message_handler(commands=['start', 'register'])
def start_registration(message):
    """
    Начало регистрации пользователя через бота.
    """
    bot.reply_to(message, "Добро пожаловать! Пожалуйста, введите ваш email:")

    # Переход к шагу получения email
    bot.register_next_step_handler(message, process_email_step)

def process_email_step(message):
    """
    Получение email от пользователя.
    """
    email = message.text
    bot.reply_to(message, "Введите ваше имя пользователя:")
    bot.register_next_step_handler(message, process_username_step, email)

def process_username_step(message, email):
    """
    Получение имени пользователя.
    """
    username = message.text
    bot.reply_to(message, "Введите пароль (должен быть не менее 8 символов):")
    bot.register_next_step_handler(message, process_password_step, email, username)

def process_password_step(message, email, username):
    """
    Получение пароля и завершение регистрации.
    """
    password = message.text

    if len(password) < 8:
        bot.reply_to(message, "Пароль слишком короткий. Попробуйте снова.")
        bot.register_next_step_handler(message, process_password_step, email, username)
        return

    # Отправляем запрос на API регистрации
    data = {
        "email": email,
        "username": username,
        "password": password,
        "password_confirm": password,
    }
    response = requests.post(f"{API_BASE_URL}/account/register/", data=data)

    if response.status_code == 201:
        bot.reply_to(message, "Вы успешно зарегистрированы! Войдите через команду /login")
    else:
        error_msg = response.json().get('detail', 'Ошибка регистрации')
        bot.reply_to(message, f"Ошибка: {error_msg}")

@bot.message_handler(commands=['login'])
def login_user(message):
    """
    Авторизация пользователя через Telegram.
    """
    bot.reply_to(message, "Введите ваш username:")
    bot.register_next_step_handler(message, process_login_username)

def process_login_username(message):
    username = message.text
    bot.reply_to(message, "Введите ваш пароль:")
    bot.register_next_step_handler(message, process_login_password, username)

def process_login_password(message, username):
    password = message.text
    data = {"username": username, "password": password}
    response = requests.post(f"{API_BASE_URL}/account/login/", data=data)

    if response.status_code == 200:
        auth_data = response.json()
        bot.reply_to(message, f"Вы успешно вошли! Ваш токен: {auth_data['access']}")
    else:
        bot.reply_to(message, "Ошибка входа. Проверьте данные и попробуйте снова.")