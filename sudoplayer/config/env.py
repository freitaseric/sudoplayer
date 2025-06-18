import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

ERROR_WEBHOOK_URL = os.getenv("ERROR_WEBHOOK_URL")
