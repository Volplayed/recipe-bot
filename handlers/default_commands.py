
from aiogram import dispatcher
from aiogram.dispatcher.filters import CommandStart, Command
from aiogram.types.message import Message


from loader import dp
from keyboards.navigation import navigation_keyboard
from states.navigation import Navigation

#start command response
@dp.message_handler(CommandStart(), state="*")
async def start_handler(message: Message):
    await message.answer(
        f"""
        Hi {message.chat.first_name}, I am RecipeBot.
    I can randomly choose a recipe for you, or you can find appropriate one with filters.
        Enter /random to get a random recipe
        /filters to find recipe with filters
        /help - for more info
        """, 
    reply_markup=navigation_keyboard
    )

    #setting state to navigation at the start
    await Navigation.PICKING_OPTION.set()

#help command response with /help, any state
@dp.message_handler(commands="help", state="*")

#help command response with Help
@dp.message_handler(text="Help", state=Navigation.PICKING_OPTION)
async def help_handler(message: Message):
    await message.answer(
        """
        RecipeBot helps you find recipes.
        Useful commands:
        /help - to see useful commands
        /random - to get random recipe
        /filters - to get recipe based on filters
    """, reply_markup=navigation_keyboard)

    #setting state to navigation at the start
    await Navigation.PICKING_OPTION.set()

