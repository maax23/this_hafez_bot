import arabic_reshaper
from .time import is_yalda

def get_caption():
    return '\n🍉🍉 @this_hafez_bot 🍉🍉' if is_yalda() else '\n@this_hafez_bot'


def to_persian_digits(text:str) -> str:
    """
    Convert English digits in a string to Persian digits.

    Args:
        text (str): Input string containing English digits.

    Returns:
        str: String with Persian digits instead of English digits.
    """
    english_numbers = "0123456789"
    persian_numbers = "۰۱۲۳۴۵۶۷۸۹"
    translation_table = str.maketrans(english_numbers, persian_numbers)
    return text.translate(translation_table)


def get_text_size(text, font):
    """
    Calculate the visual width of a Persian/Arabic text after reshaping.

    Args:
        text (str): Input text to measure.
        font (ImageFont.FreeTypeFont): PIL font used for rendering the text.

    Returns:
        int: Width of the rendered text in pixels.
    """
    return font.getbbox(arabic_reshaper.reshape(text))[2]

