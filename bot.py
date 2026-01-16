# bot.py
import time, asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import BotCommand
from config import TOKEN, FISH_COOLDOWN
from database import get_user, update_user, sql
from logic import catch, RODS, BAITS, LOCATIONS, TRASH

bot = Bot(TOKEN)
dp = Dispatcher()

def xp_limit(lvl): return 100 + (lvl - 1) * 50
def bar(xp, lim): f = int((xp / lim) * 10); return "▰"*f + "▱"*(10-f)

# --- Создание клавиатуры магазина ---
def create_shop_keyboard(items, prefix):
    kb = InlineKeyboardBuilder()
    for name, data in items.items():
        price = data["price"] if "price" in data else data[0]
        kb.button(text=f"{name}\n{price}💰", callback_data=f"{prefix}:{name}")
    return kb

# --- /start ---
@dp.message(Command("start"))
async def start(m: types.Message):
    get_user(m.from_user.id)
    await m.answer("🎣 Добро пожаловать!\n/fish /shop /balance /top")

# --- /balance ---
@dp.message(Command("balance"))
async def bal(m: types.Message):
    u = get_user(m.from_user.id)
    await m.answer(f"💰 Баланс: {u[1]} монет")

# --- /shop ---
@dp.message(Command("shop"))
async def shop(m: types.Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="🎣 Удочки", callback_data="shop_rods")
    kb.button(text="🪱 Наживки", callback_data="shop_baits")
    kb.button(text="🗺️ Локации", callback_data="shop_locations")
    await m.answer("🛒 Магазин:", reply_markup=kb.as_markup())

from aiogram import F
# Категории магазина
@dp.callback_query(F.data == "shop_rods")
async def shop_rods(cq: types.CallbackQuery):
    kb = create_shop_keyboard(RODS, "buy_rod")
    await cq.message.edit_text("🎣 Магазин удочек:", reply_markup=kb.as_markup())
    await cq.answer()

@dp.callback_query(F.data == "shop_baits")
async def shop_baits(cq: types.CallbackQuery):
    kb = create_shop_keyboard(BAITS, "buy_bait")
    await cq.message.edit_text("🪱 Магазин наживок:", reply_markup=kb.as_markup())
    await cq.answer()

@dp.callback_query(F.data == "shop_locations")
async def shop_locations(cq: types.CallbackQuery):
    kb = create_shop_keyboard(LOCATIONS, "buy_location")
    await cq.message.edit_text("🗺️ Магазин локаций:", reply_markup=kb.as_markup())
    await cq.answer()

# --- Покупка ---
@dp.callback_query(F.data.startswith("buy_"))
async def buy_item(cq: types.CallbackQuery):
    u = get_user(cq.from_user.id)
    item_type, item_name = cq.data.split(":")[0][4:], cq.data.split(":")[1]
    if item_type == "rod":
        price = RODS[item_name]["price"]
        if u[1] >= price:
            update_user(u[0], money=u[1]-price, rod=item_name)
            await cq.answer(f"✅ Куплено: {item_name}", show_alert=True)
        else:
            await cq.answer("❌ Недостаточно монет", show_alert=True)
    elif item_type == "bait":
        price = BAITS[item_name]["price"]
        if u[1] >= price:
            update_user(u[0], money=u[1]-price, bait=item_name)
            await cq.answer(f"✅ Куплено: {item_name}", show_alert=True)
        else:
            await cq.answer("❌ Недостаточно монет", show_alert=True)
    elif item_type == "location":
        price = LOCATIONS[item_name][0]
        if u[1] >= price:
            update_user(u[0], money=u[1]-price, location=item_name)
            await cq.answer(f"✅ Куплено: {item_name}", show_alert=True)
        else:
            await cq.answer("❌ Недостаточно монет", show_alert=True)

# --- /fish ---
@dp.message(Command("fish"))
async def fish(m: types.Message):
    if m.chat.type not in ["group", "supergroup"]:
        return await m.reply("⚠️ Рыбалка доступна только в группе!")

    u = get_user(m.from_user.id)
    now = int(time.time())
    time_left = FISH_COOLDOWN - (now - u[7])

    if time_left > 0:
        minutes = time_left // 60
        seconds = time_left % 60
        return await m.reply(f"⏱ Можно бросить через {minutes} мин. {seconds} сек.")

    res = catch(u[4], u[5], u[6])
    update_user(m.from_user.id, last_fish=now)

    if res["type"] == "trash":
        return await m.reply(f"🪵 Клюнуло! Ты поймал {res['name']}")

    xp = u[2] + res["xp"]
    lvl = u[3]
    lim = 100 + (lvl - 1) * 50
    if xp >= lim:
        xp -= lim
        lvl += 1

    # Обновляем статистику
    new_total = u[8] + 1
    new_max = max(u[9], res["weight"])
    update_user(m.from_user.id, xp=xp, level=lvl, money=u[1]+res["price"], total_caught=new_total, max_weight=new_max)

    await m.reply_photo(photo=res["photo"], caption=(
        f"🐟 Клюнуло! Ты поймал {res['name']} весом {res['weight']:.2f} кг\n"
        f"💰 Цена: {res['price']}\n"
        f"🏅 Ур. {lvl} {bar(xp, lim)} {xp}/{lim} (+{res['xp']} XP)"
    ))

# --- /top ---
@dp.message(Command("top"))
async def top(m: types.Message):
    top_players = sql.execute("SELECT user_id, total_caught, max_weight FROM users ORDER BY total_caught DESC LIMIT 10").fetchall()
    msg = "🏆 Топ рыболовов:\n"
    for i, t in enumerate(top_players, 1):
        uid, total, max_w = t
        msg += f"{i}. {uid} — {total} рыб, макс {max_w} кг\n"
    await m.reply(msg)

# --- Меню команд ---
async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать игру"),
        BotCommand(command="/fish", description="Поймать рыбу (только в группе)"),
        BotCommand(command="/shop", description="Открыть магазин"),
        BotCommand(command="/balance", description="Показать баланс"),
        BotCommand(command="/top", description="Топ рыболовов"),
    ]
    await bot.set_my_commands(commands)

async def main():
    await set_bot_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())