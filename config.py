from os import getenv


# Bot information
API_ID = getenv("API_ID", "17108931")
API_HASH = getenv("API_HASH", "")
BOT_TOKEN = getenv("BOT_TOKEN", "")

#Koyeb Vars And VPS 
URL = getenv("URL", "")
PORT = int(getenv("PORT", "8080"))
PICS = (getenv('PICS', ' ')).split() 
GRP_LNK = getenv('GRP_LNK', 'https://t.me/')
CHNL_LNK = getenv('CHNL_LNK', '')

# Bot Admins & Channels
LOG_CHANNEL = int(getenv('LOG_CHANNEL', "-100"))
POSTER_CHANNEL = int(getenv('POSTER_CHANNEL', "-100"))

#Mongo DB Vars 
DATABASE_URL = getenv('SECOND_FILES_DATABASE_URL', "+srv://:@cluster0.")
DATABASE_NAME = getenv("DATABASE_NAME", "aman")
COLLECTION_NAME = getenv("COLLECTION_NAME", 'Telegram_Files')
