from aiogram import executor
from dispatcher import dp
from aiogram import types
from dispatcher import dp
import config
import re
from db import BotDB
BotDB = BotDB('agrimodb.db')
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
pending_updates = {}

def is_integer(value):
    return isinstance(value, int)

def is_string(value):
    return isinstance(value, str)
    
class AddCropStates(StatesGroup):
    CROP_NAME = State()
    QUANTITY = State()
    EXPENSE = State()
    PRICE = State()

class UpdateCropStates(StatesGroup):
    CROP_ID = State()
    CROP_NAME = State()
    QUANTITY = State()
    EXPENSE = State()
    PRICE = State()

class AddWeatherSoilStates(StatesGroup):
    CROP_ID = State()
    TEMPERATURE = State()
    PRESSURE = State()
    SOIL_MOISTURE = State()
    HUMIDITY = State()
    RADIATION = State()
    PRECIPITATION = State()

@dp.message_handler(commands = "start")
async def start(message: types.Message):
    if(not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(message.from_user.id,message.from_user.username, message.from_user.first_name, message.from_user.last_name)

    photo = open('cat.jpg', 'rb')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Add Crop Data'),
               types.KeyboardButton('Check Crop Data'),
               types.KeyboardButton('Update Crop Data'),
               types.KeyboardButton('Add Weather and soil Data'),
               types.KeyboardButton('Check Weather and soil Data'),
               types.KeyboardButton('Create financial report'))
    
    await message.bot.send_photo(message.from_user.id, photo)
    await message.bot.send_message(message.from_user.id, f"Welcome {message.from_user.last_name} {message.from_user.first_name}! This is an innovative AgriMot telegram bot to help farmers quickly and conveniently compile financial reports and farm status reports!", reply_markup=markup)

@dp.message_handler()
async def handle_buttons(message: types.Message):
    user_id = message.from_user.id
    text = message.text
    if text == 'Add Crop Data':
        photo = open('crop.jpg', 'rb')
        await message.bot.send_photo(message.from_user.id, photo)
        await message.bot.send_message(user_id,"Please enter the crop name:")
        await AddCropStates.CROP_NAME.set()
    if text == 'Check Crop Data':
        await message.bot.send_message(user_id, BotDB.get_crop(user_id))
    if text == 'Update Crop Data':
        await message.answer("Please provide the crop ID:")
        await UpdateCropStates.CROP_ID.set()
    if text == 'Create financial report':
        await message.bot.send_message(user_id, BotDB.financial_analysis(user_id))
    if text == 'Add Weather and soil Data':
        photo = open('crop2.jpg', 'rb')
        await message.bot.send_photo(message.from_user.id, photo)
        await message.bot.send_message(user_id,"Please enter the crop ID:")
        await AddWeatherSoilStates.CROP_ID.set()
    if text == 'Check Weather and soil Data':
        await message.bot.send_message(user_id,BotDB.get_weatherandsoil())
    if text == 'Кто тебя создал':
        await message.bot.send_message(user_id, "Господин Алишер")
    if text == 'Ты крутой?':
        await message.bot.send_message(user_id, "Да")
    if text == 'Что такое НИШ':
        await message.bot.send_message(user_id, "Ад")
    if text == 'Что такое программирование?':
        await message.bot.send_message(user_id, "Интересно")
    if text == 'Что такое FIRST?':
        await message.bot.send_message(user_id, "Робототехника")

@dp.message_handler(state=AddCropStates.CROP_NAME)
async def add_crop_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if is_string:
            data['crop_name'] = message.text
        else:
            await message.answer("Write string text:")
    await message.answer("Enter the quantity produced:")
    await AddCropStates.next()

@dp.message_handler(state=AddCropStates.QUANTITY)
async def add_crop_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if is_integer:
            data['crop_quantity_produced'] = message.text
        else:
           await message.answer("Write integer text:") 
    await message.answer("Enter the crop expense:")
    await AddCropStates.next()

@dp.message_handler(state=AddCropStates.EXPENSE)
async def add_crop_expense(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if is_integer:
            data['crop_expense'] = message.text
        else:
            await message.answer("Write integer text:") 
    await message.answer("Enter the crop price:")
    await AddCropStates.next()

@dp.message_handler(state=AddCropStates.PRICE)
async def add_crop_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if is_integer:
            data['crop_price'] = message.text
        else:
            await message.answer("Write integer text:") 
        user_id = message.from_user.id
        if all(data.values()):
            BotDB.add_crop(user_id, data['crop_name'], data['crop_quantity_produced'], data['crop_expense'], data['crop_price']) 
            await message.answer("Crop data added successfully!")
            await state.finish()
        else:
            await message.answer("Some data is missing. Please try again.")

@dp.message_handler(state=UpdateCropStates.CROP_ID)
async def update_crop_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['crop_id'] = message.text
    await message.answer("Enter updated crop name:")
    await UpdateCropStates.CROP_NAME.set()

@dp.message_handler(state=UpdateCropStates.CROP_NAME)
async def update_crop_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        print(is_string)
        if is_string:
            data['crop_name'] = message.text
        else:
            await message.answer("Write string text:") 
    await message.answer("Enter updated quantity produced:")
    await UpdateCropStates.QUANTITY.set()

@dp.message_handler(state=UpdateCropStates.QUANTITY)
async def update_crop_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if is_integer:
            data['crop_quantity_produced'] = message.text
        else:
            await message.answer("Write integer text:") 
    await message.answer("Enter updated crop expense:")
    await UpdateCropStates.EXPENSE.set()

@dp.message_handler(state=UpdateCropStates.EXPENSE)
async def update_crop_expense(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if is_integer:
            data['crop_expense'] = message.text
        else:
            await message.answer("Write integer text:") 
    await message.answer("Enter updated crop price:")
    await UpdateCropStates.PRICE.set()

@dp.message_handler(state=UpdateCropStates.PRICE)
async def update_crop_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['crop_price'] = message.text
        crop_id = data['crop_id']
        user_id = message.from_user.id
        crop_name = data['crop_name']
        crop_quantity_produced = data['crop_quantity_produced']
        crop_expense = data['crop_expense']
        crop_price = data['crop_price']

        BotDB.update_crop(crop_id, user_id, crop_name, crop_quantity_produced, crop_expense, crop_price)

    await message.answer("Crop data updated successfully.")
    await state.finish()

@dp.message_handler(state=AddWeatherSoilStates.CROP_ID)
async def add_crop_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.isdigit():
            data['crop_id'] = int(message.text)
        else:
            await message.answer("Please enter a valid crop ID (numeric value).")
            return
    await message.answer("Enter the temperature:")
    await AddWeatherSoilStates.next()

@dp.message_handler(state=AddWeatherSoilStates.TEMPERATURE)
async def add_temperature(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.replace(".", "", 1).isdigit():
            data['temperature'] = float(message.text)
        else:
            await message.answer("Please enter a valid temperature value.")
            return
    await message.answer("Enter the pressure:")
    await AddWeatherSoilStates.next()

@dp.message_handler(state=AddWeatherSoilStates.PRESSURE)
async def add_pressure(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.replace(".", "", 1).isdigit():
            data['pressure'] = float(message.text)
        else:
            await message.answer("Please enter a valid pressure value.")
            return
    await message.answer("Enter the soil moisture:")
    await AddWeatherSoilStates.next()

@dp.message_handler(state=AddWeatherSoilStates.SOIL_MOISTURE)
async def add_soil_moisture(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.replace(".", "", 1).isdigit():
            data['soil_moisture'] = float(message.text)
        else:
            await message.answer("Please enter a valid soil moisture value.")
            return
    await message.answer("Enter the humidity:")
    await AddWeatherSoilStates.next()

@dp.message_handler(state=AddWeatherSoilStates.HUMIDITY)
async def add_humidity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.replace(".", "", 1).isdigit():
            data['humidity'] = float(message.text)
        else:
            await message.answer("Please enter a valid humidity value.")
            return
    await message.answer("Enter the radiation:")
    await AddWeatherSoilStates.next()

@dp.message_handler(state=AddWeatherSoilStates.RADIATION)
async def add_radiation(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.replace(".", "", 1).isdigit():
            data['radiation'] = float(message.text)
        else:
            await message.answer("Please enter a valid radiation value.")
            return
    await message.answer("Enter the precipitation:")
    await AddWeatherSoilStates.next()

@dp.message_handler(state=AddWeatherSoilStates.PRECIPITATION)
async def add_precipitation(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.replace(".", "", 1).isdigit():
            data['precipitation'] = float(message.text)
        else:
            await message.answer("Please enter a valid precipitation value.")
            return
        user_id = message.from_user.id
        if all(data.values()):
            BotDB.add_weather_soil(user_id, data['crop_id'], data['pressure'], data['soil_moisture'], data['humidity'], data['radiation'], data['precipitation']) 
            await message.answer("Weather and soil data added successfully!")
            await state.finish()
        else:
            await message.answer("Some data is missing. Please try again.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)