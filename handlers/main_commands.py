from logging import Filter
from msilib.schema import Error
from aiogram import dispatcher
from aiogram.dispatcher.filters import CommandStart, Command
from aiogram.types.message import Message
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from loader import dp
from keyboards.navigation import navigation_keyboard
from states.navigation import Navigation
from keyboards.filters import filters_keyboard, time_keyboard, ingredients_keyboard, lelvel_keyboard
from states.filters import Filters
import database.get_data as database
from utils.Filter_Container import Filters_container


########################################################################################

#random command response with /random (any state)
@dp.message_handler(commands='random', state="*")

#random command response with Random
@dp.message_handler(text="Random", state=Navigation.PICKING_OPTION)
async def random_handler(message: Message):
    #gets random recipe data from database
    data = database.get_random_recipe()

    await dp.bot.send_photo(chat_id=message.chat.id, photo=data['image'])

    await message.answer(
        f"""
    {data['name'].strip()}
    Preparation time: {data['time']} mins
    Complexity: {data['level'].strip()}
    Ingredients:
    {data['ingredients'].strip()}
    How to cook:
    {data['method'].strip()}
    {data['url'].strip()}
        """, 
    reply_markup=navigation_keyboard
    )

    #setting state to navigation at the start
    await Navigation.PICKING_OPTION.set()

#filters class object
filters = Filters_container([], 0, "Any")

#filters command response with /filters (any state)
@dp.message_handler(commands="filters", state="*")

#filters command response with Filters
@dp.message_handler(text="Filters", state=Navigation.PICKING_OPTION)
async def filters_handler(message: Message):

    #reset filters to default
    filters.reset()

    await message.answer(
        filters.get_string(),
        reply_markup=filters_keyboard
        )
    
    #setting state to filters menu
    await Filters.MENU.set()

########################INGREDINETS########################
#ingredients command response with Ingredients
@dp.message_handler(text="Ingredients", state=Filters.MENU)
async def filters_handler(message: Message):

    await message.answer(
        "Enter ingredients you need, divided with comma( , )",
        reply_markup=ingredients_keyboard
        )
    
    #setting state to ingredients input
    await Filters.INGREDIENTS.set()

#ingredients recieve from user
@dp.message_handler(state=Filters.INGREDIENTS)
async def ingredients_handler(message: Message):
    #setting filter ingredients from message
    filters.set_ingredients(message.text)

    await message.answer(
        filters.get_string(),
        reply_markup=filters_keyboard
        )
    
    #setting state to filters menu
    await Filters.MENU.set()

##############################TIME#########################
#time command response with Time
@dp.message_handler(text="Time", state=Filters.MENU)
async def filters_handler(message : Message):

    await message.answer(
        "Enter the amount of time (in minutes and only numbers)",
        reply_markup=time_keyboard
        )
    
    #setting state to filters time
    await Filters.TIME.set()

#time recive from user
@dp.message_handler(state=Filters.TIME)
async def time_handler(message : Message):
    #set filters time
    filters.set_time(message.text)

    await message.answer(
        filters.get_string(),
        reply_markup=filters_keyboard
        )

    #setting state to filters menu
    await Filters.MENU.set()

####################LEVEL###########################
#level command response with Complexity
@dp.message_handler(text="Complexity", state=Filters.MENU)
async def filters_handler(message : Message):

    await message.answer(
        "Choose the complexity level",
        reply_markup=lelvel_keyboard
        )
    
    #setting state to filters level
    await Filters.LEVEL.set()

#level recive from user
@dp.message_handler(state=Filters.LEVEL)
async def time_handler(message : Message):
    #set filters level
    filters.set_level(message.text)

    await message.answer(
        filters.get_string(),
        reply_markup=filters_keyboard
        )

    #setting state to filters menu
    await Filters.MENU.set()

#################READY########################
#ready command response with Ready
@dp.message_handler(text="Ready", state=Filters.MENU)
async def ready_handler(message : Message):
    try:
        #gets recipe data with filters from database
        data = database.get_recipe_with_filters(filters.get_dict())

        await dp.bot.send_photo(chat_id=message.chat.id, photo=data['image'])

        await message.answer(
            f"""
        {data['name'].strip()}
        Preparation time: {data['time']} mins
        Complexity: {data['level'].strip()}
        Ingredients:
        {data['ingredients'].strip()}
        How to cook:
        {data['method'].strip()}
        {data['url'].strip()}
            """, 
        reply_markup=filters_keyboard
        )
    except:
        #if nothing was found
        await message.answer(
            f"""
        Unfortunately nothing was found with your filters.
        Try changing some filters
            """, 
        reply_markup=filters_keyboard
        )
    #setting state to navigation at the start
    await Filters.MENU.set()