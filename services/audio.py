from services.poems import get_poem

def get_audio_message_id(omen: int) -> int | None:
    """
    Return Telegram message_id of the audio recitation for a ghazal.
    """
    poem_id = f"sh{str(omen).zfill(3)}"
    poem = get_poem(poem_id)

    if not poem:
        return None

    return poem[3]  # voice column
