from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, String, Float, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import httpx
from datetime import datetime

DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    uid = Column(String, primary_key=True, index=True)
    email = Column(String, index=True)
    first_name = Column(String)
    last_name = Column(String)
    gender = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    run_id = Column(String)
    datetime = Column(DateTime)

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/users/")
async def create_user(num_users: int):
    async with httpx.AsyncClient() as client:
        for _ in range(num_users):
            response = await client.get("https://randomuser.me/api/")
            data = response.json()["results"][0]
            user = User(
                uid=data['login']['uuid'],
                email=data['email'],
                first_name=data['name']['first'],
                last_name=data['name']['last'],
                gender=data['gender'],
                latitude=data['location']['coordinates']['latitude'],
                longitude=data['location']['coordinates']['longitude'],
                run_id="some_run_id", 
                datetime=datetime.utcnow()
            )
            db = SessionLocal()
            db.add(user)
            db.commit()
            db.refresh(user)
            db.close()
    return {"message": "Users created", "num_users": num_users}

@app.get("/users/random/")
async def get_random_user():
    db = SessionLocal()
    user = db.query(User).order_by(func.random()).first()
    db.close()
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

def calculate_vowel_overlap(name1: str, name2: str) -> int:
    vowels = set("aeiouAEIOU")
    name1_vowels = set(filter(lambda char: char in vowels, name1))
    name2_vowels = set(filter(lambda char: char in vowels, name2))
    return len(name1_vowels.intersection(name2_vowels))

@app.get("/users/nearest/{uid}/{count}")
async def get_nearest_users(uid: str, count: int):
    db = SessionLocal()
    user = db.query(User).filter(User.uid == uid).first()
    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    users = db.query(User).filter(User.uid != uid).all()
    nearest_users = sorted(users, key=lambda x: (x.latitude - user.latitude) ** 2 + (x.longitude - user.longitude) ** 2)[:count]

    response = []
    for nearest_user in nearest_users:
        compatibility_score = calculate_vowel_overlap(user.first_name, nearest_user.first_name)
        response.append({
            "uid": nearest_user.uid,
            "email": nearest_user.email,
            "first_name": nearest_user.first_name,
            "last_name": nearest_user.last_name,
            "gender": nearest_user.gender,
            "latitude": nearest_user.latitude,
            "longitude": nearest_user.longitude,
            "run_id": nearest_user.run_id,
            "datetime": nearest_user.datetime,
            "compatibility_score": compatibility_score
        })
    
    db.close()
    return response
