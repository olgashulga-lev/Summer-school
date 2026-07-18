import os
from aiogram import Router, types
from aiogram.filters import Command
import api
from .common_utils import get_player_or_none
from aiogram.types import FSInputFile

router = Router()

@router.message(Command("avatar"))
async def cmd_avatar(message: types.Message):
    player = get_player_or_none(message)

    if not player:
        await message.answer("Сначала зарегистрируйтесь: /registration")
        return

    current_level = player.level
    max_level = player.get_max_level()

    if current_level < max_level:
        exp_for_next = player.get_exp_for_next_level()
        exp_text = f"Опыт: {player.exp}/{exp_for_next}"
    else:
        exp_text = "МАКСИМУМ!"

    text = f"""
<b>{player.name}</b>

Уровень: {player.level}/30
{exp_text}
HP: {player.hp}/100
Урон: {player.damage}
Удача: {int(player.luck * 100)}
Деньги: {player.money}
"""

    # Проверяем существует ли файл
    if os.path.exists(player.photo):
        try:
            photo = FSInputFile(player.photo)
            await message.answer_photo(photo=photo, caption=text)
        except Exception as e:
            print(f"Ошибка при отправке фото: {e}")
            await message.answer(text)
    else:
        # Если файл не найден, отправляем только текст
        await message.answer(text)