from fastapi import APIRouter, status, Response, Depends
from fastapi.exceptions import HTTPException
from .. import schema, model, oauth
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
    prefix="/like",
    tags=["Like"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def like(like: schema.Like, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):

    question = db.query(model.Question).filter(
        model.Question.question_id == like.question_id).first()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Question with id: {like.question_id} does not exist.")

    like_query = db.query(model.Like).filter(
        model.Like.question_id == like.question_id,
        model.Like.user_id == current_user.user_id
    )
    found_like = like_query.first()
    if (like.dir == 1):
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.user_id} has already voted on post {like.question_id}")

        new_like = model.Like(question_id=like.question_id,
                              user_id=current_user.user_id)
        db.add(new_like)
        db.commit()

        return {"message": "successfully added Like"}
    else:
        if not found_like:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="like does not exist")

        like_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully removed like"}
