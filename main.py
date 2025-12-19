"""
Hafez Divination Telegram Bot
A Telegram bot for accessing Hafez's poetry, including divination (Fal-e Hafez) functionality.
Provides random poems, specific ghazals by number, interpretations, and audio recitations.
"""

import os
import re
import sqlite3
import logging
import random
from decouple import config
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.formatting import format_text, hcite, escape_markdown

# Configure logging to file
logging.basicConfig(
    filename='info.log', 
    filemode='a', 
    level=logging.INFO, 
    format='%(asctime)s - %(filename)s - %(message)s'
) 

# Load environment variables
# DEBUG = config('DEBUG', default=True, cast=bool)
TOKEN = config('TOKEN')  # Telegram Bot API token

# Initialize Telegram bot
bot = TeleBot(token=TOKEN)

# Database file path
database_file = 'database.db'

def get_poem(name:str) -> tuple:
    """
    Retrieve a poem from the database by its filename.
    
    Args:
        name (str): The poem filename (e.g., 'sh001' for ghazal 1)
    
    Returns:
        tuple: A tuple containing (file, text, tabir, voice) for the poem
        Returns None if poem not found
    """
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    query = "SELECT file, text, tabir, voice FROM poems WHERE file='%s'" % name
    res = cursor.execute(query)
    return res.fetchone()


@bot.message_handler(commands=['start', 'help'])
def start(message):
    """
    Handle /start and /help commands.
    Sends welcome message and usage instructions to user.
    
    Args:
        message: Telegram message object containing user's command
    """
    logging.info(f'{message.chat.username} - {message.chat.id}')

    text = """
به نام آن که جان را فکرت آموخت
من ربات دیوان حافظ هستم و اینجا‌ام تا شما را در گشودن گنجینهٔ غزلیات این شاعر بزرگ یاری کنم.

راهنمای استفاده:

• غزل خاص: اگر غزل به خصوصی مد نظرتان است، شمارهٔ آن را با اعداد برایم بفرستید.
مثال:
`495`

• فال حافظ: اگر می‌خواهید تفالی به دیوان حافظ بزنید، روی دکمهٔ «فالم رو بگیر!» لمس کنید یا دستور
/fall
را ارسال کنید.
(پس از گرفتن فال، می‌توانید توضیح و تفسیر آن غزل را نیز دریافت نمایید.)

✨ ویژگی اضافه: در هر مرحله، با انتخاب دکمهٔ «خوانش این غزل...» می‌توانید به یک خوانش شنیداری نمونه از همان غزل دسترسی داشته باشید.

پشتیبانی:
@Hr\\_ArshA
@max\\_23

@this\\_hafez\\_bot
@PhiloLearn
""".encode('utf-8')
    
    # Create inline keyboard
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("فالم رو بگیر!", callback_data="get_fall"),
        InlineKeyboardButton("فیلولرن", url="https://PhiloLearn.t.me"),
    )

    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="MarkDown")



def fall(user_id):
    """
    Send a random Hafez divination (Fal-e Hafez) to the user.
    
    Args:
        user_id (int): Telegram user ID to send the divination to
    """
    
    omen = random.randint(1, 495)
    omen_name = f"sh{str(omen).zfill(3)}"
    get_omen = get_poem(omen_name)

    # Format poem text
    text = format_text(
f'غزل {omen}',
hcite(get_omen[1]),
'\n@this_hafez_bot',
    )

    # Create interactive buttons for the poem
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("تفسیر فالم...  (تفسیر هوش مصنوعی)", callback_data=f"get_tabir-{omen}"),

    )
    markup.add(
        InlineKeyboardButton("تصویر فالم رو بده!", callback_data=f"get_pic-{omen}"),
        InlineKeyboardButton("خوانش این غزل...", callback_data=f"get_audio-{get_omen[3]}"),
        InlineKeyboardButton("فیلولرن", url="https://PhiloLearn.t.me"),

    )

    bot.send_message(user_id, text, parse_mode="HTML", reply_markup=markup)


@bot.message_handler(commands=['fall'])
def get_fall(msg):
    """
    Handle /fall command to trigger Hafez divination.
    
    Args:
        msg: Telegram message object containing the /fall command
    """
    fall(msg.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """
    Handle all inline keyboard button callbacks.
    
    Args:
        call: Telegram callback query object containing callback data
    """
    if call.data == "get_fall":
        fall(call.from_user.id)

    if str(call.data).startswith("get_tabir"):
        omen = str(call.data).split('-')[1]
        omen_name = f"sh{str(omen).zfill(3)}"

        poem = get_poem(omen_name)[2]
        text = format_text(
            f'غزل {omen}\n',
            str(poem).replace('---', ''),
            '\n@this\\_hafez\\_bot',
        )


        bot.send_message(call.from_user.id, text, parse_mode='MarkDown')

    # if str(call.data).startswith("get_pic"):
    #     file_name = str(call.data).split('-')[1]

    #     poem = make_image(file_name)
    #     pic = open(poem, 'rb')

    #     text = '@this_hafez_bot\n@PhiloLearn'
    #     bot.send_photo(call.from_user.id, pic, caption=text, reply_markup=get_fallow_markup())


    if str(call.data).startswith("get_audio"):
        omen = str(call.data).split('-')[1]
        print(omen)
        omen_name = f"sh{str(omen).zfill(3)}"


        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("فیلولرن", url="https://PhiloLearn.t.me"),
        )
        # Copy audio message from storage channel
        bot.copy_message(call.from_user.id, config('STORAGE'), omen, reply_markup=markup)



@bot.message_handler(content_types=['text'])
def send_this_poem(message):
    """
    Handle text messages to send specific poems by number.
    
    Args:
        message: Telegram message object containing the poem number
    """
    # Extract number from message text
    poem_num = re.findall(r"\d+", str(message.text))


    if poem_num != []:
        poem_num = int(poem_num[0])

        # Check if poem number is in valid range
        if poem_num in range(1, 495):
            name_of_poem = f"sh{str(poem_num).zfill(3)}"
            text_of_poem = get_poem(name_of_poem)
            
            # Format poem display
            text = format_text(
                f'غزل {poem_num}',
                hcite(text_of_poem[1]),
                '\n@this_hafez_bot',
            )

            # Create interactive buttons
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton("تفسیر این غزل... (تفسیر هوش مصنوعی)", callback_data=f"get_tabir-{poem_num}"),
            )
            markup.add(
                InlineKeyboardButton("تصویر غزل رو بده!", callback_data=f"get_pic-{poem_num}"),
                InlineKeyboardButton("خوانش این غزل...", callback_data=f"get_audio-{text_of_poem[3]}"),
                InlineKeyboardButton("فیلولرن", url="https://PhiloLearn.t.me"),

            )

            bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="HTML")
        
        else:
            bot.send_message(message.chat.id, 'این غزل وجود ندارد!')

    else:
        bot.send_message(message.chat.id, 'لطفا یک عدد معتبر از ۱ تا ۴۹۵ وارد کنید...')


        
# Start the bot with infinite polling
bot.infinity_polling()