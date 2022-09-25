from aiogram.dispatcher.filters.state import State, StatesGroup

class Navigation(StatesGroup):
    PICKING_OPTION = State()