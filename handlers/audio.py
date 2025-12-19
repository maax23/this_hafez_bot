from decouple import config
from services.audio import get_audio_message_id
from keyboards import philolearn_keyboard

STORAGE_CHAT_ID = config("STORAGE")

def handle_audio(bot, call):
    """
    Handle 'get_audio' callback and send ghazal audio recitation.
    """
    try:
        omen = int(call.data.split("-")[1])
    except (IndexError, ValueError):
        bot.answer_callback_query(call.id, "درخواست نامعتبر")
        return

    message_id = get_audio_message_id(omen)

    if not message_id:
        bot.answer_callback_query(call.id, "خوانش این غزل موجود نیست")
        return

    bot.copy_message(
        chat_id=call.from_user.id,
        from_chat_id=STORAGE_CHAT_ID,
        message_id=message_id,
        reply_markup=philolearn_keyboard()
    )
