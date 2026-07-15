from aiogram import Dispatcher

from . import common
from . import registration

def register_handlers(dp: Dispatcher):
    dp.include_routers(
        common.router,
        registration.router,
    )