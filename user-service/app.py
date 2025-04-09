from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import get_db, engine
from .models import Base, UserProfile

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/users/profile/{user_id}")
async def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@app.post("/api/users/profile")
async def create_user_profile(profile: dict, db: Session = Depends(get_db)):
    try:
        db_profile = UserProfile(
            user_id=profile['user_id'],
            email=profile['email'],
            name=profile['name'],
            bio=profile.get('bio'),
            avatar_url=profile.get('avatar_url')
        )
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        return {"message":"Profile created successfully","profile": db_profile}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/users/profile/{user_id}")
async def update_user_profile(user_id: int, profile: dict, db: Session = Depends(get_db)):
    db_profile = db.query(UserProfile).filter(
        UserProfile.user_id == user_id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    for key, value in profile.items():
        if hasattr(db_profile, key):
            setattr(db_profile, key, value)

    try:
        db.commit()
        db.refresh(db_profile)
        return {"message": "Profile updated successfully", "profile": db_profile}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
