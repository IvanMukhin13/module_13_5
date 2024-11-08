from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


API = ''
bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Информация')],
        [KeyboardButton(text='Рассчитать')]
    ],
    resize_keyboard=True)


@dp.message_handler(commands=['start'])
async def start(message):
     await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


class UserClass(StatesGroup):
    age = State()
    height = State()
    weight = State()


@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserClass.age.set()


@dp.message_handler(state=UserClass.age)
async def set_height(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserClass.height.set()


@dp.message_handler(state=UserClass.height)
async def set_weight(message, state):
    await state.update_data(height=message.text)
    await message.answer('Введите свой вес:')
    await UserClass.weight.set()


@dp.message_handler(state=UserClass.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    norma = (int(data['weight']) * 10) + (int(data['height']) * 6.25) - (5 * int(data['age']))
    await message.answer(f'Ваша норма: {norma} ')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
