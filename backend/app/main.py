# from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import psiholog, tip_termina, klijent, grupa, termin, auth
from app.database import Base, engine

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Dozvoljavamo Vite frontend
    allow_credentials=True,
    allow_methods=["*"],  # Dozvoljavamo sve HTTP metode
    allow_headers=["*"],  # Dozvoljavamo sve zaglavlja
)
app.include_router(psiholog.router)
app.include_router(tip_termina.router)
app.include_router(termin.router)
app.include_router(klijent.router)
app.include_router(grupa.router)
app.include_router(auth.router)