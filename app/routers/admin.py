from app import schema, crud
from app.database import get_db
from app.model import *
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter, status, Path
from app.oauth import get_current_user
from app.routers.answer import get_answer
from app.routers import admin_utils
from app import oauth, model, schema

router = APIRouter(
    prefix='/admin',
    tags=['Admin']
)


def check_admin(user):
    return user.is_admin


@router.get("/viewdevaskwallet")
def get_escrow_wallet(db: Session = Depends(get_db), current_user: schema.User = Depends(get_current_user)):
    "View Admin Wallet"
    if not check_admin(current_user):
        raise HTTPException(
            status_code=401, detail=f"You must be an admin to access this endpoint")
    devaskwallet = admin_utils.get_devask_wallet(db)
    return {"success": True, "data": devaskwallet}


@router.get('/users')
def fetch_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schema.User = Depends(get_current_user)):
    """ List to get all users """
    if not check_admin(current_user):
        raise HTTPException(
            status_code=401, detail=f"You must be an admin to access this endpoint")
    return crud.get_users(db, skip=skip, limit=limit)


@router.get('/user/{username}')
def fetch_user(username: str, db: Session = Depends(get_db), current_user: schema.User = Depends(get_current_user)):
    """ Fetch a user by it's username """
    if not check_admin(current_user):
        raise HTTPException(
            status_code=401, detail=f"You must be an admin to access this endpoint")
    user = crud.get_user(db, username=username)
    if not user:
        raise HTTPException(
            status_code=404, detail=f" user with user_id : {username} not found")
    return {"success": True, 'data': user}


@router.post("/add/{username}")
# , current_user: schema.User = Depends(get_current_user)):
def make_admin(username: str, db: Session = Depends(get_db)):
    "Make a user an admin using his/her username"
    # if current_user.is_admin:
    #     raise HTTPException(
    #         status_code=401, detail=f"You must be an admin to access this endpoint")
    user = db.query(model.User).filter(model.User.username == username).first()
    if not user:
        return HTTPException(
            status_code=404, detail=f"No user found with this username: {username}")
    if user.is_admin:
        return HTTPException(status_code=401, detail=f"User {username} is an admin")
    user.is_admin = True
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"success": True, "message": f"User with username {username} is now an admin"}


@router.post("/remove/{username}")
# , current_user: schema.User = Depends(get_current_user)):
def remove_admin(username: str, db: Session = Depends(get_db)):
    "Remove an admin user using his/her username"
    # if not check_admin(current_user):
    #     raise HTTPException(
    #         status_code=401, detail=f"You must be an admin to access this endpoint")
    user = db.query(model.User).filter(model.User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"No user found for this username: {username}")
    try:
        user.is_admin = False
        db.add(user)
        db.commit()
        db.refresh(user)

        return {"success": True, "message": f"User with username {username} has been stripped of Admin priviledges"}
    except Exception as err:
        raise HTTPException(status_code=502, detail=err)


@router.post("/create_tags", status_code=status.HTTP_201_CREATED)
async def create_tag(tag: schema.TagCreate, db: Session = Depends(get_db), current_user: schema.User = Depends(get_current_user)):
    """
    Creates a tag
    """
    if not check_admin(current_user):
        raise HTTPException(
            status_code=401, detail=f"You must be an admin to access this endpoint")
    db_tag = model.Tag(tag_name=tag.tag_name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


@router.put("/user/{username}")
def update_user(user_update: schema.UserUpdate, username: str, db: Session = Depends(get_db), current_user: schema.User = Depends(get_current_user)):
    """ Update a User profile by user_id  """

    if not check_admin(current_user):
        raise HTTPException(
            status_code=401, detail=f"You must be an admin to access this endpoint")
    user = db.query(model.User).filter(model.User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_update = user_update.dict()
    for field in user_update:
        setattr(user, field, user_update[field])

    db.add(user)
    db.commit()
    db.refresh(user)
    return {"success": True, "message": "Profile Updated", "data": user}


@router.delete('/user/{username}')
def delete_user(username: str, db: Session = Depends(get_db), current_user: schema.User = Depends(get_current_user)):
    """ Delete a user by it's username  """
    if not check_admin(current_user):
        raise HTTPException(
            status_code=401, detail=f"You must be an admin to access this endpoint")
    delete_user = crud.delete_user(
        db, username=username, current_user=current_user)
    if not delete_user:
        raise HTTPException(
            status=404, detail=f" User {username} does not exist")
    return delete_user


@router.delete("/question/{question_id}", status_code=status.HTTP_200_OK)
def delete_question(question_id: str, db: Session = Depends(get_db), current_user: schema.User = Depends(oauth.get_current_user)):
    """delete questions using the question_id"""
    if not check_admin(current_user):
        raise HTTPException(
            status_code=401, detail=f"You must be an admin to access this endpoint")
    delete_question = db.query(model.Question).filter(
        model.Question.question_id == question_id).first()
    if delete_question:
        db.delete(delete_question)
        db.commit()
        return {"success": True, "message": "Question deleted successfully"}
    else:
        return {"success": False, "message": "Question not found"}


@router.delete("/answer/{answer_id}")
def delete_answer(answer_id: str, db: Session = Depends(get_db),
                  current_user: schema.User = Depends(oauth.get_current_user)):
    """ Delete answer endpoint for a specific question """
    if not check_admin(current_user):
        raise HTTPException(
            status_code=401, detail=f"You must be an admin to access this endpoint")
    answer = get_answer(db=db, answer_id=answer_id)
    if answer is None:
        raise HTTPException(status_code=404, detail="Invalid answer id")
    db.delete(answer)
    db.commit()
    return {"success": True, "message": "Answer deleted successfully"}


@router.delete("/tag/{tag_id}", status_code=status.HTTP_200_OK)
async def delete_tag(
    tag_id: str = Path(
        default=...,
        description="The id of the tag to be deleted."
    ),
    db: Session = Depends(get_db),
    current_user: schema.User = Depends(oauth.get_current_user)
):
    """
    Deletes the tag that matches the tag_id specified in the url
    """
    if not check_admin(current_user):
        raise HTTPException(
            status_code=401, detail=f"You must be an admin to access this endpoint")
    tag = db.query(model.Tag).filter(model.Tag.tag_id == tag_id).first()
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found.")
    db.delete(tag)
    db.commit()
    return {"success": True, "message": "Tag deleted successfully"}
