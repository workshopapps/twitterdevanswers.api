from fastapi import APIRouter, status, Response, Depends
from fastapi.exceptions import HTTPException
from .. import schema, model, oauth
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
    prefix="/tag",
    tags=["Tag"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def Tag(tag: schema.Tag, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):

    question = db.query(model.Question).filter(
        model.Question.question_id == tag.question_id).first()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Question with id: {tag.question_id} does not exist.")

    tag_query = db.query(model.Tag).filter(
        model.Tag.question_id == tag.question_id,
        model.Tag.user_id == current_user.user_id
    )
    found_tag = tag_query.first()
    if (tag.dir == 1):
        if found_tag:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.user_id} has already tagged on post {tag.question_id}")

        new_tag = model.Tag(question_id=tag.question_id,
                              user_id=current_user.user_id)
        db.add(new_tag)
        db.commit()

        return {"message": "successfully added Tag to Question"}
    else:
        if not found_tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="tag does not exist")

       tag_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully removed tag"}
