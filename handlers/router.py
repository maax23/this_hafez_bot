# handlers/router.py
from handlers.fall import handle_fall
from handlers.tabir import handle_tabir
from handlers.image import handle_image, handle_story
from handlers.audio import handle_audio

def callback_router(bot, call):
    routes = {
        "get_fall": handle_fall,
        "get_tabir": handle_tabir,
        "get_pic": handle_image,
        "get_story": handle_story,
        "get_audio": handle_audio,
    }

    for prefix, handler in routes.items():
        if call.data.startswith(prefix):
            handler(bot, call)
            return
