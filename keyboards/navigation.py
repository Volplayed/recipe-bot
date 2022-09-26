from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

#buttons with actions
navigation_keyboard = ReplyKeyboardMarkup([
    #two inline buttons (first row)
    [KeyboardButton("Random"), KeyboardButton("Filters")],
    
    #one inline button (second row)
    [KeyboardButton("Help")],
    ])
