from aiogram.dispatcher.filters.state import State, StatesGroup

#default state set after /start command
class Navigation(StatesGroup):
    PICKING_OPTION = State()