#(©)dramaost

from pyrogram import __version__
from bot import Bot
from config import OWNER_ID, START_MSG
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = f"<b>○ Version : 0.3.0 (stable)\n○ Dev : <a href='https://t.me/hybridupdates'>HybridUpdates</a>\n○ Language : <code>Python3</code>\n○ Library : <a href='https://docs.pyrogram.org/'>Pyrogram asyncio {__version__}</a>\n○ Channel : @Drama4UK\n○ Support Group : @Hybrid_Chat</b>",
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔙 Back", callback_data = "start"),
                        InlineKeyboardButton("🔒 Close", callback_data = "close")
                    ]#,
                    # [
                    #     InlineKeyboardButton("💰 Donate Us", callback_data = "donate")
                    # ]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
    elif data == "start":
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("ℹ️ About Me", callback_data = "about"),
                    InlineKeyboardButton("🔒 Close", callback_data = "close")
                ]#,
                # [
                #     InlineKeyboardButton("💰 Donate Us", callback_data = "donate")
                # ]
            ]
        )
        await query.message.edit_text(
            text = START_MSG.format(
                first = query.from_user.first_name,
                last = query.from_user.last_name,
                username = None if not query.from_user.username else '@' + query.from_user.username,
                mention = query.from_user.mention,
                id = query.from_user.id
            ),
            reply_markup = reply_markup,
            disable_web_page_preview = True
        )
    # elif data == "donate":
    #     reply_markup = InlineKeyboardMarkup(
    #         [
    #             [
    #                 InlineKeyboardButton("💵 UPI", url = "https://t.me/IUTheFileBot/UPI"),
    #                 InlineKeyboardButton("💳 PayPal", url = "https://www.paypal.me/nadhirah24")
    #             ],
    #             [
    #                 InlineKeyboardButton("🏠 Home", callback_data = "start"),
    #                 InlineKeyboardButton("ℹ️ About Me", callback_data = "about")
    #             ],
    #             [
    #                 InlineKeyboardButton("🔒 Close", callback_data = "close")
    #             ]
    #         ]
    #     )
    #     await query.message.edit_text(
    #         text = DONATE_MSG,
    #         reply_markup = reply_markup
    #     )
    elif data == "disclaimer":
        TEXT = "📂 This bot shares publicly available files \n⚠️ We do not claim ownership of any content share \n\nIf you believe your copyright is being infringed, please contact us 📩"
        await query.answer(TEXT, show_alert=True)

