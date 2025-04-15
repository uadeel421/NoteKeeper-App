from fastapi import FastAPI, HTTPException, Depends, Header, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, init_db
from models import Note
from jose import JWTError, jwt
import os

# Initialize app
app = FastAPI()

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup


@app.on_event("startup")
async def startup_event():
    init_db()


async def get_current_user(authorization: str = Header(...)):
    try:
        scheme, token = authorization.split()
        if scheme.lower() != 'bearer':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme"
            )

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("id")
            email = payload.get("sub")
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token payload"
                )
            return {"id": user_id, "email": email}
        except JWTError as e:
            print(f"JWT decode error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    except Exception as e:
        print(f"Auth error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@app.get("/api/notes")
async def get_notes(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    notes = db.query(Note).filter(Note.owner_id == current_user["id"]).all()
    return [{"id": note.id, "content": note.content} for note in notes]


@app.post("/api/notes")
async def create_note(note: dict, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        # Debug log
        print(f"Creating note with content: {note.get('content')}")
        print(f"User ID: {current_user.get('id')}")  # Debug log

        if not note.get('content'):
            raise HTTPException(
                status_code=400, detail="Note content is required")

        db_note = Note(
            content=note['content'],
            owner_id=current_user["id"]
        )

        db.add(db_note)
        db.commit()
        db.refresh(db_note)

        print(f"Note created with ID: {db_note.id}")  # Debug log

        return {
            "message": "Note created successfully",
            "note": {
                "id": db_note.id,
                "content": db_note.content
            }
        }
    except Exception as e:
        db.rollback()
        print(f"Error creating note: {str(e)}")  # Debug log
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/notes/{note_id}")
async def delete_note(note_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == current_user["id"]
        ).first()
    if not db_note:
        raise HTTPException(status_code=404, 
                            detail="Note not found")
    try:
        db.delete(db_note)
        db.commit()
        return {"message": "Note deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
