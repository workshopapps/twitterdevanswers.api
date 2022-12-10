from fastapi import APIRouter, status, Response, Depends, FastAPI
from fastapi.exceptions import HTTPException
from app import schema, model, oauth
from sqlalchemy.orm import Session
from app.database import get_db
# from fastapi_pagination import LimitOffsetPage, add_pagination, paginate


router = APIRouter(
    prefix='/blog',
    tags=['Blog']
)

# get all posts paginated


@router.get("/", status_code=status.HTTP_200_OK)
def get_all_post(db: Session = Depends(get_db)):
    get_all_posts = db.query(model.Blog).all()
    return get_all_posts

# get all posts not paginated


@router.get("/", status_code=status.HTTP_200_OK)
def get_post(db: Session = Depends(get_db)):
    get_post = db.query(model.Blog).all()
    return {"success": True, "data": get_post}


# make posts by a user
@router.post("/", status_code=status.HTTP_201_CREATED)
def post_blog(user_id, request: schema.Blog, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    new_post = model.Blog(title=request.title, body=request.body, blog_user_id=user_id,
                          author=request.author, image_url=request.image_url, post_category=request.post_category)
# make posts by a user

    if current_user.is_admin == True:
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return {"success": True, "data": new_post}
    else:
        return HTTPException(status_code=401, detail="Unauthorized, Only an admin can post blogs")

# get post by blog_id


@router.get("/{blog_id}", status_code=status.HTTP_200_OK)
def get_post_by_blog_id(blog_id, db: Session = Depends(get_db)):
    get_post = db.query(model.Blog).filter(
        model.Blog.blog_id == blog_id).first()
    if not get_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{blog_id} does not exist")
    return get_post

# get all posts by user_id


@router.get("/{user_id}/admin", status_code=status.HTTP_200_OK)
def get_post_by_user_id(user_id, db: Session = Depends(get_db)):
    get_post = db.query(model.Blog).filter(
        model.Blog.blog_user_id == user_id).all()
    if not get_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{user_id} does not exist")
    return get_post


"""
@router.delete("/{user_id}/user", status_code=status.HTTP_200_OK)
def delete_post_by_user_id(user_id, db: Session = Depends(get_db)):
    post_delete = db.query(model.Blog).filter(
        model.Blog.blog_user_id == user_id).delete(synchronize_session=False)
    return {"sucess": True, "data": f"{user_id} deleted"}
"""


@router.delete("/{blog_id}/admin")
def delete_post_by_user_id(blog_id, db: Session = Depends(get_db),
                           current_user: int = Depends(oauth.get_current_user)):
    db_blog = db.query(model.Blog).filter(
        model.Blog.blog_id == blog_id).first()
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Invalid blog id")
    if current_user.is_admin != True or db_blog.blog_user_id != current_user.user_id:
        return HTTPException(
            status_code=400, detail="Only owner and Admins can delete this blog")
    db.delete(db_blog)
    db.commit()
    return {"detail": "success"}

# update post by user id


@router.patch("/{blog_id}/admin", status_code=status.HTTP_202_ACCEPTED)
def update_post_by_blog_id(blog_id, request: schema.Blog, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    post_update = db.query(model.Blog).filter(
        model.Blog.blog_id == blog_id).first()

    if not post_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {blog_id} does not exist")
    if current_user.is_admin == True:
        post_update.title = request.title
        post_update.body = request.body
        post_update.author = request.author
        post_update.image_url = request.image_url
        post_update.post_category = request.post_category
        db.add(post_update)
        db.commit()
        db.refresh(post_update)
        return {"success": True, "data": "update sucessful"}
    else:
        return HTTPException(status_code=401, detail="Only Admins can perform this action")
