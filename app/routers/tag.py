from fastapi import APIRouter, status, Response, Depends, Path
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
import schema
import model
import oauth
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from typing import List

router = APIRouter(
    prefix="/tag",
    tags=["Tag"]
)


@router.get("/", response_model=List[schema.Tag])
async def list_all_tags(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """
    Lists all available tags
    """
    tags = db.query(model.Tag).offset(skip).limit(limit).all()
    return {"success": True, "data": tags}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Tag)
async def create_tag(tag: schema.TagCreate, db: Session = Depends(get_db), user: schema.User = Depends(oauth.get_current_user)):
    """
    Creates a tag
    """
    db_question = db.query(model.Question).filter(
        model.Question.question_id == tag.question_id).first()
    if db_question is None:
        raise HTTPException(status_code=404, detail="Invalid Question ID")
    owner_id = user.user_id
    db_tag = model.Tag(tag_name=tag.tag_name,
                       owner_id=owner_id, question_id=tag.question_id)

    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return {"success": True, "tag_name": tag.tag_name, "tag_id": db_tag.tag_id, "question_id": db_tag.question_id}


@router.delete("/{tag_id}", status_code=status.HTTP_200_OK)
async def delete_tag(
    tag_id: int = Path(
        default=...,
        description="The id of the tag to be deleted."
    ),
    db: Session = Depends(get_db),
    user: schema.User = Depends(oauth.get_current_user)
):
    """
    Deletes the tag that matches the tag_id specified in the url
    """
    tag = db.query(model.Tag).filter(model.Tag.tag_id == tag_id).first()
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found.")
    db.delete(tag)
    db.commit()
    return {"Successfully deleted"}


@router.post("/add-question/")
async def add_tag_to_question(
    add_tag_model: schema.Tag,
    db: Session = Depends(get_db),
    user: schema.User = Depends(oauth.get_current_user)
):
    """
    Adds a tag to a question
    """
    tag = db.query(model.Tag).options(joinedload(model.Tag.questions)).where(
        model.Tag.tag_id == add_tag_model.tag_id).first()
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found.")
    question = db.query(model.Question).filter(
        model.Question.question_id == add_tag_model.question_id).first()
    if question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found.")
    tag.questions.append(question)
    db.commit()
    db.refresh(tag)
    return jsonable_encoder(tag)


@router.get("/{tag_id}/questions", )
async def get_questions_under_tag(
    tag_id: int = Path(
        default=...,
        description="The id of the tag"
    ),
    db: Session = Depends(get_db)
):
    """
    Lists all the questions attached to the tag with the specified id
    """
    tag = db.query(model.Tag).options(joinedload(model.Tag.questions)).where(
        model.Tag.tag_id == tag_id).first()
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found.")
    return jsonable_encoder(tag)

# @router.post("/", status_code=status.HTTP_201_CREATED)
# def Tag(tag: schema.Tag, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
#
#    question = db.query(model.Question).filter(
#        model.Question.question_id == tag.question_id).first()
#    if not question:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                            detail=f"Question with id: {tag.question_id} does not exist.")
#
#    tag_query = db.query(model.Tag).filter(
#        model.Tag.question_id == tag.question_id,
#        model.Tag.user_id == current_user.user_id
#    )
#    found_tag = tag_query.first()
#    if (tag.dir == 1):
#        if found_tag:
#            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
#                                detail=f"user {current_user.user_id} has already tagged on post {tag.question_id}")
#
#        new_tag = model.Tag(question_id=tag.question_id,
#                              user_id=current_user.user_id)
#        db.add(new_tag)
#        db.commit()
#
#        return {"message": "successfully added Tag to Question"}
#    else:
#        if not found_tag:
#            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tag does not exist")
#
#        tag_query.delete(synchronize_session=False)
#        db.commit()
#
#        return {"message": "successfully removed tag"}
