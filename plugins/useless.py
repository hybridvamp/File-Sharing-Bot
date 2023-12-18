from bot import Bot
from pyrogram.types import Message
from pyrogram import filters
from config import ADMINS, BOT_STATS_TEXT, USER_REPLY_TEXT
from datetime import datetime
from helper_func import get_readable_time
from database.database import full_userbase

@Bot.on_message(filters.command('stats') & filters.user(ADMINS))
async def stats(bot: Bot, message: Message):
    now = datetime.now()
    uptime = get_readable_time(now - bot.start_timestamp)
    await message.reply(BOT_STATS_TEXT.format(uptime))

@Bot.on_message(filters.command("list") & filters.user(ADMINS))
async def get_users_ids(client, message: Message):
    reply_message = await message.reply_text("Checking users count...")
    user_ids = await full_userbase()    
    
    await reply_message.edit_text(f"{len(user_ids)} users found on db")
    await reply_message.edit_text(f"{len(user_ids)} users found on db \n**Creating userlist file...**")
    
    file_message = await message.reply_text("Creating userlist file...")
    with open("user_ids.txt", "w") as file:
        for i, user_id in enumerate(user_ids):
            file.write(f"{user_id}" + "\n")
            if (i + 1) % 1000 == 0:
                await file_message.edit_text(f"Creating userlist file... {i+1}/{len(user_ids)}")
    
    await file_message.edit_text("Userlist file created.")
    await client.send_document(chat_id=message.chat.id, document="user_ids.txt", file_name="user_ids.txt")
    await file_message.delete()
    await reply_message.delete()
    os.remove("user_ids.txt")

@Bot.on_message(filters.private & filters.incoming)
async def useless(_,message: Message):
    if USER_REPLY_TEXT:
        await message.reply(USER_REPLY_TEXT)
