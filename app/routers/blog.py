from fastapi import APIRouter, status, Response, Depends,FastAPI
from fastapi.exceptions import HTTPException
from app import schema, model, oauth
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi_pagination import LimitOffsetPage, add_pagination, paginate


router = APIRouter(
    prefix='/blog',
    tags=['Blog']
)

#get all posts paginated
@router.get("/",status_code=status.HTTP_200_OK,response_model=LimitOffsetPage[schema.Blog])
def get_all_post(db: Session = Depends(get_db)):
    get_all_posts = db.query(model.Blog).all()
    return paginate(get_all_posts)
add_pagination(router)

#get all posts not paginated
@router.get("/",status_code=status.HTTP_200_OK)
def get_post(db: Session = Depends(get_db)):
    get_post = db.query(model.Blog).all()
    return {"success": True, "data": get_post}    

#make posts by a user
@router.post("/",status_code=status.HTTP_201_CREATED)
def post_blog(user_id,request:schema.Blog,db:Session=Depends(get_db), admin=Depends(oauth.get_admin)):
    new_post =  model.Blog(title=request.title,body=request.body,blog_user_id=user_id,author=request.author,image_url=request.image_url,post_category=request.post_category)
    db.add(new_post)
    db.commit() 
    db.refresh(new_post)
    return {"success":True,"data":new_post}

#get post by blog_id
@router.get("/{blog_id}",status_code=status.HTTP_200_OK)
def get_post_by_blog_id(blog_id,db:Session=Depends(get_db)):
    get_post = db.query(model.Blog).filter(model.Blog.blog_id == blog_id).first()
    if not get_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{blog_id} does not exist")
    return get_post

#get all posts by user_id
@router.get("/{user_id}/user",status_code=status.HTTP_200_OK)
def get_post_by_user_id(user_id,db:Session=Depends(get_db)):
    get_post = db.query(model.Blog).filter(model.Blog.blog_user_id == user_id).all()
    if not get_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{user_id} does not exist")
    return get_post

#delete post by user_id
@router.delete("/{user_id}/user",status_code=status.HTTP_200_OK)
def delete_post_by_user_id(user_id,db:Session=Depends(get_db), admin = Depends(oauth.get_admin)):
    post_delete = db.query(model.Blog).filter(model.Blog.blog_user_id == user_id).delete(synchronize_session=False)
    return {"sucess":True,"data":f"{user_id} deleted"}

#update post by user id
@router.patch("/{user_id}/user",status_code=status.HTTP_202_ACCEPTED)
def update_post_by_user_id(user_id,request:schema.Blog,db:Session=Depends(get_db),  admin = Depends(oauth.get_admin)):
    post_update = db.query(model.Blog).filter(model.Blog.blog_user_id == user_id).first()
    if not post_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{user_id} does not exist")
    post_update.title = request.title
    post_update.body = request.body
    post_update.author = request.author
    post_update.image_url = request.image_url
    post_update.post_category = request.post_category
    db.commit()
    return {"success":True,"data":"update sucessful"}