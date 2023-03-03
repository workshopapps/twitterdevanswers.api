from fastapi import FastAPI, status, Depends, HTTPException, APIRouter, Request
from app import crud, schema, oauth, model
from app.database import get_db
from app.model import *
from typing import List
from sqlalchemy.orm import Session
from app.oauth import get_current_user


router = APIRouter(
    prefix='/community',
    tags=['Community']
)


@router.get('/', status_code=status.HTTP_200_OK)
def fetch_communities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    """ List to get all communities """

    return crud.get_communities(db, skip=skip, limit=limit)


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_community(request: schema.AddCommunity, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):

    if current_user.is_admin == True:
        add_community = model.Community(
            community_id=uuid4(),
            user_id=current_user.user_id,
            name=request.name,
            description=request.description,
            image_url=request.image_url,
            users=[]
        )
        db.add(add_community)
        db.commit()
        db.refresh(add_community)
        return {"success": True, "data" :{
                "community_id": add_community.community_id,
                "name": add_community.name,
                "description": add_community.description
                }}
    else:
        return {"success": False, "message": "You're not authorized to perform this operation"}


@router.post("/join_community/{community_id}")
def join_community(community_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    community = db.query(model.Community).filter(
        model.Community.community_id == community_id).first()
    present = db.query(model.Community).filter().first()    
    if community:
        new_total = community.total_members + 1
        community.total_members = new_total
        community.users.append(current_user)
        db.add(community)
        db.commit()
        db.refresh(community)
        return {"success": True,
                "message": f" You have successfully joined {community.name}"}
    else:
        raise HTTPException(
            status_code=404, detail=f" Community not found")


@router.post("/leave_community/{community_id}")
def leave_community(community_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    community = db.query(model.Community).filter(
        model.Community.community_id == community_id).first()
    if community:
        new_total = community.total_members - 1
        community.total_members = new_total
        for i, user in enumerate(community.users):
            if user.user_id == current_user.user_id:
                community.users.pop(i)   
        db.add(community)
        db.commit()
        db.refresh(community)
        return {"success": True,
                "message": f"Left {community.name} successfully"}
    else:
        raise HTTPException(
            status_code=404, detail=f" Community not found")


@router.get('/get/{community_id}', status_code=status.HTTP_200_OK)
def fetch_a_community(community_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    """ Fetch a Community by Id  """

    community = db.query(model.Community).filter(
        model.Community.community_id == community_id).first()
    if not community:
        raise HTTPException(
            status_code=404, detail=f" Community not found")
    users = community.users
    return {"success": True, 'data': community}


@router.get('/search/{community_name}', status_code=status.HTTP_200_OK)
def fetch_by_community_name(community_name: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    """ Fetch a Community by Name  """

    community = db.query(model.Community).filter(
        model.Community.name == community_name).first()
    if not community:
        raise HTTPException(
            status_code=404, detail=f" Community not found")
    users = community.users
    return {"success": True, 'data': community}


@router.patch('/edit/{community_id}', status_code=status.HTTP_200_OK)
def update_community(community: schema.UpdateCommunity, _id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """ Update a community by it's id  """

    community_db = db.query(Community).filter(
        Community.community_id == _id).first()
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


@router.delete('/delete/{community_id}',status_code=status.HTTP_200_OK)
def delete_community(community_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    """ Delete a user by id  """
    return crud.delete_community(
        db, community_id=community_id, current_user=current_user)
    

#  TOPICS

@router.get('/topics/', status_code=status.HTTP_200_OK)
def fetch_topics(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    """ List to get all topics  """

    return crud.get_topics(db, skip=skip, limit=limit)


@router.get('/topic/{topic_id}', status_code=status.HTTP_200_OK)
def fetch_a_topic(topic_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    """ Fetch a topic from the database """
    topic = db.query(model.Topic).filter(
        model.Topic.topic_id == topic_id).first()
    if topic is None:
        raise HTTPException(
            status_code=404, detail=f" Topic not found")
    return {"success": True, "data": topic}


@router.get('/topics/{community_id}', status_code=status.HTTP_200_OK)
def fetch_topics_by_community(community_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    """ List to get all topics in a community """
    return crud.get_topic_in_community(db, community_id=community_id)


@router.post("/post_topic/", status_code=status.HTTP_201_CREATED)
def post_topic(request: schema.PostTopic, community_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    """ Add a topics in a community """

    community = db.query(Community).filter(
        Community.community_id == community_id).first()

    if community:
        for i, user in enumerate(community.users):
            if user.user_id == current_user.user_id:   
                add_topic = model.Topic(
                    topic_id=uuid4(),
                    user_id=current_user.user_id,
                    community_id=community_id,
                    title=request.title,
                    content=request.content,
                    image_url=request.image_url,
                )
                db.add(add_topic)
                db.commit()
                db.refresh(add_topic)
                return {"success": True, "message":"Topic yet to be reviewed", "data":{ 
                "topic_id": add_topic.topic_id,
                "title":add_topic.title,
                "content": add_topic.content,
                "image_url" : add_topic.image_url
                }}
        raise HTTPException(
            status_code=404, detail=f" User has not joined {community.name}")                    
    else:
        raise HTTPException(
            status_code=404, detail=f"Community not found ")


@router.patch("/approve_topic/{topic_id}")
def approve_topic(topic_id:str,db:Session = Depends(get_db),current_user : str = Depends(oauth.get_current_user)):
    topic = db.query(Topic).filter(Topic.topic_id == topic_id).first()

    if topic :
        if current_user.is_admin == True:
            if topic.is_approved == True:
                return HTTPException(status_code=401, detail="Topic has been reviewed")
            else:
                topic.is_approved = True
                db.add(topic)
                db.commit()
                db.refresh(topic)
                return{"success":True,"message":"Topic has been Approved"}
        else:
            return HTTPException(status_code=401, detail="Action can only be performed by an admin")
    else:
        return HTTPException(status_code=404, detail=f"Topic not found")



@router.patch('/topic/edit/{topic_id}',status_code=status.HTTP_200_OK)
def update_topic(topic: schema.UpdateTopic, _id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """ Update a Topic by it's id  """

    topic_db = db.query(Topic).filter(Topic.topic_id == _id).first()
    if topic_db is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    if current_user.user_id == topic_db.user_id:
        update_topic = db.query(model.Topic).filter(
            model.Topic.topic_id == _id).first()
        if update_topic is None:
            raise HTTPException(status_code=404, detail="Topic not found")

        if isinstance(topic, dict):
            update_data = topic
        else:
            update_data = topic.dict(exclude_unset=True)
        for field in update_data:
            setattr(update_topic, field, update_data[field])

        db.add(update_topic)
        db.commit()
        db.refresh(update_topic)
        return {"success": True, "message": "Topic Updated", "data": update_data}
    else:
        return {"success": False, "message":  "You're not authorized to perform this update "}


@router.get('/topics/user/{user_id}')
def get_topic_user(user_id:str,db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    """ Get all topics a user created from the database based on their id  """
    
    return crud.get_topic_user(db,user_id=user_id)


@router.delete('/delete/topic/{topic_id}',status_code=status.HTTP_200_OK)
def delete_topic(topic_id:str,db :Session = Depends(get_db),current_user : str = Depends(get_current_user)):
    """ Delete a topic """

    return crud.delete_topic(db,topic_id=topic_id,current_user=current_user)

# COMMENTS            

@router.post('/add_comment/')
def add_comment(request:schema.AddComment,topic_id:str,db: Session = Depends(get_db),current_user:str = Depends(get_current_user)):
    """ Add a comment  """
    topic = db.query(model.Topic).filter(model.Topic.topic_id==topic_id).first()
    comment = db.query(model.Comment).filter(model.Comment.topic_id == topic_id).all()
    total_comments = len(comment) + 1
    
    if topic :
        add_comment = model.Comment(
            comment_id = uuid4(),
            topic_id = topic_id,
            user_id = current_user.user_id,
            content = request.content,
            image_url = request.image_url
        )
        topic.total_comments = total_comments
        db.add(add_comment)
        db.commit()
        db.refresh(add_comment)

        return{
            "success" : True, "data":{
            "comment_id" : add_comment.comment_id,
            "content": add_comment.content,
            "image_url" : add_comment.image_url
        }}
    else:
        raise HTTPException(
            status_code=404, detail=f"Topic not found , add a topic first")    


@router.patch('/comment/edit/{comment_id}',status_code=status.HTTP_200_OK)
def update_comment(comment: schema.UpdateComment, _id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """ Update a comment by it's id  """

    comment_db = db.query(Comment).filter(Comment.comment_id == _id).first()
    if comment_db is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if current_user.user_id == comment_db.user_id:
        update_comment = db.query(model.Comment).filter(
            model.Comment.comment_id == _id).first()
        if update_comment is None:
            raise HTTPException(status_code=404, detail="Comment not found")

        if isinstance(comment, dict):
            update_data = comment
        else:
            update_data = comment.dict(exclude_unset=True)
        for field in update_data:
            setattr(update_comment, field, update_data[field])

        db.add(update_comment)
        db.commit()
        db.refresh(update_comment)
        return {"success": True, "message": "Community Updated", "data": update_data}
    else:
        return {"success": False, "message":  "You're not authorized to perform this update "}


@router.get('/comments/',status_code=status.HTTP_200_OK)
def fetch_comments( skip: int = 0, limit: int = 100, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    """ List to get all comments  """

    return crud.get_comments(db, skip=skip, limit=limit)


@router.get('/comments/{comment_id}',status_code=status.HTTP_200_OK)
def fetch_a_comment( comment_id:str, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    """ Fetch a comment from the database """
    comment = db.query(model.Comment).filter(model.Comment.comment_id==comment_id).first()
    if comment is None:
        raise HTTPException(
            status_code=404, detail=f" Comment not found")
    return {"success":True,"data":comment}


@router.get('/comments/topic/{topic_id}',status_code=status.HTTP_200_OK)
def fetch_comment_by_topic( topic_id:str, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    """ Fetch comments by a topic"""

    return crud.get_comment_in_topic(db,topic_id=topic_id)    


@router.get('/comments/user/{user_id}',status_code=status.HTTP_200_OK)
def get_comment_user( user_id:str, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    """ Fetch comments by a User"""
    
    return crud.get_comment_user(db,user_id=user_id)    


@router.delete('/delete/comment/{comment_id}',status_code=status.HTTP_200_OK)
def delete_comment(comment_id:str,db :Session = Depends(get_db),current_user : str = Depends(get_current_user)):
    """ Delete a comment """

    return crud.delete_comment(db,comment_id=comment_id,current_user=current_user)