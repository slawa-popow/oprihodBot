from aiogram.dispatcher.filters.state import State, StatesGroup


class BotState(StatesGroup):
   
    isauth = State()
    adduser = State()
    banuser = State()
    