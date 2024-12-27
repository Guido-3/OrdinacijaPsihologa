# from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import psiholog, tip_termina,  termin, klijent, grupa
from app.database import Base, engine

# @asynccontextmanager
# def lifespan(app: FastAPI):
#     print("Starting the app")
#     # Base.metadata.create_all(engine)
#     # print("kreirane su")
#     yield
#     print("Shutting down the app")

app = FastAPI()

app.include_router(psiholog.router)
app.include_router(tip_termina.router)
app.include_router(termin.router)
app.include_router(klijent.router)
app.include_router(grupa.router)
