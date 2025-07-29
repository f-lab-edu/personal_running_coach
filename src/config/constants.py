from dotenv import load_dotenv
from pathlib import Path
import os

SRC_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = SRC_DIR / ".env"
load_dotenv(ENV_PATH)

### TOKEN ###
JWT_SECRET = os.getenv("JWT_SECRET", None)
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", None)
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7


PLATFORM = ['facebook', 'kakao', ]