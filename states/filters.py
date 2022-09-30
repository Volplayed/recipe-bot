from aiogram.dispatcher.filters.state import State, StatesGroup

#state set after /filters command
class Filters(StatesGroup):
    #first state where user chooses what filters to apply
    MENU = State()

    #ingredients getting state
    INGREDIENTS = State()

    #time getting state
    TIME = State()

    #level getting state
    LEVEL = State()