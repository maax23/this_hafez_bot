import random
from services.poems import get_poem
from utils.text import to_persian_digits, get_caption
from telebot.formatting import format_text, hcite, escape_markdown

MAX_GHAZAL = 495

def generate_fall():
    """
    Generate a random Hafez fal.

    Returns:
        dict: Contains omen number, poem text, and formatted caption.
    """
    omen = random.randint(1, MAX_GHAZAL)
    poem_id = f"sh{str(omen).zfill(3)}"
    poem = get_poem(poem_id)

    if not poem:
        return None

    text = format_text(
        f"<b>- غزل {to_persian_digits(str(omen))}</b>\n",
        hcite(f"{poem[1].replace('\n', '\n\n')}"),
        get_caption(),
    )

    return {
        "omen": omen,
        "text": text,
        "voice": poem[3],
    }













# import random
# from .poems import get_poem
# from utils.text import get_caption, to_persian_digits
# from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
# from telebot.formatting import format_text, hcite, escape_markdown


# def fall(bot, msg, philolearn_button):
#     """
#     Send a random Hafez divination (Fal-e Hafez) to a user.

#     Selects a random ghazal, formats it, and sends it with
#     interactive options such as interpretation, image, and audio.

#     Args:
#         user_id (int): Telegram user ID.
#     """
#     user_id = msg.from_user.id
#     omen = random.randint(1, 495)
#     omen_name = f"sh{str(omen).zfill(3)}"
#     get_omen = get_poem(omen_name)

#     caption = get_caption()

#     # Format poem text
#     text = format_text(
#         f'<b>- غزل {to_persian_digits(str(omen))}</b>\n',
#         hcite(str(get_omen[1]).replace('\n', '\n\n')),
#         caption,
#     )

#     # Create interactive buttons for the poem
#     markup = InlineKeyboardMarkup(row_width=2)
#     markup.add(
#         InlineKeyboardButton("تفسیر فالم...  (تفسیر هوش مصنوعی)", callback_data=f"get_tabir-{omen}"),
#     )
#     markup.add(
#         InlineKeyboardButton("تصویر فالم رو بده!", callback_data=f"get_pic-{omen}"),
#         InlineKeyboardButton("استوری فالم رو بده!", callback_data=f"get_story-{omen}"),
#     )
#     markup.add(
#         InlineKeyboardButton("خوانش این غزل...", callback_data=f"get_audio-{get_omen[3]}"),
#     )
#     markup.add(
#         philolearn_button()
#     )

#     bot.send_message(user_id, text, parse_mode="HTML", reply_markup=markup)
