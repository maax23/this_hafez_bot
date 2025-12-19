from services.fall import generate_fall
from keyboards import fal_keyboard, philolearn_keyboard

def handle_fall(bot, call):
    """
    Handle 'get_fall' callback and send a random Hafez fal.
    """
    result = generate_fall()

    if not result:
        bot.answer_callback_query(call.id, "خطا در دریافت فال")
        return

    bot.send_message(
        call.from_user.id,
        result["text"],
        parse_mode="HTML",
        reply_markup=fal_keyboard(result["omen"], True)
    )
