# from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import psiholog, tip_termina, klijent, grupa, termin
from app.database import Base, engine

app = FastAPI()

app.include_router(psiholog.router)
app.include_router(tip_termina.router)
app.include_router(termin.router)
app.include_router(klijent.router)
app.include_router(grupa.router)
