from fastapi import APIRouter, Depends, HTTPException, status
from app.model import Following, User
from sqlalchemy.orm import Session
from app.database import get_db
from app.oauth import get_current_user
from app import schema


router = APIRouter(prefix='/following', tags=['Follow'])


@router.get('/followers/{user_id}', status_code=status.HTTP_200_OK)
def followers(user_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    """Get the list of followers a user has"""
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        followers = db.query(Following).filter(
            Following.target_user == user_id)
        return {"success": True, "followers": list(followers)}
    else:
        return HTTPException(status_code=200, detail="User not found")


@router.post('/follow/', status_code=status.HTTP_201_CREATED)
def follow_user(request: schema.Follow, db: Session = Depends(get_db),
                current_user: str = Depends(get_current_user)):
    """Follow a user"""
    target_user = db.query(User).filter(
        User.user_id == request.target_user).first()
    if target_user:
        following = db.query(Following).filter(
            Following.target_user == target_user.user_id).first()
        if following:
            if following.user_from == current_user.user_id:
                return HTTPException(status_code=401, detail="You already follow this user")
        if current_user.user_id != target_user.user_id:
            following = Following(target_user=target_user.user_id,
                                  user_from=current_user.user_id)
            # update target user
            target_user.followers = target_user.followers + 1
            # update current user
            following_user = db.query(User).filter(
                User.user_id == current_user.user_id).first()
            following_user.following = following_user.following + 1

            db.add(following)
            db.commit()
            db.refresh(following)
            db.refresh(target_user)
            db.refresh(following_user)
            return {"success": True, "msg": f"You successfully {target_user.username}", "status": status.HTTP_201_CREATED}
        return {"success": False, "msg": "You can't follow yourself", "status": status.HTTP_403_FORBIDDEN}
    else:
        return HTTPException(status_code=404, detail="user not found")


@router.delete('/unfollow/{user_id}', status_code=status.HTTP_200_OK)
def delete_user(user_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    """Unfollow a user"""
    target_user = db.query(User).filter(User.user_id == user_id).first()
    following = db.query(Following).filter(
        Following.target_user == user_id).first()
    if following:
        if following.user_from == current_user.user_id:
            # update target user
            target_user.followers = target_user.followers - 1
            # update current user
            following_user = db.query(User).filter(
                User.user_id == current_user.user_id).first()
            following_user.following = following_user.following - 1

            db.delete(following)
            db.commit()
            db.refresh(target_user)
            db.refresh(following_user)

            return {"success": True, "msg": f"unfollowed {target_user.username}", "status": status.HTTP_200_OK}
        else:
            return HTTPException(status_code=403, detail="unauthorized to make this request")
