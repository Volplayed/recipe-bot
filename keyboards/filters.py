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

#buttons for ingredients
ingredients_keyboard = ReplyKeyboardMarkup([
    #one inline button
    [KeyboardButton('Any')]
])

#buttons for default time options
time_keyboard = ReplyKeyboardMarkup([
    #three inline buttons (first row)
    [KeyboardButton("30"), KeyboardButton("60"), KeyboardButton("90")],

    #one einline button (second row)
    [KeyboardButton("Any")]
])

#buttons for complexity level options
lelvel_keyboard = ReplyKeyboardMarkup([
    #three inline buttons (first row)
    [KeyboardButton("Easy"), KeyboardButton("Medium"), KeyboardButton("Hard")],

    #one einline button (second row)
    [KeyboardButton("Any")]
])

