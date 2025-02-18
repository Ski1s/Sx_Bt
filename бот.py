import sys
sys.path.append(r"C:\Users\gge94\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages")

import os
import random
import requests
from telebot import TeleBot, types
from telethon import TelegramClient
import webbrowser


# Ваш API ключ от OpenWeatherMap
API_KEY = "9d15a0f055317619b2b307fb71a92cdc"
TOKEN = '7567875016:AAHbzAegdgA7my-n-oMrPXPM3wGCqhBsZL8'
bot = TeleBot(TOKEN)

# Путь к папке с медиафайлами
MEDIA_FOLDER = 'C:/Users/gge94/OneDrive/Desktop/Bot/media'

# Проверка существования папки
if not os.path.exists(MEDIA_FOLDER):
    raise FileNotFoundError(f"Папка {MEDIA_FOLDER} не найдена. Проверьте правильность пути.")

# Стартовое сообщение и кнопки
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        f'Привет {message.from_user.first_name}, ваш ID - {message.from_user.id}\n'
        'Команды для бота:\n'
        '/site - Открывает мой сайт\n'
        '/id - Показывает ID пользователя\n'
        '/mem - Показывает мемы\n'
        '/weather - Узнать погоду в вашем городе\n'
        '/don - Поддержка автора\n'
        '/converter - конвертер валют'
    )

# Отправка сайта
@bot.message_handler(func=lambda message: message.text == "Перейти на мой сайт")
def send_site(message):
    bot.reply_to(message, 'Мой сайт - https://sites.google.com/view/blackjackgame')

# Погода
@bot.message_handler(commands=['weather'])
def weather(message):
    bot.send_message(message.chat.id, "Введите название города, чтобы узнать погоду:")
    bot.register_next_step_handler(message, get_weather_for_city)

def get_weather_for_city(message):
    city = message.text  # Получаем текст от пользователя (название города)
    weather_data = get_weather(city)
    
    if weather_data:
        bot.send_message(
            message.chat.id, 
            f"Погода в {city}:\n{weather_data['weather']}\nТемпература: {weather_data['temp']}°C"
        )
    else:
        bot.send_message(message.chat.id, f"Не удалось получить данные о погоде для города {city}. Попробуйте еще раз.")

def get_weather(city):
    # URL API для получения погоды
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"
    
    # Отправляем запрос на сервер OpenWeatherMap
    response = requests.get(url)
    
    # Если запрос успешен (код 200)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        return {"weather": weather, "temp": temp}
    else:
        return None

# Мемы
@bot.message_handler(func=lambda message: message.text == "Мемы" or message.text == "/mem" or message.text == "/mem@Anonymous_228_bot" or message.text == "venom" )
def send_random_media(message):
    # Получаем список всех файлов в папке
    files = os.listdir(MEDIA_FOLDER)
    if not files:
        bot.send_message(message.chat.id, "В папке нет файлов.")
        return
    
    # Выбираем случайный файл
    random_file = random.choice(files)
    file_path = os.path.join(MEDIA_FOLDER, random_file)

    # Определяем тип файла
    if random_file.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        with open(file_path, 'rb') as file:
            bot.send_photo(message.chat.id, file, reply_markup=next_button_markup())
    elif random_file.endswith(('.mp4', '.avi', '.mov')):
        with open(file_path, 'rb') as file:
            bot.send_video(message.chat.id, file, reply_markup=next_button_markup())
    else:
        bot.send_message(message.chat.id, "Подпишитесь на канал автора https://t.me/ski1s4k") #Ошибка

def next_button_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    next_button = types.KeyboardButton("Следующие")
    home_button = types.KeyboardButton("Главная")
    markup.add(next_button, home_button)
    return markup

@bot.message_handler(func=lambda message: message.text == 'Следующие')
def send_next_media(message):
    send_random_media(message)

@bot.message_handler(func=lambda message: message.text == 'Главная')
def send_to_main(message):
    # Отправляем сообщение с главными кнопками
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Перейти на мой сайт")
    item2 = types.KeyboardButton("Мемы")
    markup.add(item1, item2)
    bot.send_message(
        message.chat.id,
        'Вы вернулись в главное меню. Выберите команду:\n'
        '/site - Открывает мой сайт\n'
        '/id - Показывает ID пользователя\n'
        '/mem - Показывает мемы\n'
        '/don - Поддержка автора\n'
        '/converter - конвертер валют',
        reply_markup=markup
    )



@bot.message_handler(commands=['website', 'site'])
def site(message):
    bot.reply_to(message, f'мой сайт - https://sites.google.com/view/blackjackgame')
        
@bot.message_handler(commands=['don'])
def site(message):
    bot.reply_to(message, f'Поддержка автора - https://www.donationalerts.com/r/ski1s4k')

#декаратор https://www.donationalerts.com/r/ski1s4k


@bot.message_handler(commands=["id"])
def start(message):
    bot.send_message(message.chat.id, f'ваш id - {message.from_user.id}' )


@bot.message_handler(commands=["help"])
def start(message):
    bot.send_message(message.chat.id, 'Команды для бота:\n' 
                    '/site - Открывает мой сайт\n'
                    '/id - Показывает ID пользователя\n'
                    '/mem - Показывает мемы\n'
                    '/weather - Узнать погоду в вашем городе\n'
                    '/don - Поддержка автора\n'
                    '/converter - конвертер валют')




#Конвертер валют
amount = 0

class CurrencyConverter:
    def __init__(self):
        self.api_url = "https://api.apilayer.com/exchangerates_data/convert"
        self.api_key = "VdZYyJT9mrhhAWwVpc6QgK27gqh03KTD"

    def convert(self, amount, from_currency, to_currency):
        try:
            response = requests.get(self.api_url, params={
                "to": to_currency,
                "from": from_currency,
                "amount": amount
            }, headers={"apikey": self.api_key})
            if response.status_code == 200:
                data = response.json()
                return data.get("result", None)
            else:
                raise ValueError(f"Ошибка API: {response.status_code}")
        except Exception as e:
            raise ValueError(f"Не удалось выполнить запрос: {e}")

currency_converter = CurrencyConverter()

@bot.message_handler(commands=['converter'])
def converter(message):
    bot.send_message(message.chat.id, 'Введите сумму для конвертации:')
    bot.register_next_step_handler(message, handle_amount)

def handle_amount(message):
    global amount
    try:
        amount = float(message.text.strip())
        if amount > 0:
            markup = types.InlineKeyboardMarkup(row_width=2)
            btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
            btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
            btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
            btn4 = types.InlineKeyboardButton('Другое', callback_data='else')
            markup.add(btn1, btn2, btn3, btn4)
            bot.send_message(message.chat.id, 'Выберите валюту для конвертации:', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Сумма должна быть больше 0. Пожалуйста, введите сумму заново:')
            bot.register_next_step_handler(message, handle_amount)
    except ValueError:
        bot.send_message(message.chat.id, 'Ошибка ввода. Введите сумму числом:')
        bot.register_next_step_handler(message, handle_amount)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    try:
        values = call.data.upper().split('/')
        if call.data == 'else':
            bot.send_message(call.message.chat.id, "Введите валюты в формате FROM/TO, например, RUB/USD:")
            bot.register_next_step_handler(call.message, custom_currency)
            return
        result = currency_converter.convert(amount, values[0], values[1])
        if result:
            bot.send_message(call.message.chat.id, f'Результат конвертации: {result:.2f}')
        else:
            bot.send_message(call.message.chat.id, 'Ошибка при конвертации валюты.')
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Произошла ошибка: {e}")

def custom_currency(message):
    try:
        values = message.text.upper().split('/')
        if len(values) == 2:
            result = currency_converter.convert(amount, values[0], values[1])
            if result:
                bot.send_message(message.chat.id, f'Результат конвертации: {result:.2f}')
            else:
                bot.send_message(message.chat.id, 'Ошибка при конвертации валюты.')
        else:
            bot.send_message(message.chat.id, 'Неверный формат. Введите валюты в формате FROM/TO.')
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")




bot.polling()




#@bot.message_handler(content_types=['text'])
#def get_text_messages(message):
    #bot.send_message(message.from_user.id, message.text)


@bot.message_handler()
def info(message):
    if message.text.lower() == "сайт":
        bot.reply_to(message, f'мой сайт - https://sites.google.com/view/blackjackgame')
@bot.message_handler()
def info(message):
    if message.text.lower() == "Сайт":
        bot.reply_to(message, f'мой сайт - https://sites.google.com/view/blackjackgame')



#кнопка она не подключена функции вот и не работать 
# markup = types.InlineKeyboardMarkup()
# markup.add(types.InlineKeyboardButton('Перейти на сайт', url='https://sites.google.com/view/blackjackgame/%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F-%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0'))
# def site(message):
    # bot.reply_to(message , reply_markup=markup)


#reply_to - ответ на собшение
#send_message - собшение

#бесконечный цикл что бы бот моментально не отключался


bot.polling(none_stop=True, interval=0)