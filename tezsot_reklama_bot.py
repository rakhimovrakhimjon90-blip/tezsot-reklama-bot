import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

BOT_TOKEN = os.getenv("BOT_TOKEN", "BU_YERGA_YANGI_TOKENNI_QOYING")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

bot = Bot(BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class AdState(StatesGroup):
    waiting_ad = State()

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Reklama yuborish", callback_data="send_ad")],
        [InlineKeyboardButton(text="🛒 TezSot kanaliga kirish", url="https://t.me/TezSotUz")]
    ])

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 Assalomu alaykum!\n\n🤖 TezSot Reklama botiga xush kelibsiz.\n\nReklamangizni yuborish uchun quyidagi tugmani bosing.",
        reply_markup=main_menu()
    )

@dp.callback_query(F.data == "send_ad")
async def send_ad_button(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdState.waiting_ad)
    await callback.message.answer(
        "📢 Reklamangizni yuboring.\n\nMatn, rasm, video yoki hujjat yuborishingiz mumkin.\nReklama avval admin tekshiruviga yuboriladi.\n\nBekor qilish: /cancel"
    )
    await callback.answer()

@dp.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Reklama yuborish bekor qilindi.", reply_markup=main_menu())

@dp.message(AdState.waiting_ad)
async def receive_ad(message: Message, state: FSMContext):
    if ADMIN_ID == 0:
        await message.answer("⚠️ Bot hali ADMIN_ID bilan sozlanmagan.")
        return
    await message.forward(ADMIN_ID)
    await bot.send_message(
        ADMIN_ID,
        f"📢 Yangi reklama!\n👤 {message.from_user.full_name}\n🆔 {message.from_user.id}"
    )
    await message.answer(
        "✅ Reklamangiz qabul qilindi! Admin tekshirganidan keyin keyingi bosqichga o'tadi.",
        reply_markup=main_menu()
    )
    await state.clear()

async def main():
    print("TezSot Reklama Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
