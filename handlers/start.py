from aiogram import dispatcher
from aiogram.dispatcher.filters import CommandStart, Command
from aiogram.types.message import Message


from loader import dp
from keyboards.navigation import navigation_keyboard
from states.navigation import Navigation



@dp.message_handler(CommandStart(), state="*")
async def start_handler(message: Message):
    await message.answer(
        'Ok', 
    reply_markup=navigation_keyboard
    )

    await Navigation.PICKING_OPTION.set()
