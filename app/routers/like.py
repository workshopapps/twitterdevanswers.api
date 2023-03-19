from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.exceptions import HTTPException
from app import schema, model, oauth
from sqlalchemy.orm import Session
from app.database import get_db
from app.routers.answer import get_question
from app.routers.notification import create_notification
from uuid import uuid4


router = APIRouter(
    prefix="/like",
    tags=["Like"]
)


@router.get("/{question_id}")
def list_like_question(question_id, db: Session = Depends(get_db)):
    """ List all likes for a specific Question """

    return db.query(model.Like).filter(model.Like.item_id == question_id).all()



@router.get("/posts/{topic_id}")
def list_like_post(topic_id, db: Session = Depends(get_db),current_user: str = Depends(oauth.get_current_user)):
    """ List all likes for a specific Post """

    return db.query(model.Like).filter(model.Like.item_id == topic_id).all()



@router.get("/comments/{comment_id}")
def list_like_comment(comment_id, db: Session = Depends(get_db),current_user: str = Depends(oauth.get_current_user)):
    """ List all likes for a specific Comment """

    return db.query(model.Like).filter(model.Like.item_id == comment_id).all()


# combined endpoints(like & unlike)
@router.post('/toggle_like/') 
def toggle_like(id: str, item_type: str, background_task: BackgroundTasks, db: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
    # Check if the specified ID and item_type exist in the database
    
    if item_type == 'question':
        item = db.query(model.Question).filter_by(question_id=id).first()
    elif item_type == 'topic':
        item = db.query(model.Topic).filter_by(topic_id=id).first()
    elif item_type == 'comment':
        item = db.query(model.Comment).filter_by(comment_id=id).first()
    else:
        raise HTTPException(status_code=400, detail=f"Invalid item_type: {item_type}")

    if not item:
        raise HTTPException(status_code=404, detail=f"{item_type.capitalize()} not found")

    # Check if the user has already liked the item
    like = db.query(model.Like).filter_by(user_id=current_user.user_id, item_id=id, item_type=item_type).first()

    if like:
        # Remove the existing like
        db.delete(like)

        # Update the item's like count
        if item_type == 'question':
            item.total_like -= 1
        elif item_type == 'topic':
            item.total_likes -= 1    
        elif item_type == 'comment':    
            item.total_reactions -= 1
        db.commit()

        # Return the updated like count as a JSON response
        return {"success": True, "data":"Item Unliked Successfully" }

    else:
        # Add a new like
        like = model.Like(
            like_id=uuid4(),
            item_id=id,
            user_id=current_user.user_id,
            item_type=item_type
        )
        db.add(like)
        db.commit()
        db.refresh(like)

        # Update the item's like count
        if item_type == 'question':
            item.total_like += 1
        elif item_type == 'topic':
            item.total_likes += 1    
        elif item_type == 'comment':    
            item.total_reactions += 1
        db.commit()

        # Return the new like data as a JSON response
        return {"success": True, "message":"Item Liked Successfully", "data": {
            "like_id": like.like_id,
            "item_id": like.item_id,
            "user_id": like.user_id,
            "item_type": like.item_type,
        }}
