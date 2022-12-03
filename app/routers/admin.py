from app import schema, crud
from app.database import get_db
from app.model import *
from typing import List
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, APIRouter, status, Request, Path
from app.oauth import get_current_user
from app import oauth, model

router = APIRouter(
    prefix='/admin',
    tags=['Admin']
)


@router.get('/')
def fetch_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    """ List to get all users """

    return crud.get_users(db, skip=skip, limit=limit)


@router.get('/{username}')
def fetch_user(username: str, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    """ Fetch a user by it's user_id  """

    user = crud.get_user(db, username=username)
    if not user:
        raise HTTPException(
            status_code=404, detail=f" user with user_id : {username} not found")
    return {"success": True, 'data': user}


@router.delete('/delete/{username}')
def delete_user(username: str, db: Session = Depends(get_db)):
    """ Delete a user by it's user_id  """

    delete_user = crud.delete_user(db, username=username)
    if not delete_user:
        raise HTTPException(
            status_code=404, detail=f"user with user_id : {username} does not exist")
    return delete_user


@router.put("/{user_id}")
def update_user(user: schema.UserUpdate, user_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    """ Update a User profile by user_id  """

    user_db = db.query(User).filter(User.user_id == user_id).first()
    if user_db is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user_db.user_id == current_user.user_id or current_user.is_admin == True:
        update_user = db.query(model.User).filter(
            model.User.user_id == user_id).first()

        if update_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        if isinstance(user, dict):
            update_data = user
        else:
            update_data = user.dict(exclude_unset=True)
        for field in update_data:
            setattr(update_user, field, update_data[field])

        db.add(update_user)
        db.commit()
        db.refresh(update_user)
        return {"success": True, "message": "Profile Updated", "data": update_user}


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(question_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    """delete questions using the question_id"""
    delete_question = db.query(model.Question).filter(
        model.Question.question_id == question_id).first()
    if delete_question:
        if delete_question.owner_id == current_user.user_id or current_user.is_admin == True:
            db.delete(delete_question)
            db.commit()
            return {"success": True, "message": delete_question.question_id}
        else:
            return {"success": False, "message": "Not authorized"}


@router.delete("/{answer_id}")
def delete_answer(answer_id: int, db: Session = Depends(get_db),
                  current_user: int = Depends(oauth.get_current_user)):
    """ Delete answer endpoint for a specific question """

    db_answer = get_answer(db=db, answer_id=answer_id)
    if db_answer is None:
        raise HTTPException(status_code=404, detail="Invalid answer id")
    elif db_answer.owner_id != current_user.user_id:
        raise HTTPException(
            status_code=400, detail="Only owner can delete this answer")
    del_answer = db.query(model.Answer).filter(
        model.Answer.answer_id == answer_id).first()
    db.delete(del_answer)
    db.commit()
    return {"detail": "success"}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_tag(tag: schema.TagCreate, db: Session = Depends(get_db), user: schema.User = Depends(oauth.get_current_user)):
    """
    Creates a tag
    """
    db_tag = model.Tag(tag_name=tag.tag_name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


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
