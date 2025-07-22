from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import get_db
from app.db import models
from app.db.database import engine

from app.routers import auth, user, chat, emotion

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(chat.router)
app.include_router(emotion.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}