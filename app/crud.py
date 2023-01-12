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
        "work_experience": user.work_experience,
        "position": user.position,
        "stack": user.stack,
        "links": [user.links],
        "role": user.role,
        "image_url": user.image_url,
        "location": user.location,
        "is_admin": user.is_admin,
        "account_balance": user.account_balance,
        "followers": user.followers,
        "following": user.following,
        "date_joined": user.created_at
    }


def get_user_id(db: Session, user_id: int):
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
        "work_experience": user.work_experience,
        "position": user.position,
        "stack": user.stack,
        "links": [user.links],
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
            "work_experience": user.work_experience,
            "position": user.position,
            "stack": user.stack,
            "links": [user.links],
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


def delete_user(db: Session, username: str, current_user: int):
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

def get_a_question(question_id:int,db:Session):
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

def get_questions_and_answers(question_id:int,db:Session):
    get_question_db = db.query(model.Question).filter(
        model.Question.question_id == question_id).first()
    get_answer_db = db.query(model.Answer).filter(model.Answer.question_id == question_id).first()

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
                }
    return {"success": True, "message": "user have not asked any questions"}            