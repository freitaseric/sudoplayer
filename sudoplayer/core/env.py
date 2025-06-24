import os
import dotenv


def setup_env():
    dotenv.load_dotenv()


ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise EnvironmentError("token is not defined!")

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_USERNAME = os.environ.get("REDIS_USERNAME", "default")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
