from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Text, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import os

# Настройки
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bot.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI(title="МеханоБот API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модели БД
class Person(Base):
    __tablename__ = "person"
    
    user_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    photo = Column(String(255), default="default.jpg")
    experience = Column(Integer, default=0)
    money = Column(Integer, default=100)
    hp = Column(Integer, default=100)
    damage = Column(Integer, default=20)
    luck = Column(Integer, default=20)
    level = Column(Integer, default=1)

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Pydantic Схемы
class PersonCreate(BaseModel):
    user_id: int
    chat_id: int
    name: str
    photo: str = "default.jpg"
    level: int = 1

class PersonUpdate(BaseModel):
    name: Optional[str] = None
    photo: Optional[str] = None
    experience: Optional[int] = None
    money: Optional[int] = None
    hp: Optional[int] = None
    damage: Optional[int] = None
    luck: Optional[int] = None
    level: Optional[int] = None

class PersonResponse(BaseModel):
    userId: int
    chatId: int
    name: str
    photo: str
    experience: int
    money: int
    hp: int
    damage: int
    luck: int
    level: int = 1
    
    class Config:
        from_attributes = True

# Вспомогательные функции
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_person(db: Session, chat_id: int, user_id: int):
    return db.query(Person).filter(
        Person.chat_id == chat_id,
        Person.user_id == user_id
    ).first()

# API Эндпоинты

# Person
@app.get("/api/person/id/{chat_id}", response_model=List[PersonResponse])
def get_players_by_chat(chat_id: int, db: Session = Depends(get_db)):
    players = db.query(Person).filter(Person.chat_id == chat_id).all()
    return [
        PersonResponse(
            userId=p.user_id,
            chatId=p.chat_id,
            name=p.name,
            photo=p.photo,
            experience=p.experience,
            money=p.money,
            hp=p.hp,
            damage=p.damage,
            luck=p.luck,
            level=p.level
        )
        for p in players
    ]

@app.post("/api/person/create_alt", status_code=201)
def create_player_alt(data: dict, db: Session = Depends(get_db)):
    try:
        user_id = data.get('user_id')
        chat_id = data.get('chat_id')
        name = data.get('name')
        photo = data.get('photo', 'default.jpg')
        level = data.get('level', 1)
        
        if not all([user_id, chat_id, name]):
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        existing = get_person(db, chat_id, user_id)
        if existing:
            raise HTTPException(status_code=400, detail="Игрок уже существует")
        
        db_player = Person(
            user_id=user_id,
            chat_id=chat_id,
            name=name,
            photo=photo,
            experience=0,
            money=100,
            hp=100,
            damage=20,
            luck=20,
            level=level
        )
        db.add(db_player)
        db.commit()
        db.refresh(db_player)
        return {"message": "Игрок создан"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/person/update")
def update_player(
        chat_id: int,
        user_id: int,
        data: PersonUpdate,
        db: Session = Depends(get_db)
):
    player = get_person(db, chat_id, user_id)
    if not player:
        raise HTTPException(status_code=404, detail="Игрок не найден")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(player, key, value)

    db.commit()
    return {"message": "Игрок обновлён"}

@app.get("/api/person/all", response_model=List[PersonResponse])
def get_all_players(db: Session = Depends(get_db)):
    players = db.query(Person).all()
    return [
        PersonResponse(
            userId=p.user_id,
            chatId=p.chat_id,
            name=p.name,
            photo=p.photo,
            experience=p.experience,
            money=p.money,
            hp=p.hp,
            damage=p.damage,
            luck=p.luck,
            level=p.level
        )
        for p in players
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)