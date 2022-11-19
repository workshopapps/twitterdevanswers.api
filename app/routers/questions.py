from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from .. import model
from app.database import engine
from .. import schema
from app.database import get_db

router = APIRouter(
    prefix='',
    tags=['Question']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_question(request: schema.Question, db: Session = Depends(get_db)):
    ask_question = model.Question(content=request.content,
                                  body=request.answered, user_id=request.user_id)
    db.add(ask_question)
    db.commit()
    db.refresh(ask_question)
    return {"success": True, "message": ask_question.content}


@router.patch("/question/{question_id}", status_code=status.HTTP_200_OK)
def answer_question(question_id, request: schema.Question, db: Session = Depends(get_db)):
    update_answer = db.query(model.Question).filter(
        model.Question.id == question_id).first
    if update_answer:
        update_answer.answered = request.answered
        update_answer.user_id = request.user_id
        update_answer.answer_id = request.answer_id
        db.commit()
        db.close()
        return {"success": True, "message": update_answer.content}


@router.delete("/questionid/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(question_id, db: Session = Depends(get_db)):
    delete_question = db.query(model.Question).filter(
        model.Question.id == question_id).first
    if delete_question:
        db.delete(delete_question)
        db.commit()
        return {"success": True, "message": delete_question.question_id}


@router.get("/question/{question_id}", status_code=status.HTTP_200_OK)
def get_question(question_id, db: Session = Depends(get_db)):
    get_question = db.query(model.Question).filter(
        model.Question.id == question_id).first
    if get_question:
        db.commit()
        return {"success": True, "data": {
            "questionid": get_question.question_id,
            "content": get_question.content,
            "answered": True,
            "createdAt": get_question.created_at,
            "updatedAT": get_question.updated_at,
            "answers": [],
        }
        }


@router.patch("/question/{question_id}", status_code=status.HTTP_200_OK)
def update_question(question_id, request: schema.Question, db: Session = Depends(get_db)):
    update_question = db.query(model.Question).filter(
        model.Question.id == question_id).first
    if update_question:
        update_question.content = request.content
        update_question.answer = request.answer
        db.commit()
        return {"success": True, "message": update_question.content}


@router.get("/", status_code=status.HTTP_200_OK)
def get_all_questions(db: Session = Depends(get_db)):
    get_all_questions = db.query(model.Question).all()
    return {"success": True, "data": [
            {
                "questionid": get_all_questions.question_id,
                "content": get_all_questions.content,
                "answered": True,
                "createdAt": get_all_questions.created_at,
                "updatedAt": get_all_questions.updated_at,
                "answers": []
            }
            ]
            }
