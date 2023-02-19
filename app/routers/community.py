from fastapi import FastAPI,status, Depends, HTTPException, APIRouter, Request
from app import crud, schema , oauth , model
from app.database import get_db
from app.model import *
from typing import List
from sqlalchemy.orm import Session
from app.oauth import get_current_user



router = APIRouter(
    prefix='/community',
    tags=['Community']
)


@router.get('/',status_code=status.HTTP_200_OK)
def fetch_communities( skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """ List to get all communities """

    return crud.get_communities(db, skip=skip, limit=limit)


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_community(request: schema.AddCommunity, db: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):

    if current_user.is_admin == True:
        add_community = model.Community(
            community_id = uuid4(),
            user_id=current_user.user_id,
            name=request.name,
            description=request.description, 
            image_url=request.image_url,
        )
        db.add(add_community)
        db.commit()
        db.refresh(add_community)
        return {"success": True, 
        "community_id": add_community.community_id,
        "name":add_community.name,
        "description": add_community.description,
        }
    else:
        return{"success":False,"message":"You're not authorized to perform this operation"}


# @router.post("/join_community/{community_id}")
# def join_community(request: schema.AddCommunity, community_id:str, db: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
#     # request.owner_id = current_user.user_id
#     if current_user.is_admin == True:
#         add_community = model.Community(
#             community_id = uuid4(),
#             user_id=current_user.user_id,
#             name=request.name,
#             description=request.description, 
#             image_url=request.image_url,
#             # created_at=request.created_at,
#         )
#         db.add(add_community)
#         db.commit()
#         db.refresh(add_community)
#         return {"success": True, 
#         "community_id": add_community.community_id,
#         "name":add_community.name,
#         "description": add_community.description,
#         }
#     else:
#         return{"success":False,"message":"You're not authorized to perform this operation"}


# @router.get('/{user_id}',status_code=status.HTTP_200_OK)
# def fetch_user_id(user_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
#     """ Fetch a user by Id  """

#     user = crud.get_user_id(db, user_id=user_id)
#     if not user:
#         raise HTTPException(
#             status_code=404, detail=f" User {user_id} not found")
#     return {"success": True, 'data': user}


# @router.get('/get/{username}',status_code=status.HTTP_200_OK)
# def fetch_by_username(username: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
#     """Fetches user by username"""
#     user = db.query(model.User).filter(
#         model.User.username == username).first()
#     if user:
#         user_data = crud.get_user(db, username)
#         return {"success": True, 'data': user_data}
#     return HTTPException(status_code=404, detail="Username doesn't exist.")




@router.patch('/edit/{community_id}',status_code=status.HTTP_200_OK)
def update_community(community: schema.UpdateCommunity, _id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """ Update a community by it's id  """

    community_db = db.query(Community).filter(Community.community_id == _id).first()
    if community_db is None:
        raise HTTPException(status_code=404, detail="Community not found")
    if current_user.is_admin == True:
        update_community = db.query(model.Community).filter(
            model.Community.community_id == _id).first()
        if update_community is None:
            raise HTTPException(status_code=404, detail="User not found")

        if isinstance(community, dict):
            update_data = community
        else:
            update_data = community.dict(exclude_unset=True)
        for field in update_data:
            setattr(update_community, field, update_data[field])

        db.add(update_community)
        db.commit()
        db.refresh(update_community)
        return {"success": True, "message": "Community Updated", "data": update_data}
    else:
        return {"success": False, "message":  "You're not authorized to perform this update "}




# @router.delete('/delete/{username}',status_code=status.HTTP_200_OK)
# def delete_user(username: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
#     """ Delete a user by username  """
#     delete_user = crud.delete_user(
#         db, username=username, current_user=current_user)
#     if not delete_user:
#         raise HTTPException(
#             status=404, detail=f" User {username} does not exist")
#     return delete_user


#  TOPICS

@router.get('/topics',status_code=status.HTTP_200_OK)
def fetch_topics( skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """ List to get all topics  """

    return crud.get_topics(db, skip=skip, limit=limit)


@router.get('/topics/{topic_id}',status_code=status.HTTP_200_OK)
def fetch_a_topic( topic_id:str, db: Session = Depends(get_db)):
    """ Fetch a topic from the database """
    topic = db.query(Model.Topic).filter(model.topic.topic_id==topic_id)
    if topic is None:
        return{"success":True,"message":f"Topic with id {topic_id} not found"}
    return {"success":True,"data":topic}


@router.get('/topics/{community_id}',status_code=status.HTTP_200_OK)
def fetch_topics_by_community(community_id :str , db: Session = Depends(get_db)):
    """ List to get all topics in a community """
    return crud.get_topic_in_community(db, community_id = community_id)



@router.post("/post_topic", status_code=status.HTTP_201_CREATED)
def post_topic(request: schema.PostTopic, community_id : str , db: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):

    community =  db.query(Community).filter(Community.community_id == community_id).first()

    if community :
        add_topic = model.Topic(
            topic_id = uuid4(),
            user_id=current_user.user_id,
            community_id = community_id ,
            title=request.title,
            content=request.content, 
            image_url=request.image_url,
        )
        db.add(add_topic)
        db.commit()
        db.refresh(add_topic)
        return {"success": True, 
        "topic_id": add_topic.topic_id,
        "title":add_topic.title,
        "content": add_topic.content,
        "image_url" : add_topic.image_url
        }
    else:
        return{"success":False,"message":f"There is no community {community_id}"}
