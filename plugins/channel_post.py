#(©)dramaost

import asyncio
import random
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON, CMD_LIST
from helper_func import encode

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(CMD_LIST))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("⏳", quote = True)
    try:
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
        await post_message.reply_text(f"From {message.from_user.mention} (`{message.from_user.id}`)")
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
        await post_message.reply_text(f"From {message.from_user.mention} (`{message.from_user.id}`)")
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went Wrong..!")
        return
    converted_id = post_message.id * abs(client.db_channel.id)
    string = await encode(f"get-{converted_id}")
    link = f"https://t.me/{client.username}?start={string}"

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])

    await reply_text.edit(f"<b>Here is your link</b>\n\n{link}", reply_markup=reply_markup, disable_web_page_preview = True)

    if not DISABLE_CHANNEL_BUTTON:
        await post_message.edit_reply_markup(reply_markup)

@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):

    if DISABLE_CHANNEL_BUTTON:
        return

    converted_id = message.id * abs(client.db_channel.id)
    string = await encode(f"get-{converted_id}")
    link = f"https://t.me/{client.username}?start={string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    try:
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(e)
        pass

REACT_ID = -1001948557982

# @Bot.on_message(filters.chat(REACT_ID))
# async def react_msg_appx(_, message):
#     # chat = await Bot.get_chat(chat_id=REACT_ID)
#     # react = chat.available_reactions
#     # reactions = react.reactions
#     msglink = message.link
#     emoji = "👍"
#     try:
#         await message.react(emoji=emoji)
#         msg = await Bot.send_message(chat_id=1412909688, text=f"**Reaction sent to message:** {msglink}")
#     except Exception as e:
#         msg = await Bot.send_message(chat_id=1412909688, text=f"**Error while reacting:** {e}")
#         pass
