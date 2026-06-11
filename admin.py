from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import ADMINS
import database as db


def is_admin(user_id):
    return int(user_id) in ADMINS


async def approve_request(query, context, user_id):
    pending = db.get_pending()

    for row in pending:
        if str(row[4]) == str(user_id):
            db.add_data(row[1], row[2], row[3])
            db.delete_pending(row[0])

            await context.bot.send_message(
                chat_id=user_id,
                text="✅ Your FF ID has been approved."
            )

            await query.message.reply_text(
                "✅ Request Approved"
            )
            return


async def reject_request(query, context, user_id):
    pending = db.get_pending()

    for row in pending:
        if str(row[4]) == str(user_id):
            db.delete_pending(row[0])

            await context.bot.send_message(
                chat_id=user_id,
                text="❌ Your FF ID has been rejected."
            )

            await query.message.reply_text(
                "❌ Request Rejected"
            )
            return


async def send_pending_to_admin(bot, user_id, name, uid, text):
    keyboard = [
        [
            InlineKeyboardButton(
                "✅ Approve",
                callback_data=f"ap_{user_id}"
            ),
            InlineKeyboardButton(
                "❌ Reject",
                callback_data=f"rej_{user_id}"
            ),
        ]
    ]

    msg = f"""
🆕 New FF ID Request

👤 User ID: {user_id}
🎮 Name: {name}
🆔 UID: {uid}
📌 Text: {text}
"""

    for admin in ADMINS:
        await bot.send_message(
            chat_id=admin,
            text=msg,
            reply_markup=InlineKeyboardMarkup(keyboard)
          )
