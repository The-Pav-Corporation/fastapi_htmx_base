from pathlib import Path
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
import jinja_partials

BASE_DIR = Path(__file__).resolve().parent

### Templates ###
TEMPLATES_DIR = str(Path(BASE_DIR, 'templates'))
templates = Jinja2Templates(directory=TEMPLATES_DIR)
jinja_partials.register_starlette_extensions(templates)

### Security ###
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "574a7f0129e7ff33fdebef3a29d0e5d9d8817059f9b98721c742624f94079afd"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
