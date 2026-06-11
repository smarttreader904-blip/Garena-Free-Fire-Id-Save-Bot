
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from database import init_db, add_ff

BOT_TOKEN="YOUR_BOT_TOKEN"
ADMINS={8859975301:AAEqR6ut9U_Vh77slUhAj5RdbwQmt2OoTXk}

class AddFF(StatesGroup):
    name=State()
    uid=State()
    note=State()

dp=Dispatcher()

kb=ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Add FF ID")]],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def start(msg: Message):
    if msg.from_user.id not in ADMINS:
        await msg.answer("Not authorized.")
        return
    await msg.answer("Welcome", reply_markup=kb)

@dp.message(F.text=="Add FF ID")
async def add_start(msg: Message, state:FSMContext):
    await state.set_state(AddFF.name)
    await msg.answer("Send Free Fire account name")

@dp.message(AddFF.name)
async def get_name(msg: Message, state:FSMContext):
    await state.update_data(name=msg.text)
    await state.set_state(AddFF.uid)
    await msg.answer("Send UID")

@dp.message(AddFF.uid)
async def get_uid(msg: Message, state:FSMContext):
    await state.update_data(uid=msg.text)
    await state.set_state(AddFF.note)
    await msg.answer("Send note")

@dp.message(AddFF.note)
async def get_note(msg: Message, state:FSMContext):
    data=await state.get_data()
    await add_ff(data["name"], data["uid"], msg.text)
    await state.clear()
    await msg.answer("Saved successfully")

async def main():
    await init_db()
    bot=Bot(BOT_TOKEN)
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())
