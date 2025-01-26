from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio

api = ""
bot = Bot(token = api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text = 'Calories')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    if message.text.isdigit():
        await state.update_data(age = int(message.text))
        await message.answer('Введите свой рост:')
        await UserState.growth.set()
    else:
        await message.answer('Введите число.')

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    if message.text.isdigit():
        await state.update_data(growth = int(message.text))
        await message.answer('Введите свой вес:')
        await UserState.weight.set()
    else:
        await message.answer('Введите число.')

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    if message.text.isdigit():
        await state.update_data(weight=int(message.text))
        data = await state.get_data()
        result = round(10*int(data['weight']) + 6.25*int(data['growth']) - 5*int(data['age']) + 5, 2)
        await message.answer(f'Ваша норма калорий: {result}\n')
        await state.finish()
    else:
        await message.answer('Введите число.')

@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью. Введите Calories, чтобы начать расчёты.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)