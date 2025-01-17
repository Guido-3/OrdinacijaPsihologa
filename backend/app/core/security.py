from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt

# Konfiguracija za hashovanje lozinki
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT podešavanja
SECRET_KEY = "tajni_kljuc"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Funkcija za hashovanje lozinke
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Funkcija za proveru hashovane lozinke
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Funkcija za kreiranje JWT tokena
def create_access_token(user_data: dict, expires_delta: timedelta = None):
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    
    to_encode = {
        "sub": user_data["username"],  # Korisničko ime
        "id": str(user_data["id"]),  # ID korisnika, obavezno string
        "exp": expire
    }

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
