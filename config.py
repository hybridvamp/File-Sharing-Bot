#(©)dramaost

import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv() 

TG_BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
APP_ID = int(os.environ.get("APP_ID", ""))
API_HASH = os.environ.get("API_HASH", "")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", ""))
LOG_ID = int(os.environ.get("LOG_ID", ""))
OWNER_ID = int(os.environ.get("OWNER_ID", ""))
PORT = os.environ.get("PORT", "8080")
DB_URI = os.environ.get("DATABASE_URL", "")
DB_NAME = os.environ.get("DATABASE_NAME", "iufilebot")
FORCE_SUB_CHANNELS = os.environ.get("FORCE_SUB_CHANNELS", False)
INVITE_LINK = os.environ.get("INVITE_LINK", "")
CMD_LIST = ['start','users','broadcast','batch','genlink','stats','donate','list','send']

try:
    FORCE_SUB_CHANNELS = int(FORCE_SUB_CHANNELS)
except ValueError:
    print(f"Invalid value for FORCE_SUB_CHANNELS: {FORCE_SUB_CHANNELS}")

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "10"))

START_MSG = os.environ.get("START_MESSAGE", "Hello {first}!\n\nI am a File Sharing Bot Made specially for @Dramaost for file sharing purposes")
try:
    ADMINS=[]
    for x in (os.environ.get("ADMINS", "").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list doesn't contain valid integers.")

FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "Hello {first}\n\n<b>You'll need to join my Channel to use me\n\nPlease kindly join the channel</b>")

#set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

#set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

#Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "❌ Don't send me messages directly, I'm just a File Sharing bot!\nJoin: @DramaOST"

DONATE_MSG = """
<b>Donate us to keep the service alive 🙂

Many of the Members, already know that the uploading expenses are taken from the donations, we need atleast a minimum amount to keep everything in our hands, the OTT subscription and also the bot expenses 😐

We are not forcing you to pay, but any amount of donation is appreciated 😍

Please donate any amount, so that we can together complete D&O monthly donation target.

Monthly targeted Donation is 27$ only.. kindly donate us to reach the target to continue our service in the coming month.
</b>
You can pay through - 
<a href='https://graph.org/file/b26c631f19b16943a4d96.jpg'>\u2063</a>
For Indians - Gpay/Phonepay/Paytm - <code>pavalad68@okhdfcbank</code> or <a href='https://t.me/IUTheFileBot?start=Z2V0LTM1ODY4NTgwMzcxMzE0MA'>scan the QR</a>

For outside Indian pay through PayPal - https://www.paypal.me/nadhirah24

\u2063
"""

ADMINS.append(OWNER_ID)

LOG_FILE_NAME = "iufilebot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
