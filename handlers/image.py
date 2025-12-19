from services.poems import get_poem
from image.generator import make_image, make_story_image
from keyboards import philolearn_keyboard
from utils.text import get_caption

def handle_image(bot, call):
    omen = call.data.split("-")[1]
    poem = get_poem(f"sh{omen.zfill(3)}")

    img_path = make_image(omen, poem[1], call.from_user)

    with open(img_path, "rb") as img:
        bot.send_photo(
            call.from_user.id,
            img,
            caption=get_caption(),
            reply_markup=philolearn_keyboard()
        )


def handle_story(bot, call):
    omen = call.data.split("-")[1]
    poem = get_poem(f"sh{omen.zfill(3)}")

    img_path = make_story_image(omen, poem[1], call.from_user)

    with open(img_path, "rb") as img:
        bot.send_photo(
            call.from_user.id,
            img,
            caption=get_caption(),
            reply_markup=philolearn_keyboard()
        )