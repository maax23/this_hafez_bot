# handlers/__init__.py
from handlers.router import callback_router

def register_handlers(bot):

    @bot.callback_query_handler(func=lambda call: True)
    def _callback(call):
        callback_router(bot, call)
