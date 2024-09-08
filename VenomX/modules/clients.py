from VenomX import config
from pyrogram import Client
from pytgcalls import PyTgCalls


app = Client(
    name="App",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=config.STRING_SESSION,
)

bot = Client(
    name="Bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
)

call = PyTgCalls(app)
