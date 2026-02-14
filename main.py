import telebot
from telebot import formatting
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot_logic import gen_pass, gen_emodji, flip_coin
import os
import random
import requests
# use pip install pyTelegramBotAPI
# Get token from BotFather
bot = telebot.TeleBot("token here")
    
def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.message_handler(commands=['start'])
def send_hello(message):
    bot.reply_to(message, "Привет! Как дела?", reply_markup=gen_markup())
    
@bot.message_handler(commands=['countiue'])
def send_good(message):
    bot.reply_to(message, "Команды: /bye - прощание, /pass - генерация, /emodji - рандомный эмодзи, /coin - перевернуть монетку, /format - формат текста, /mem - все мемы, /randmem - рандомный мем, /animals - мемы про животных, /duck - картинки уток")

@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи!")

@bot.message_handler(commands=['pass'])
def send_password(message):
    password = gen_pass(10)  # Устанавливаем длину пароля, например, 10 символов
    bot.reply_to(message, f"Вот твой сгенерированный пароль: {password}")

@bot.message_handler(commands=['emodji'])
def send_emodji(message):
    emodji = gen_emodji()
    bot.reply_to(message, f"Вот эмоджи': {emodji}")

@bot.message_handler(commands=['coin'])
def send_coin(message):
    coin = flip_coin()
    bot.reply_to(message, f"Монетка выпала так: {coin}")

@bot.message_handler(commands=['format'])
def send_format(message):
    bot.send_message(
        message.chat.id,
        # function which connects all strings
        formatting.format_text(
            formatting.mbold(message.from_user.first_name),
            formatting.mitalic(message.from_user.first_name),
            formatting.munderline(message.from_user.first_name),
            formatting.mstrikethrough(message.from_user.first_name),
            formatting.mcode(message.from_user.first_name),
            separator=" " # separator separates all strings
        ),
        parse_mode='MarkdownV2'
    )

    # just a bold text using markdownv2
    bot.send_message(
        message.chat.id,
        formatting.mbold(message.from_user.first_name),
        parse_mode='MarkdownV2'
    )

    # html
    bot.send_message(
        message.chat.id,
        formatting.format_text(
            formatting.hbold(message.from_user.first_name),
            formatting.hitalic(message.from_user.first_name),
            formatting.hunderline(message.from_user.first_name),
            formatting.hstrikethrough(message.from_user.first_name),
            formatting.hcode(message.from_user.first_name),
            # hide_link is only for html
            formatting.hide_link('https://telegra.ph/file/c158e3a6e2a26a160b253.jpg'),
            separator=" "
        ),
        parse_mode='HTML'
    )

    # just a bold text in html
    bot.send_message(
        message.chat.id,
        formatting.hbold(message.from_user.first_name),
        parse_mode='HTML'
    )

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Хорошо", callback_data="cb_good"),
                               InlineKeyboardButton("Пока", callback_data="cb_bye"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_good":
        bot.answer_callback_query(call.id, "Очень приятно!! /countiue")
    elif call.data == "cb_bye":
        bot.answer_callback_query(call.id, "Пока! Удачи!")

@bot.message_handler(commands=['mem'])
def send_mem(message):
    with open('images/mem1.jpeg', 'rb') as f:  
        bot.send_photo(message.chat.id, f)  
    with open('images/mem2.jpeg', 'rb') as f:  
        bot.send_photo(message.chat.id, f)  
    with open('images/mem3.png', 'rb') as f:  
        bot.send_photo(message.chat.id, f)  

@bot.message_handler(commands=['animals'])
def send_animals(message):
    with open('images/mem4.png', 'rb') as f:  
        bot.send_photo(message.chat.id, f)  
    with open('images/mem5.png', 'rb') as f:  
        bot.send_photo(message.chat.id, f)  
    with open('images/mem6.png', 'rb') as f:  
        bot.send_photo(message.chat.id, f)  

@bot.message_handler(commands=['randmem'])
def send_randmem(message):
    img_name = random.choice(os.listdir('images'))
    with open(f'images/{img_name}', 'rb') as f:  
        bot.send_photo(message.chat.id, f)  

@bot.message_handler(commands=['duck'])
def send_duck(message):
    '''По команде duck вызывает функцию get_duck_image_url и отправляет URL изображения утки'''
    image_url = get_duck_image_url()
    bot.reply_to(message, image_url)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()
