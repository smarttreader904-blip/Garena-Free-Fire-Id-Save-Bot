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

user_state = {}


# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("➕ Add FF ID", callback_data="add")],
        [InlineKeyboardButton("📋 Show IDs", callback_data="show")],
        [InlineKeyboardButton("🗑 Delete FF ID", callback_data="delete")],
    ]

    await update.message.reply_text(
        "🎮 Welcome to FF Save Bot\nChoose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ---------------- CALLBACK HANDLER ----------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = str(query.from_user.id)

    # ---------------- ADD ----------------
    if query.data == "add":
        user_state[user_id] = {"step": "name"}
        await query.message.reply_text("📩 Send Free Fire Name")

    # ---------------- SHOW ----------------
    elif query.data == "show":
        data = db.get_all()

        if not data:
            await query.message.reply_text("❌ No data found")
            return

        keyboard = []

        for key, value in data.items():
            keyboard.append([
                InlineKeyboardButton(
                    f"🎮 {value['name']}",
                    callback_data=f"view_{key}"
                )
            ])

        await query.message.reply_text(
            "📋 Select ID:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ---------------- VIEW ----------------
    elif query.data.startswith("view_"):
        key = query.data.split("_")[1]
        data = db.get_one(key)

        if not data:
            await query.message.reply_text("❌ Not found")
            return

        text = f"""
📋 FF ID Details

🎮 Name: {data['name']}
🆔 UID: {data['uid']}
📌 Text: {data['text']}
"""

        keyboard = [
            [InlineKeyboardButton("🗑 Delete", callback_data=f"askdel_{key}")]
        ]

        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    # ---------------- DELETE LIST ----------------
    elif query.data == "delete":
        data = db.get_all()

        if not data:
            await query.message.reply_text("❌ No data found")
            return

        keyboard = []

        for key, value in data.items():
            keyboard.append([
                InlineKeyboardButton(
                    f"🎮 {value['name']}",
                    callback_data=f"askdel_{key}"
                )
            ])

        await query.message.reply_text(
            "🗑 Select ID to delete:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ---------------- CONFIRM DELETE ----------------
    elif query.data.startswith("askdel_"):
        key = query.data.split("_")[1]

        keyboard = [
            [InlineKeyboardButton("✅ Confirm", callback_data=f"del_{key}")],
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
        ]

        await query.message.reply_text(
            "⚠️ Are you sure?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ---------------- FINAL DELETE ----------------
    elif query.data.startswith("del_"):
        key = query.data.split("_")[1]
        db.delete_data(key)
        await query.message.reply_text("✅ Deleted Successfully")

    # ---------------- CANCEL ----------------
    elif query.data == "cancel":
        await query.message.reply_text("❌ Cancelled")

    # ---------------- ADMIN APPROVE ----------------
    elif query.data.startswith("ap_"):
        uid = query.data.split("_")[1]

        pending = db.get_pending()

        for row in pending:
            if str(row[4]) == uid:
                db.add_data(row[1], row[2], row[3])
                db.delete_pending(row[0])
                break

        await context.bot.send_message(uid, "✅ Your FF ID was approved")
        await query.message.reply_text("Approved ✔")

    # ---------------- ADMIN REJECT ----------------
    elif query.data.startswith("rej_"):
        uid = query.data.split("_")[1]

        pending = db.get_pending()

        for row in pending:
            if str(row[4]) == uid:
                db.delete_pending(row[0])
                break

        await context.bot.send_message(uid, "❌ Your FF ID was rejected")
        await query.message.reply_text("Rejected ❌")


# ---------------- MESSAGE HANDLER ----------------
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)

    if user_id not in user_state:
        return

    step = user_state[user_id]["step"]

    if step == "name":
        user_state[user_id]["name"] = update.message.text
        user_state[user_id]["step"] = "uid"
        await update.message.reply_text("📩 Send UID")

    elif step == "text":
    name = user_state[user_id]["name"]
    uid = user_state[user_id]["uid"]
    text = update.message.text

    if update.message.from_user.id in ADMINS:
        db.add_data(name, uid, text)
        await update.message.reply_text("✅ Admin: Saved Directly")
    else:
        db.add_pending(name, uid, text, user_id)
        await update.message.reply_text("⏳ Sent for Admin Approval")

    user_state.pop(user_id)
    # ---------------- ADMIN CHECK ----------------
    if update.message.from_user.id in ADMINS:
        db.add_data(name, uid, text)
        await update.message.reply_text("✅ Admin: Saved Directly")
    else:
        db.add_pending(name, uid, text, user_id)
        await update.message.reply_text("⏳ Sent for Admin Approval")

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
