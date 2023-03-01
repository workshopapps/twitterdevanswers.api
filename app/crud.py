from sqlalchemy.orm import Session
from app import model, schema
from fastapi.exceptions import HTTPException

#  User Functions

def get_user(db: Session, username: str):
    """ Get a user from the database based on their Username  """

    user = db.query(model.User).filter(model.User.username == username).first()
    if user is None:
        return None
    return {
        "user_id": user.user_id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "date_of_birth": user.date_of_birth,
        "gender": user.gender,
        "description": user.description,
        "phone_number": user.phone_number,
        "organization":user.organization,
        "work_experience": user.work_experience,
        "position": user.position,
        "stack": user.stack,
        "links": user.links.split(','),
        "role": user.role,
        "image_url": user.image_url,
        "location": user.location,
        "is_admin": user.is_admin,
        "account_balance": user.account_balance,
        "followers": user.followers,
        "following": user.following,
        "date_joined": user.created_at
    }


def get_user_id(db: Session, user_id: str):
    """ Get a user from the database based on their id  """

    user = db.query(model.User).filter(model.User.user_id == user_id).first()
    if user is None:
        return None
    return {
        "user_id": user.user_id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "date_of_birth": user.date_of_birth,
        "gender": user.gender,
        "description": user.description,
        "phone_number": user.phone_number,
        "organization":user.organization,
        "work_experience": user.work_experience,
        "position": user.position,
        "stack": user.stack,
        "links": user.links.split(','),
        "role": user.role,
        "image_url": user.image_url,
        "location": user.location,
        "is_admin": user.is_admin,
        "account_balance": user.account_balance,
        "followers": user.followers,
        "following": user.following,
        "date_joined": user.created_at
    }


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """ Get all users in the database  """

    users = db.query(model.User).offset(skip).limit(limit).all()
    users_list = []
    for user in users:
        users_list.append({
            "user_id": user.user_id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "date_of_birth": user.date_of_birth,
            "gender": user.gender,
            "description": user.description,
            "phone_number": user.phone_number,
            "organization":user.organization,
            "work_experience": user.work_experience,
            "position": user.position,
            "stack": user.stack,
            "links": user.links.split(','),
            "role": user.role,
            "image_url": user.image_url,
            "location": user.location,
            "is_admin": user.is_admin,
            "account_balance": user.account_balance,
            "followers": user.followers,
            "following": user.following,
            "date_joined": user.created_at
        })
    return {"success": True, 'data': users_list}


def delete_user(db: Session, username: str, current_user: str):
    """ Delete a user Profile  """

    delete_user = db.query(model.User).filter(
        model.User.username == username).first()
    if delete_user:
        wallet = db.query(model.Wallet).filter(
            model.Wallet.user_id == delete_user.user_id).first()
        if delete_user.user_id == current_user.user_id or current_user.is_admin == True:
            db.delete(wallet)
            db.commit()
            db.delete(delete_user)
            db.commit()
            return {"success": True, "message": "profile removed"}
        else:
            return {"success": False, "message": "You're not authorized to perform this operation"}
    else:
        return {"success": False, "message": "User does not exist"}


# Question Functions

def get_a_question(question_id:str,db:Session):
    """ Get a Question from the database  """
    get_question_db = db.query(model.Question).filter(
        model.Question.question_id == question_id).first()
    if get_question_db:
        db.commit()
        return {
            "questionid": get_question_db.question_id,
            "title": get_question_db.title,
            "content": get_question_db.content,
            "expected_result": get_question_db.expected_result,
            "payment_amount": get_question_db.payment_amount,
            "answered": True,
            "createdAt": get_question_db.created_at,
            "updatedAT": get_question_db.updated_at,
            "owner": get_question_db.owner_id,
            "total_unlike":  get_question_db.total_unlike,
            "total_like":  get_question_db.total_like
            } 
    return {"success": True, "message": "user have not asked any questions"}

def get_all(question_id:str,db:Session):
    get_question_db = db.query(model.Question).filter(
        model.Question.question_id == question_id).first()
    get_answer_db = db.query(model.Answer).filter(model.Answer.question_id == question_id).first()
    get_likes_db = db.query(model.Like).filter(model.Like.question_id == question_id).first()

    if get_question_db:
        db.commit()
        return {
                "questionid": get_question_db.question_id,
                "title": get_question_db.title,
                "content": get_question_db.content,
                "expected_result": get_question_db.expected_result,
                "payment_amount": get_question_db.payment_amount,
                "answered": True,
                "createdAt": get_question_db.created_at,
                "updatedAT": get_question_db.updated_at,
                "owner": get_question_db.owner_id,
                "total_unlike":  get_question_db.total_unlike,
                "total_like":  get_question_db.total_like,
                "answers": [{
                    "answer_id":get_answer_db.answer_id,
                    "question_id":get_answer_db.question_id,
                    "owner":get_answer_db.owner_id,
                    "content":get_answer_db.content,
                    "is_answered" : get_answer_db.is_answered,
                    "vote": get_answer_db.vote,
                    "created_at": get_answer_db.created_at
                }],
                "likes" :[{
                    "like_id" :get_likes_db.like_id,
                    "like_type":get_likes_db.like_type,
                    "user_id":get_likes_db.user_id,
                    "question_id":get_likes_db.question_id
                }]
                }
    return {"success": True, "message": "user have not asked any questions"}            

def get_questions_and_answers(question_id:str,db:Session):
    get_question_db = db.query(model.Question).filter(
        model.Question.question_id == question_id).first()
    get_answer_db = db.query(model.Answer).filter(model.Answer.question_id == question_id).first()
    get_likes_db = db.query(model.Like).filter(model.Like.question_id == question_id).first()

    if get_question_db:
        db.commit()
        return {
                "questionid": get_question_db.question_id,
                "title": get_question_db.title,
                "content": get_question_db.content,
                "expected_result": get_question_db.expected_result,
                "payment_amount": get_question_db.payment_amount,
                "answered": True,
                "createdAt": get_question_db.created_at,
                "updatedAT": get_question_db.updated_at,
                "owner": get_question_db.owner_id,
                "total_unlike":  get_question_db.total_unlike,
                "total_like":  get_question_db.total_like,
                "answers": [{
                    "answer_id":get_answer_db.answer_id,
                    "question_id":get_answer_db.question_id,
                    "owner":get_answer_db.owner_id,
                    "content":get_answer_db.content,
                    "is_answered" : get_answer_db.is_answered,
                    "vote": get_answer_db.vote,
                    "created_at": get_answer_db.created_at
                }]
                }
    return {"success": True, "message": "user have not asked any questions"}            


def get_questions_and_likes(question_id:str,db:Session):
    get_question_db = db.query(model.Question).filter(
        model.Question.question_id == question_id).first()
    get_answer_db = db.query(model.Answer).filter(model.Answer.question_id == question_id).first()
    get_likes_db = db.query(model.Like).filter(model.Like.question_id == question_id).first()

    if get_question_db:
        db.commit()
        return {
                "questionid": get_question_db.question_id,
                "title": get_question_db.title,
                "content": get_question_db.content,
                "expected_result": get_question_db.expected_result,
                "payment_amount": get_question_db.payment_amount,
                "answered": True,
                "createdAt": get_question_db.created_at,
                "updatedAT": get_question_db.updated_at,
                "owner": get_question_db.owner_id,
                "total_unlike":  get_question_db.total_unlike,
                "total_like":  get_question_db.total_like,
                "likes" :[{
                    "like_id" :get_likes_db.like_id,
                    "like_type":get_likes_db.like_type,
                    "user_id":get_likes_db.user_id,
                    "question_id":get_likes_db.question_id
                }]
                }
    return {"success": True, "message": "user have not asked any questions"}            

#  Community Endponts


def get_communities(db: Session, skip: int = 0, limit: int = 100):
    """ Get all communities in the database  """

    communities = db.query(model.Community).offset(skip).limit(limit).all()
    return {"success": True, 'data': communities}


# def delete_community(db: Session, community_id: str, current_user: str):
#     """ Delete a user Profile  """

#     delete_community= db.query(model.Community).filter(
#         model.Community.community_id == community_id).first()
#     if delete_community:
#         topic = db.query(model.Topic).filter(
#             model.Topic.community_id == delete_community.community_id).all()
#         comment = db.query(model.Comment).filter(
#                        model.Topic.community_id == delete_community.community_id).all()

#         if delete_community.community_id == current_user.community_id or current_user.is_admin == True:
#             db.delete(topic)
#             db.delete(comment)
#             db.commit()
#             db.delete(delete_community)
#             db.commit()
#             return {"success": True, "message": "Community had been succesfully deleted"}
#         else:
#             return {"success": False, "message": "You're not authorized to perform this operation"}
#     else:
#         raise HTTPException(
            # status_code=404, detail=f" Community {community_id} not found")


#  TOPIC ENDPOINTS 

def get_topics(db: Session, skip: int = 0, limit: int = 100):
    """ Get all topics in the database  """

    topics = db.query(model.Topic).offset(skip).limit(limit).all()
    return {"success": True, 'data': topics}

def get_topic_in_community(db: Session, community_id: str):
    """ Get a user from the database based on their id  """
    
    topics = db.query(model.Topic).filter(model.Topic.community_id == community_id).all()
    if topics is None:
        return{"success":True,"message":"No topic under this Community"}
    return {"success":True, "data" : topics}


def get_topic_user(db: Session, user_id: str):
    """ Get all topics a user created from the database based on their id  """
    
    users = db.query(model.User).filter(model.User.user_id ==user_id).first()   
    topics = db.query(model.Topic).filter(model.Topic.user_id == user_id).all()
    if not users:
        return{"success":True,"message":"User doesn't exist"}   
    if not topics:
        return{"success":True,"message":"No topic created under this User"}        
    return {"success":True, "data" : topics}


#  COMMENT ENDPOINTS 
