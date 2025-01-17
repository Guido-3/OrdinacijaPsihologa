from pydantic import BaseModel

# Šema za prijavu korisnika
class LoginSchema(BaseModel):
    username: str
    password: str

# Šema za JWT token
class Token(BaseModel):
    access_token: str
    token_type: str
