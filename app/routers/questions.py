from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import model, schema, oauth
from database import engine, get_db


router = APIRouter(
    prefix='/questions',
    tags=['Questions']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_question(request: schema.Question, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    # request.owner_id = current_user.user_id
    ask_question = model.Question(
        content=request.content, owner_id=current_user.user_id,
        expected_result=request.expected_result, payment_amount=request.payment_amount,
        title=request.title,
        tag=request.tag
    )
    db.add(ask_question)
    db.commit()
    db.refresh(ask_question)
    return {"success": True, "message": ask_question.content}


@router.get("/update_questions/{question_id}", status_code=status.HTTP_200_OK)
def retrieve_question(question_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    retrieve = db.query(model.Question).filter(
        model.Question.question_id == question_id).first()
    if retrieve:
        return retrieve
    return {"success": True, "message": "detail not found"}


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(question_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    delete_question = db.query(model.Question).filter(
        model.Question.question_id == question_id).first()
    if delete_question:
        if delete_question.owner_id == current_user.user_id:
            db.delete(delete_question)
            db.commit()
            return {"success": True, "message": delete_question.question_id}
        else:
            return {"success": False, "message": "Not authorized"}


@router.get("/{question_id}", status_code=status.HTTP_200_OK)
def get_question(question_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    get_question_db = db.query(model.Question).filter(
        model.Question.question_id == question_id).first()
    if get_question_db:
        db.commit()
        return {"success": True, "data": {
                "questionid": get_question_db.question_id,
                "title": get_question_db.title,
                "content": get_question_db.content,
                "expected_result": get_question_db.expected_result,
                "payment_amount": get_question_db.payment_amount,
                "answered": True,
                "createdAt": get_question_db.created_at,
                "updatedAT": get_question_db.updated_at,
                "owner": get_question_db.owner_id,
                "answers": [],
                }
                }
    return {"success": True, "message": "user have not asked any questions"}


@router.patch("/{question_id}", status_code=status.HTTP_200_OK)
def update_question(question_id, request: schema.QuestionUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    update_question = db.query(model.Question).filter(
        model.Question.question_id == question_id).first()
    if update_question:
        if update_question.owner_id != current_user.user_id:
            return HTTPException(status_code=404, detail="Not authorized")
        update_question.title = request.title
        update_question.content = request.content
        update_question.expected_result = request.expected_result
        update_question.updated_at = request.updated_at
        db.commit()
        return {"success": True, "message": {update_question.title,
                                             update_question.content,
                                             update_question.expected_result,
                                             update_question.updated_at}}


@router.get("/", status_code=status.HTTP_200_OK)
def get_all_questions(db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    get_all_questions_db = db.query(model.Question).all()
    return {"success": True, "data": get_all_questions_db}


# get all questions by a user
@router.get("/{user_id}/user/", status_code=status.HTTP_200_OK)
def get_all_questions_by_a_user(user_id: int, db: Session = Depends(get_db)):
    get_all_user_question = db.query(model.Question).filter(
        model.Question.owner_id == user_id).all()
    if not get_all_user_question:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True, "data": get_all_user_question}


# gets a particular question from a user using the question id
@router.get("/{user_id}/user/{question_id}", status_code=status.HTTP_200_OK)
def get_a_particular_user_question_by_a_question_id(user_id: int, question_id: int, db: Session = Depends(get_db)):
    get_a_particular_user_question = db.query(model.Question).filter(
        model.Question.owner_id == user_id, model.Question.question_id == question_id).first()
    if not get_a_particular_user_question:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True, "data": get_a_particular_user_question}
