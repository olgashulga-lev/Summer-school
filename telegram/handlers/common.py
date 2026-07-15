from aiogram import Router, types
from aiogram.filters import Command


router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    text = """
<b>Привет! Я МеханоБот!</b>

Я помогу тебе и твоим друзьям играть в интересную игру!

<b>Основные команды:</b>
/start - показать это сообщение
/help - помощь по командам
/registration - создать своего персонажа
/avatar - посмотреть своего персонажа
/inventory - посмотреть инвентарь
/fight - вызвать на дуэль (ответь на сообщение)
/event - посмотреть мероприятия
/raid - посмотреть боссов
/achievement - посмотреть достижения
/shop - магазин предметов
/dice - игра в кости
    """
    await message.answer(text)