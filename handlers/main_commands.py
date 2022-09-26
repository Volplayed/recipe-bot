from aiogram import dispatcher
from aiogram.dispatcher.filters import CommandStart, Command
from aiogram.types.message import Message


from loader import dp
from keyboards.navigation import navigation_keyboard
from states.navigation import Navigation

import database.get_data as database

#random command response with /random
@dp.message_handler(commands='random', state="*")

#random command response with Random
@dp.message_handler(text="Random", state=Navigation.PICKING_OPTION)
async def start_handler(message: Message):
    #gets random recipe data from database
    data = database.get_random_recipe()

    await dp.bot.send_photo(chat_id=message.chat.id, photo=data['image'])

    await message.answer(
        f"""
        {data['name']}

        Preparation time: {data['time']} mins
        Complexity: {data['level']}
        Ingredients:
        {data['ingredients']}

        How to cook:
        {data['method']}

        {data['url']}
        """, 
    reply_markup=navigation_keyboard
    )

    #setting state to navigation at the start
    await Navigation.PICKING_OPTION.set()

