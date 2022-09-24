from pathlib import Path
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from .secrets import ULTRA_SECRET_KEY
import jinja_partials

BASE_DIR = Path(__file__).resolve().parent

# Templates #
TEMPLATES_DIR = Path(BASE_DIR, 'templates')
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
jinja_partials.register_starlette_extensions(templates)

# Security #
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = ULTRA_SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
