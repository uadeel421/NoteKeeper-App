from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# MySQL configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+mysqlconnector://root:password@db:3306/notesdb')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(255))

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/notes")
def read_notes():
    db = SessionLocal()
    notes = db.query(Note).all()
    db.close()
    return {"notes": [note.content for note in notes]}

@app.post("/notes")
def create_note(note: dict):
    db = SessionLocal()
    db_note = Note(content=note['note'])
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    db.close()
    return {"message": "Note created successfully"}
