from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from config import Config
from datetime import datetime
from states.fsm_states import BotState
from keyboards.keyboards import get_kb_main, auth_kb_main
from database import Db
import uuid
import asyncio


bot = Bot(token=Config.TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())
db = Db()

@dp.message_handler(commands=['start'], state='*')
async def auth_start(message: types.Message, state: FSMContext):

    l = asyncio.get_running_loop()
    coro = db.get_all_usrs
    res =  l.create_task(coro())
    c = await res
    
    await message.answer(str(c))
     

    user_id = str(message.from_user.id)
    user_name = message.from_user.username or 'Anonymous'
    auth = await db.is_auth(user_id)
    keyboard = None
    if (auth and len(auth) > 0):
        id, name = auth
        user_id = id
        user_name = name
        token = uuid.uuid4()
        await BotState.isauth.set()
        keyboard = auth_kb_main()
        return await message.answer(
            f"""Привет {user_name}.\nТвой telegram id: <b>{user_id}</b>\n\n\tЧтобы начать работу с оприходованием нажми
    кнопку 'Открыть приложение' для запуска веб-приложения.\n\tЕсли твой телеграм id есть в базе данных, то ты можешь
    работать с приложением, иначе нет. \n\tТы можешь дать доступ к приложению любому человеку, добавив его телеграм id в базу
    данных. Также ты, если у тебя есть доступ, можешь забанить любого пользователя.\n\tДля добавления пользователя
    нажми кнопку 'Добавить пользователя' на клавиатуре.""",
            reply_markup=keyboard
        )

    else:
        keyboard = get_kb_main()
        await state.reset_state(with_data = False)
        return await message.answer(f"""Привет {user_name}.\nТвой telegram id: <b>{user_id}</b>\n\n """, reply_markup=keyboard)

@dp.message_handler(text='Все пользователи', state='*')
async def all_admins(message: types.Message, state: FSMContext):
        await print_all_users(message)
        
        


@dp.message_handler(text='Добавить пользователя', state="*")
async def add_admins(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)
    auth = await db.is_auth(user_id)
    if (len(auth) > 0):
        await BotState.adduser.set()
        return await message.answer('Введи имя пользователя и его телеграм id в одной строкой например так: Коля#321234354')
    else:
        await state.reset_state(with_data = False)
        return await message.answer('Тебе нельзя здесь быть.')
    
    
@dp.message_handler(text='Забанить пользователя по id', state="*")
async def del_admins(message: types.Message, state: FSMContext):
    await BotState.banuser.set()
    return await message.answer('Введи телеграм id того, кого надо забанить')

@dp.message_handler(state=BotState.banuser)
async def del_admins(message: types.Message, state: FSMContext):
    await state.reset_state(with_data = False)
    id = message.text
    isdel = await db.del_user_by_id(id)
    if isdel:
        await message.answer(f'Пользователь с id: <b>{id}</b> забанен')
        await print_all_users(message)
    else:
        await message.answer('Пользователь с id: <b>{id}</b> не найден')
    

    


@dp.message_handler(state=BotState.adduser)
async def add_new_usr(message: types.Message, state: FSMContext):
    uslist = message.text.split('#')
    await state.reset_state(with_data = False)
    if len(uslist) == 2:
        name, tgid = uslist
        await db.add_admin_user(name, tgid)
        return  await message.answer(f'Пользователь {name} c telegram id {tgid} добавлен.')
    else:
        return await message.answer('не корректный ввод.')
    


async def print_all_users(message):
    allusers = await db.get_all_usrs()
    for usr in allusers:
        _, name, tgid = usr
        await message.answer(f'имя: <b>{name}</b>  telegram id: <b>{tgid}</b>')



if __name__ == '__main__':
    print('\n--------- start bot: oprihod_bot ---------\n')
    executor.start_polling(dp)