from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from telebot.types import User
from datetime import datetime
from utils.time import today, current_year, start_date, end_date, is_yalda
from utils.text import get_text_size, to_persian_digits
from uuid import uuid4

def make_base_image(bg_normal, bg_yalda):
    bg = bg_yalda if is_yalda() else bg_normal
    return Image.open(bg)


def make_story_image(title_num:str, text:str, user:User):
    """
    Generate a vertical (story-style) image containing a Hafez ghazal.

    The image layout and background change automatically during Yalda nights.
    The poem text is reshaped for proper Persian/Arabic rendering.

    Args:
        title_num (str): Ghazal number.
        text (str): Full ghazal text.
        user (telebot.types.User): Telegram user requesting the image.

    Returns:
        str: Path to the generated image file.
    """
    BLACK = (0, 0, 0)
    font = ImageFont.truetype('src/font/Nian.ttf', 40)
    title = ImageFont.truetype(f'src/font/Nian-Black.ttf', 50)

    text = text.split('\n')[:4]
    
    image = make_base_image(
        'src/images/bg_story.jpg',
        'src/images/bg_yalda_story.jpg'
    )

    TEXT = ImageDraw.Draw(image)
    
    _, _, width, length = image.getbbox()
    half_width, half_length = int(width/2), int(length/2)

    title_text = arabic_reshaper.reshape(f"غزل {to_persian_digits(title_num)}")
    # title
    TEXT.text((half_width - int(get_text_size(title_text, title)//2), int(length//3)), title_text, BLACK, font=title)

    lines = {
        'first': arabic_reshaper.reshape(text[0]),
        'second': arabic_reshaper.reshape(text[1]),
        'third': arabic_reshaper.reshape(text[2]),
        'fourth': arabic_reshaper.reshape(text[3]),
    }

    # The first bit
    TEXT.text((half_width - get_text_size(lines['first'], font)//2, int(length//3)+120), lines['first'], BLACK, font=font)
    TEXT.text((half_width - get_text_size(lines['second'], font)//2, int(length//3)+170), lines['second'], BLACK, font=font)

    # The second bit
    TEXT.text((half_width - get_text_size(lines['third'], font)//2, int(length/3)+270), lines['third'], BLACK, font=font)
    TEXT.text((half_width - get_text_size(lines['fourth'], font)//2, int(length/3)+320), lines['fourth'], BLACK, font=font)

    image.save('image.jpg', quality=80)
    return 'image.jpg'



def make_image(title_num:str, text:str, user:User):
    """
    Generate a image containing a Hafez ghazal.

    The image is optimized for regular Telegram photo messages.
    Background switches automatically during Yalda nights.

    Args:
        title_num (str): Ghazal number.
        text (str): Full ghazal text.
        user (telebot.types.User): Telegram user requesting the image.

    Returns:
        str: Path to the generated image file.
    """
    BLACK = (0, 0, 0)
    font = ImageFont.truetype('src/font/Nian.ttf', 40)
    title = ImageFont.truetype(f'src/font/Nian-Black.ttf', 50)

    text = text.split('\n')[:4]

    image = make_base_image(
            'src/images/bg.jpg',
            'src/images/bg_yalda.jpg'
        )

    TEXT = ImageDraw.Draw(image)
    
    _, _, width, length = image.getbbox()
    half_width, half_length = int(width/2), int(length/2)

    title_text = arabic_reshaper.reshape(f"غزل {to_persian_digits(title_num)}")

    # title
    TEXT.text((half_width - int(get_text_size(title_text, title)//2), int(length//3)-60), title_text, BLACK, font=title)

    lines = {
        'first': arabic_reshaper.reshape(text[0]),
        'second': arabic_reshaper.reshape(text[1]),
        'third': arabic_reshaper.reshape(text[2]),
        'fourth': arabic_reshaper.reshape(text[3]),
    }

    # The first bit
    TEXT.text((half_width + 30, int(length//3)+50), arabic_reshaper.reshape(text[0]), BLACK, font=font)
    TEXT.text((half_width - get_text_size(text[1], font) - 30, int(length//3)+60), arabic_reshaper.reshape(text[1]), BLACK, font=font)

    # # The second bit
    TEXT.text((half_width + 30, int(length//3)+150), arabic_reshaper.reshape(text[2]), BLACK, font=font)
    TEXT.text((half_width - get_text_size(text[3], font) - 30, int(length//3)+160), arabic_reshaper.reshape(text[3]), BLACK, font=font)

    image.save('image.jpg', quality=80)
    return 'image.jpg'
