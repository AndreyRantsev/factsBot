import telebot
import os
from dotenv import load_dotenv
from random import choice

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)

sections = facts_dict = {
    "Космос и астрономия🪐": [
        "Солнце занимает почти все 99 процентов массы нашей системы",
        "На Марсе одни сутки длятся ровно 24 часа и 37 минут",
        "Нейтронная звезда весом в целый миллиард тонн мала",
        "Свет от Солнца долетает до нашей Земли за 8 минут",
        "Венера считается самой жаркой планетой в системе",
        "Юпитер настолько велик что внутри него влезет Земля",
        "Млечный Путь вращается вокруг центра со скоростью света",
        "Черные дыры могут искривлять само время и пространство",
        "Кольца Сатурна состоят из чистых кусков льда и пыли",
        "Вакуум в космосе не имеет запаха и абсолютный холод"
    ],
    "Мир смартфонов": [
        "Экран смартфона обновляется до 120 раз за одну секунду",
        "Первый айфон был представлен миру в далеком 2007 году",
        "Зарядка мощностью 200 ватт зарядит телефон за 10 минут",
        "Матрица камеры состоит из многих миллионов пикселей",
        "Корпус из титана делает гаджет очень легким и прочным",
        "Процессор в телефоне мощнее чем старые компьютеры ПК",
        "Складной экран выдерживает более 200 тысяч сгибаний",
        "Сенсор отпечатка может быть скрыт прямо под стеклом",
        "Система охлаждения внутри нужна для тяжелых игр и видео",
        "Датчик Лидар помогает камере мерить точное расстояние"
    ],
    "Мода и стиль": [
        "Японский стиль одежды часто включает очень широкие вещи",
        "Кеды изначально создавались как обувь для баскетбола",
        "Ткань деним стала популярной благодаря прочности брюк",
        "Оверсайз футболки скрывают фигуру и создают комфорт",
        "Стиль винтаж подразумевает вещи старше двадцати лет",
        "Логотип бренда может стоить дороже чем сама вещь в цехе",
        "Шерсть мериноса отлично греет даже в сильный мороз",
        "Дизайнеры часто черпают идеи из старой формы военных",
        "Шелковая ткань была изобретена в Китае тысячи лет назад",
        "Белые кроссовки требуют очень частого и бережного ухода"
    ]
}

all_facts = [fact for facts in sections.values() for fact in facts]
current_section = {}

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, f"Привет, <b>{message.from_user.first_name}</b> \n\n Я бот-справочник. Выбери раздел:", parse_mode="HTML", reply_markup=mainKeyboard())

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, f"<b>Как пользоваться:</b> \n\n Выбери раздел из меню → выбери номер факта → читай.\n\n Кнопка <b>«Случайный факт»</b> — случайный факт из любого раздела.\n Кнопка <b>«Закрыть меню»</b> или /cancel — убирает клавиатуру. /start — вернуть главное меню.", parse_mode="HTML")

def mainKeyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for name in sections:
        keyboard.add(telebot.types.KeyboardButton(name))
    keyboard.add(telebot.types.KeyboardButton("Случайный факт🎲"))
    keyboard.add(telebot.types.KeyboardButton("Закрыть❌"))
    return keyboard

def secondary_keyboard(section):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    facts = sections[section]
    for i, name in enumerate(facts, start=1): 
        keyboard.add(telebot.types.KeyboardButton(f"Факт {i} : {name[:30]}..."))
    keyboard.add(telebot.types.KeyboardButton("Закрыть❌"))
    return keyboard

@bot.message_handler(func = lambda m: m.text in sections)
def open_sections(message):
    section = message.text 
    current_section[message.chat.id] = section
    facts = sections[section]
    bot.send_message(message.chat.id, facts, reply_markup=secondary_keyboard(section))

@bot.message_handler(func = lambda m: m.text.startswith("Факт"))
def fact_show(message):
    current_number = int(message.text.split()[1]) - 1
    section_name = current_section.get(message.chat.id)
    fact = sections[section_name][current_number]
    bot.send_message(message.chat.id, fact, reply_markup=secondary_keyboard(section_name))

@bot.message_handler(func = lambda m: m.text == "Случайный факт🎲")
def random_fact(message):
    bot.send_message(message.chat.id, choice(all_facts), reply_markup=mainKeyboard())

@bot.message_handler(func = lambda m: m.text == "Закрыть❌")
def cancel(message):
    bot.send_message(message.chat.id, "Клавиатура закрыта", reply_markup=telebot.types.ReplyKeyboardRemove())

print("Hello World!")
bot.polling()