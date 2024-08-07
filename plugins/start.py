#(©)dramaost

import asyncio

from bot import Bot
from temp import temp
from config import (ADMINS, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, FORCE_MSG,
                    PROTECT_CONTENT, START_MSG, INVITE_LINK, LOG_ID, DONATE_MSG)
from database.database import add_user, del_user, full_userbase, present_user, present_user_file, add_user_file, del_user_file, full_userbase_file
from helper_func import decode, encode, get_messages, subscribed
from pyrogram import Client, __version__, filters
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked
from pyrogram.types import InlineKeyboardButton as Button
from pyrogram.types import InlineKeyboardMarkup as Markup
from pyrogram.types import Message


@Bot.on_message(filters.command('start') & filters.private & subscribed)
# @Nbot.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if client.username == "IUTheFileBot":
        check = await present_user(id)
    else:
        check = await present_user_file(id)
    if not check:
        try:
            if client.username == "IUTheFileBot":
                await add_user(id)
                count = len(await full_userbase())
                await client.send_message(LOG_ID, f"#IUBot #NewUser \n\nUser: {message.from_user.mention}\nID: {id}\n\nUsers count: {count}")
            else:
                await add_user_file(id)
                count = len(await full_userbase_file())
                await client.send_message(LOG_ID, f"#IUBot_File #NewUser \n\nUser: {message.from_user.mention}\nID: {id}\n\nUsers count: {count}")
        except:
            pass
    text = message.text
    if len(text)>7:
        if client.username == "IUTheFileBot":
            MARKUP = Markup(
                [
                    [
                        Button("📁 Download files now", url = f"https://t.me/{temp.FILE_UN}?start={message.command[1]}")
                    ]
                ]
            )
            await message.reply_text(f"<i>⚠️ To prevent copyright we moved file sharing to a seperate bot</i>\n\n<b>Click the button below and start the bot for files 👇🏻</b>", reply_markup=MARKUP)
            return
        try:
            string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start,end+1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        temp_msg = await message.reply("⏳")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("Something went wrong..!")
            return
        await temp_msg.edit("Join @DramaOST")

        for msg in messages:
            
            caption = "" if not msg.caption else msg.caption.html

            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption = caption, filename = msg.document.file_name)
            MARKUP = Markup(
                [
                    [
                        Button("⚠️ Disclaimer", callback_data = "disclaimer"),
                        Button("🔗 Share", url = f"https://t.me/share/url?url=https://t.me/{client.username}?start={message.command[1]}")
                    ]
                ]
            )
            if DISABLE_CHANNEL_BUTTON:
                reply_markup = MARKUP
            else:
                reply_markup = MARKUP

            try:
                await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = ParseMode.HTML, reply_markup = reply_markup, protect_content=PROTECT_CONTENT)
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = ParseMode.HTML, reply_markup = reply_markup, protect_content=PROTECT_CONTENT)
            except:
                pass
        return
    else:
        if not client.username == "IUTheFileBot":
            await message.reply_text("<b>Use @IUTheFileBot !</b>")
            return
        reply_markup = Markup(
            [
                [
                    Button("ℹ️ About Me", callback_data = "about"),
                    Button("🔒 Close", callback_data = "close")
                ],
                [
                    Button("💰 Donate Us", callback_data = "donate")
                ]
            ]
        )
        await message.reply_text(
            text = START_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
            reply_markup = reply_markup,
            disable_web_page_preview = True,
            quote = True
        )
        return

    
#=====================================================================================##

WAIT_MSG = """"<b>Processing ...</b>"""

REPLY_ERROR = """<code>Use this command as a reply to any telegram message without any spaces.</code>"""

#=====================================================================================##

    
@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    id = message.from_user.id
    if client.username == "IUTheFileBot":
        if not await present_user(id):
            try:
                await add_user(id)
                count = len(await full_userbase())
                await client.send_message(LOG_ID, f"#IUBot #NewUser \n\nUser: {message.from_user.mention}\nID: {id}\n\nUsers count: {count}")
            except:
                pass
    else:
        if not await present_user_file(id):
            try:
                await add_user_file(id)
                count = len(await full_userbase_file())
                await client.send_message(LOG_ID, f"#IUBot_File #NewUser \n\nUser: {message.from_user.mention}\nID: {id}\n\nUsers count: {count}")
            except:
                pass
    url = INVITE_LINK
    buttons = [
        [
            Button(
                "Join Channel",
                url = url)
        ]
    ]
    try:
        buttons.append(
            [
                Button(
                    text = 'Try Again',
                    url = f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text = FORCE_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
        reply_markup = Markup(buttons),
        quote = True,
        disable_web_page_preview = True
    )

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    if client.username == "IUTheFileBot":
        users = await full_userbase()
    else:
        users = await full_userbase_file()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        args = message.text.split()
        if len(args) == 1:
            if client.username == "IUTheFileBot":
                query = await full_userbase()
            else:
                query = await full_userbase_file()
            broadcast_msg = message.reply_to_message
            total = 0
            successful = 0
            blocked = 0
            deleted = 0
            unsuccessful = 0
            
            pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
            for chat_id in query:
                try:
                    await broadcast_msg.copy(chat_id)
                    successful += 1
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await broadcast_msg.copy(chat_id)
                    successful += 1
                except UserIsBlocked:
                    await del_user(chat_id)
                    blocked += 1
                except InputUserDeactivated:
                    await del_user(chat_id)
                    deleted += 1
                except:
                    unsuccessful += 1
                    pass
                total += 1
            
            status = f"""<b><u>Broadcast Completed</u>

    Total Users: <code>{total}</code>
    Successful: <code>{successful}</code>
    Blocked Users: <code>{blocked}</code>
    Deleted Accounts: <code>{deleted}</code>
    Unsuccessful: <code>{unsuccessful}</code></b>"""
            
            return await pls_wait.edit(status)
        elif len(args) == 2:
            fwd = message.command[1]
            if not fwd == "-f":
                msg = await message.reply(REPLY_ERROR)
                await asyncio.sleep(8)
                await msg.delete()
            query = await full_userbase()
            broadcast_msg = message.reply_to_message
            total = 0
            successful = 0
            blocked = 0
            deleted = 0
            unsuccessful = 0
            
            pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
            for chat_id in query:
                try:
                    await broadcast_msg.forward(chat_id)
                    successful += 1
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await broadcast_msg.forward(chat_id)
                    successful += 1
                except UserIsBlocked:
                    await del_user(chat_id)
                    blocked += 1
                except InputUserDeactivated:
                    await del_user(chat_id)
                    deleted += 1
                except:
                    unsuccessful += 1
                    pass
                total += 1
            
            status = f"""<b><u>Broadcast Completed</u>

    Total Users: <code>{total}</code>
    Successful: <code>{successful}</code>
    Blocked Users: <code>{blocked}</code>
    Deleted Accounts: <code>{deleted}</code>
    Unsuccessful: <code>{unsuccessful}</code></b>"""
            
            return await pls_wait.edit(status)
    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()


@Bot.on_message(filters.private & filters.command('send') & filters.user(ADMINS))
async def send_message_to_chat(client: Bot, message: Message):
    user = message.chat
    user_id = message.from_user.id
    if message.reply_to_message:
        broadcast_msg = message.reply_to_message
    else:
        broadcast_msg = await user.ask("Send / forward the message you wanna send to the chat:")
    chatID = await user.ask("Send Chat ID:")
    chat_id = int(chatID.text)
    if not chat_id:
        await client.send_message(chat_id=user_id, text="⚠️ Send correct chat_id, try again with /send")
        return
    chat = await client.get_chat(chat_id=chat_id)
    if not chat:
        await client.send_message(chat_id=user_id, text="⚠️ Make sure i am admin in the chat, try again with /send")
        return
    try:
        post = await broadcast_msg.copy(chat_id)
        await client.send_message(chat_id=user_id, text=f"✅ Posted to the chat: {chat_id}\nLink: {post.link}", disable_web_page_preview=True)
    except Exception as e:
        await client.send_message(chat_id=user_id, text=f"⚠️ Error while sending the post\n\n```Error:\n{e}```")

@Bot.on_message(filters.command('donate') & filters.private)
async def donate_handler(client: Client, message: Message):
    reply_markup = Markup(
        [
            [
                Button("💵 UPI", url = "https://t.me/IUTheFileBot/UPI"),
                Button("💳 PayPal", url = "https://www.paypal.me/nadhirah24")
            ],
            [
                Button("🏠 Home", callback_data = "start"),
                Button("ℹ️ About Me", callback_data = "about")
            ],
            [
                Button("🔒 Close", callback_data = "close")
            ]
        ]
    )
    await message.reply_text(
        text = DONATE_MSG,
        reply_markup = reply_markup
    )




