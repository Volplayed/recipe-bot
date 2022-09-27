from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

#buttons with filter actions
filters_keyboard = ReplyKeyboardMarkup([
    #one inline button (first row)
    [KeyboardButton("Ingredients")],
    
    #two inline buttons (second row)
    [KeyboardButton("Time"), KeyboardButton("Complexity")],

    #one inline button (third row)
    [KeyboardButton("Ready"),]
    ])
