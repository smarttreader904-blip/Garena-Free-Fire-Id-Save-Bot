from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from config import BOT_TOKEN, ADMINS
import database as db

# user state store
user_state = {}


# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("➕ Add FF ID", callback_data="add")],
        [InlineKeyboardButton("🗑 Delete FF ID", callback_data="delete")],
        [InlineKeyboardButton("📋 Show IDs", callback_data="show")],
    ]

    await update.message.reply_text(
        "Welcome to FF Save Bot 🎮\nChoose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ---------------- CALLBACK HANDLER ----------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "add":
        user_state[user_id] = {"step": "name"}
        await query.message.reply_text("Please send me your Free Fire Account Name")

    elif query.data == "delete":
        data = db.get_all()
        if not data:
            await query.message.reply_text("No FF IDs found ❌")
            return

        keyboard = []
        for key, value in data.items():
            keyboard.append([
                InlineKeyboardButton(
                    f"🎮 {value['name']}",
                    callback_data=f"del_{key}"
                )
            ])

        await query.message.reply_text(
            "Select ID to delete:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "show":
        data = db.get_all()
        if not data:
            await query.message.reply_text("No data found ❌")
            return

        text = "📋 Saved FF IDs:\n\n"
        for v in data.values():
            text += f"🎮 Name: {v['name']}\nUID: {v['uid']}\nText: {v['text']}\n\n"

        await query.message.reply_text(text)

    elif query.data.startswith("del_"):
        key = query.data.split("_")[1]
        db.delete_data(key)
        await query.message.reply_text("Deleted Successfully 🗑")


# ---------------- MESSAGE HANDLER ----------------
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id not in user_state:
        return

    step = user_state[user_id]["step"]

    # NAME
    if step == "name":
        user_state[user_id]["name"] = update.message.text
        user_state[user_id]["step"] = "uid"
        await update.message.reply_text("Please send your Free Fire UID")

    # UID
    elif step == "uid":
        user_state[user_id]["uid"] = update.message.text
        user_state[user_id]["step"] = "text"
        await update.message.reply_text("Please send any text (level, rank etc)")

    # TEXT FINAL SAVE
    elif step == "text":
        name = user_state[user_id]["name"]
        uid = user_state[user_id]["uid"]
        text = update.message.text

        db.add_data(name, uid, text)

        await update.message.reply_text("Saved Successfully ✅")

        user_state.pop(user_id)


# ---------------- MAIN ----------------
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
