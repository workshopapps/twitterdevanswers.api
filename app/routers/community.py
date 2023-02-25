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
def fetch_communities( skip: int = 0, limit: int = 100, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    """ List to get all communities """

    return crud.get_communities(db, skip=skip, limit=limit)


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_community(request: schema.AddCommunity, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):

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


# coming back for you (Logic Not written properly )
@router.post("/join_community/{community_id}")
def join_community( community_id:str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    community = db.query(model.Community).filter(model.Community.community_id == community_id).first()
    if current_user.is_admin == True:
        if community:
            community.total_members +=1
            
            db.add(community)
            db.commit()
            db.refresh(community)
            return {"success": True, 
            "message":"community_joined"}
        else:
            raise HTTPException(
            status_code=404, detail=f" Community not found")    
    else:
        return{"success":False,"message":"You're not authorized to perform this operation"}


@router.get('/get/{community_id}',status_code=status.HTTP_200_OK)
def fetch_a_community(community_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    """ Fetch a Community by Id  """

    community = db.query(model.Community).filter(model.Community.community_id==community_id).first()   
    if not community:
        raise HTTPException(
            status_code=404, detail=f" Community not found")
    return {"success": True, 'data': community}


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
            raise HTTPException(status_code=404, detail="Community not found")

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


# @router.delete('/delete/{community_id}',status_code=status.HTTP_200_OK)
# def delete_community(community_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
#     """ Delete a user by username  """
#     delete_community = crud.delete_community(
#         db, community_id=community_id, current_user=current_user)
#     if not delete_community:
#         raise HTTPException(
#             status=404, detail=f" Community does not exist")
#     return delete_user


#  TOPICS

@router.get('/topics/',status_code=status.HTTP_200_OK)
def fetch_topics( skip: int = 0, limit: int = 100, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    """ List to get all topics  """

    return crud.get_topics(db, skip=skip, limit=limit)


@router.get('/topics/{topic_id}',status_code=status.HTTP_200_OK)
def fetch_a_topic( topic_id:str, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    """ Fetch a topic from the database """
    topic = db.query(model.Topic).filter(model.Topic.topic_id==topic_id).first()
    if topic is None:
        raise HTTPException(
            status_code=404, detail=f" Topic not found")
    return {"success":True,"data":topic}


@router.get('/topics/{community_id}',status_code=status.HTTP_200_OK)
def fetch_topics_by_community(community_id :str , db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    """ List to get all topics in a community """
    return crud.get_topic_in_community(db, community_id = community_id)


@router.post("/post_topic", status_code=status.HTTP_201_CREATED)
def post_topic(request: schema.PostTopic, community_id : str , db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    """ Add a topics in a community """

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
        raise HTTPException(
            status_code=404, detail=f"Community not found ")