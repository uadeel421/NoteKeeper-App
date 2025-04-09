import os
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

load_dotenv()

# MySQL configuration
DATABASE_URL = os.getenv(
    'DATABASE_URL', 'mysql+mysqlconnector://kpadmin:sdfdsf8^@python-dbserver.mysql.database.azure.com:3306/pyth-micros-db?ssl_ca=backend/ssl/DigiCertGlobalRootCA.crt.pem')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    name = Column(String(255))
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(255), nullable=False)  # Make content required
    # Make owner_id required
    owner_id = Column(Integer, nullable=False, index=True)


# Security setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # Specifically allow your frontend origin
    allow_origins=["http://localhost:5000"],
    allow_credentials=True,  # Important for cookies/authentication
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the DB session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utility functions


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependency to get current user


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return {"email": email, "id": user.id}

# Authentication endpoints


@app.post("/api/signup")
def signup(user: dict, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user['email']).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user['password'])
    db_user = User(
        email=user['email'],
        name=user['name'],
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created successfully"}


@app.post("/api/login")
def login(form_data: dict, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == form_data['email']).first()
    if not db_user or not verify_password(form_data['password'], db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email, "id": db_user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/api/notes")
def read_notes(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    notes = db.query(Note).filter(Note.owner_id == current_user['id']).all()
    # Return notes array directly instead of wrapping in "notes" object
    return [{"id": note.id, "content": note.content} for note in notes]


@app.post("/api/notes")
def create_note(note: dict, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        if not note.get('content'):
            raise HTTPException(
                status_code=400, detail="Note content is required")

        db_note = Note(
            content=note['content'],
            owner_id=current_user['id']
        )
        db.add(db_note)
        db.commit()
        db.refresh(db_note)

        return {
            "message": "Note created successfully",
            "note": {
                "id": db_note.id,
                "content": db_note.content,
                "owner_id": db_note.owner_id
            }
        }
    except Exception as e:
        db.rollback()
        print(f"Error creating note: {e}")  # Add logging
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_note = db.query(Note).filter(Note.id == note_id,
                                    Note.owner_id == current_user['id']).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(db_note)
    db.commit()
    return {"message": "Note deleted successfully"}
