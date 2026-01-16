from os import getenv


# Bot information
API_ID = getenv("API_ID", "23416113")
API_HASH = getenv("API_HASH", "5f66046e7129c9bf6e2b3da943ae2993")
BOT_TOKEN = getenv("BOT_TOKEN", "")

#Koyeb Vars And VPS 
URL = getenv("URL", "")
PORT = int(getenv("PORT", "8080"))
PICS = (getenv('PICS', ' ')).split() 
GRP_LNK = getenv('GRP_LNK', 'https://t.me/+-r5KwO5DXEoxODFl')')
CHNL_LNK = getenv('CHNL_LNK', 'https://t.me/+AEHdKFeiNt9jMjk1')

# Bot Admins & Channels
LOG_CHANNEL = int(getenv('LOG_CHANNEL', "-1003523852458"))
POSTER_CHANNEL = int(getenv('POSTER_CHANNEL', "-1003323487847"))

#Mongo DB Vars 
DATABASE_URL = getenv('SECOND_FILES_DATABASE_URL', "mongodb+srv://vinod974323_db_user:bmDLcs8ExE7T2yxX@cluster0.wln6cms.mongodb.net/?appName=Cluster0")
DATABASE_NAME = getenv("DATABASE_NAME", "aman")
COLLECTION_NAME = getenv("COLLECTION_NAME", 'Telegram_Files')
