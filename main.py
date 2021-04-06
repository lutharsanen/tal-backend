from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def main():
    return RedirectResponse("/docs")


@app.get("/test")
def test_api(limit: int):
    return {"data": 2*limit}


@app.post("/api/insert-videoid")
def text_analyzer(request: schemas.VideoBase, db: Session = Depends(get_db)):
    new_keyframe_video = models.Video(
        id=request.video_id, description=request.description)
    db.add(new_keyframe_video)
    db.commit()
    db.refresh(new_keyframe_video)
    return {"database_update": "success"}


@app.post("/api/insert-textanalysis")
def text_analyzer(request: schemas.Text, db: Session = Depends(get_db)):
    new_keyframe_text = models.Text(
        keyframe_id=request.keyframe_id, text=request.text, video_id=request.video_id)
    db.add(new_keyframe_text)
    db.commit()
    db.refresh(new_keyframe_text)
    return {"database_update": "success"}


@app.get("/api/all-text")
def get_text(db: Session = Depends(get_db)):
    video_searched = db.query(models.Text).all()
    return video_searched


@app.get("/api/specific-text")
def get_text(text: str, db: Session = Depends(get_db)):
    video_searched = db.query(models.Text).filter(
        models.Text.text.ilike(f'%{text}%')).all()
    return {"results": video_searched}
