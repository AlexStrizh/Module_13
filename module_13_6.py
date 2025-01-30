from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API = ""
bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())

# Клавиатуры
kb_main = ReplyKeyboardMarkup(resize_keyboard=True)
kb_main.row(KeyboardButton('Рассчитать'), KeyboardButton('Информация'))

kb_calculate = InlineKeyboardMarkup()
kb_calculate.row(
    InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories'),
    InlineKeyboardButton('Формулы расчёта', callback_data='formulas')
)


class UserState(StatesGroup):
    age = State()
    height = State()
    weight = State()


# Обработчики
@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await message.answer('Привет!', reply_markup=kb_main)


@dp.message_handler(text='Информация')
async def inform(message: types.Message):
    await message.answer('Я бот, помогающий рассчитать вашу норму калорий. Нажмите "Рассчитать", чтобы начать.')


@dp.message_handler(text='Рассчитать')
async def main_menu(message: types.Message):
    await message.answer('Выберите действие:', reply_markup=kb_calculate)


@dp.callback_query_handler(text='formulas')
async def show_formulas(call: types.CallbackQuery):
    await call.message.answer('Формула Харриса-Бенедикта:\n10 x вес (кг) + 6.25 x рост (см) - 5 x возраст (г) + 5')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def start_calculation(call: types.CallbackQuery):
    await call.message.answer('Введите ваш возраст:')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def process_age(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(age=int(message.text))
        await message.answer('Введите ваш рост (в см):')
        await UserState.next()
    else:
        await message.answer('Пожалуйста, введите число!')


@dp.message_handler(state=UserState.height)
async def process_height(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(height=int(message.text))
        await message.answer('Введите ваш вес (в кг):')
        await UserState.next()
    else:
        await message.answer('Пожалуйста, введите число!')


@dp.message_handler(state=UserState.weight)
async def process_weight(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(weight=int(message.text))
        data = await state.get_data()

        result = 10 * data['weight'] + 6.25 * data['height'] - 5 * data['age'] + 5
        await message.answer(f'Ваша суточная норма: {int(result)} ккал')

        await state.finish()
    else:
        await message.answer('Пожалуйста, введите число!')


@dp.message_handler()
async def handle_unknown(message: types.Message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)