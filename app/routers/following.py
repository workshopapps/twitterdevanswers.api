from fastapi import APIRouter, Depends, HTTPException, status
from model import Following, User
from sqlalchemy.orm import Session
from database import get_db
from oauth import get_current_user
import schema


router = APIRouter(prefix='/following', tags=['Follow'])


@router.post('/follow/{user_id}', status_code=status.HTTP_201_CREATED)
def follow_user(user_id: int, request: schema.Follow, db: Session = Depends(get_db),
                current_user: int = Depends(get_current_user)):
    """Follow a user"""
    target_user = db.query(User).filter(User.user_id == user_id).first()
    if target_user:
        if current_user.user_id != target_user.user_id:
            following = Following(target_user=target_user.user_id,
                                  user_from=current_user.user_id)
            db.add(following)
            db.commit()
            db.refresh(following)
            return {"success": True, "msg": f"You successfully {target_user.username}", "status": status.HTTP_201_CREATED}
        return {"success": False, "msg": "You can't follow yourself", "status": status.HTTP_403_FORBIDDEN}
    else:
        return HTTPException(status_code=404, detail="user not found")


@router.delete('/unfollow/{user_id}', status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    """Unfollow a user"""
    target_user = db.query(User).filter(User.user_id == user_id).first()
    following = db.query(Following).filter_by(
        target_user=user_id, user_from=current_user.user_id).first()
    if following:
        db.delete(following)
        db.commit()
        return {"success": True, "msg": f"unfollowed {target_user.username}", "status": status.HTTP_200_OK}
