from msilib.schema import Error
from aiogram import dispatcher
from aiogram.dispatcher.filters import CommandStart, Command
from aiogram.types.message import Message
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from loader import dp
from keyboards.navigation import navigation_keyboard
from states.navigation import Navigation
from keyboards.filters import filters_keyboard
from states.filters import Filters
import database.get_data as database

#filters class
class Filters_container():
    def __init__(self, ingredients: list, time: int, level: str):
        #variables to be used
        self.ingredients = ingredients
        self.time = time
        self.level = level


    #sets everything to default values
    def reset(self):
        self.ingredients = []
        self.time = 0
        self.level = "Any"

    #makes a beautiful current filter string
    def get_string(self):
        #ingredients string making
        ingredients = ''

        if len(self.ingredients) > 0:
            #get each ingredient and put into string
            for ingredient in self.ingredients:
                if ingredients == '': #is empty
                    ingredients += ingredient
                else:
                    ingredients += f', {ingredient}'
        else: #if no ingredients are set
            ingredients = 'Any'
        
        #time string making
        time = ''

        if self.time != 0: #if filter is set
            time = f"{self.time}"
        else:
            time = 'Any'
        
        #level string
        level = self.level

        #final string
        text = f"Currently applied filters:\nIngredients: {ingredients}\nTime: {time}\nComplexity: {level}"

        return text
    
    #set ingredients
    def set_ingredients(self, text):
        try:
            #clear current ingredients
            self.ingredients = []

            #split input
            ingredients = text.split(',')

            #add each ingredient to the list
            for ingredient in ingredients:
                if (ingredient.strip()) != '': #is not empty string
                    self.ingredients.append(ingredient.strip())
        except:
            pass

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

#ingredients command response with Ingredients
@dp.message_handler(text="Ingredients", state=Filters.MENU)
async def filters_handler(message: Message):
    #filters dict of applied filters
    await message.answer(
        "Enter ingredients you need divided with comma( , )",
        reply_markup=ReplyKeyboardRemove()
        )
    
    #setting state to ingredients input
    await Filters.INGREDIENTS.set()

#ingredients recieve from user
@dp.message_handler(state=Filters.INGREDIENTS)
async def filters_handler(message: Message):
    #filters dict of applied filters
    filters.set_ingredients(message.text)
    await message.answer(
        filters.get_string(),
        reply_markup=filters_keyboard
        )
    
    #setting state to filters menu
    await Filters.MENU.set()