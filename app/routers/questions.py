from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app import model, crud, schema, oauth
from app.database import engine, get_db
from uuid import uuid4


router = APIRouter(
    prefix='/questions',
    tags=['Questions']
)


@router.get("/update_questions/{question_id}", status_code=status.HTTP_200_OK)
def retrieve_question(question_id: str, db: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
    retrieve = db.query(model.Question).filter(
        model.Question.question_id == question_id).first()
    if retrieve:
        return retrieve
    return {"success": True, "message": "detail not found"}


@router.get("/{question_id}", status_code=status.HTTP_200_OK)
def get_question(question_id: str, db: Session = Depends(get_db)):
    get_all_questions_db = db.query(model.Question).all()
    get_question_db = db.query(model.Question).filter(
        model.Question.question_id == question_id).first()
    get_answer_db = db.query(model.Answer).filter(model.Answer.question_id == question_id).first()
    get_likes_db = db.query(model.Like).filter(model.Like.item_id == question_id).first()

    if get_question_db:
        if not get_answer_db and not get_likes_db:
            return {"success": True, "message": "Questions doesn't have answers or likes yet","data":crud.get_a_question(question_id, db) } 
        if not get_answer_db :
            return {"success": True, "message": "Questions doesn't have answers yet","data":crud.get_questions_and_likes(question_id, db)} 
        if not get_likes_db :
            return {"success": True, "message": "Questions doesn't have likes yet","data":crud.get_questions_and_answers(question_id, db)} 
        return {"success": True, "data":crud.get_all(question_id, db) }          
    return {"success": True, "message": "user have not asked any questions"}


#  get all questions 
@router.get("/", status_code=status.HTTP_200_OK)
def get_all_questions(db: Session = Depends(get_db)):
    get_all_questions_db = db.query(model.Question).all()
    
    return {"success": True, "data": get_all_questions_db}


# get all questions and their respective answers and likes
@router.get("/allquestions/",status_code=status.HTTP_200_OK)
def get_all_questions_and_answers(db: Session = Depends(get_db)):
    """Get all questions and their respective answers and likes"""
    get_all_questions_db = db.query(model.Question).all()
    questions_list = []
    for question in get_all_questions_db:
        q_dict = {}
        answers = db.query(model.Answer).filter(model.Answer.question_id == question.question_id).all()
        likes = db.query(model.Like).filter(model.Like.item_id == question.question_id).all()
        q_dict["question"] = question
        q_dict["answers"] = answers
        q_dict["likes"] = likes
        questions_list.append(q_dict)
    return {"success": True, "data":questions_list}


# get all questions by a user
@router.get("/{user_id}/user/", status_code=status.HTTP_200_OK)
def get_all_questions_by_a_user(user_id: str, db: Session = Depends(get_db)):
    get_all_user_question = db.query(model.Question).filter(
        model.Question.owner_id == user_id).all()
    if not get_all_user_question:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True, "data": get_all_user_question}


# gets a particular question from a user using the question id
@router.get("/{user_id}/user/{question_id}", status_code=status.HTTP_200_OK)
def get_a_particular_user_question_by_a_question_id(user_id: str, question_id: str, db: Session = Depends(get_db)):
    get_a_particular_user_question = db.query(model.Question).filter(
        model.Question.owner_id == user_id, model.Question.question_id == question_id).first()
    if not get_a_particular_user_question:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True, "data": get_a_particular_user_question}


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_question(request: schema.Question, db: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
    # request.owner_id = current_user.user_id
    ask_question = model.Question(
        question_id = uuid4(),
        content=request.content, owner_id=current_user.user_id,
        expected_result=request.expected_result, payment_amount=request.payment_amount,
        title=request.title,
        tag=request.tag
        # created_at=request.created_at,
        # updated_at=request.updated_at
    )
    db.add(ask_question)
    db.commit()
    db.refresh(ask_question)
    return {"success": True, "message": ask_question.content, "id": ask_question.question_id}


# selects the correct answer
@router.patch("/select_answer/{answer_id}", status_code=status.HTTP_200_OK)
def select_answer(answer_id: str, question_id: str, db: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
    get_answer = db.query(model.Answer).filter(
        model.Answer.question_id == question_id, model.Answer.answer_id == answer_id).first()
    if get_answer:
        if get_answer.owner_id == current_user.user_id:
            get_answer.is_answered = True
            db.commit()
            if get_answer.is_answered == True:
                get_question = db.query(model.Question).filter(
                    model.Question.question_id == question_id).first()
                get_question.answered = True
                db.commit()
                return {"success": True, "message": "correct answer selected", "info": "question has been answered correctly"}


@router.patch("/{question_id}", status_code=status.HTTP_200_OK)
def update_question(question_id, request: schema.QuestionUpdate, db: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
    update_question = db.query(model.Question).filter(
        model.Question.question_id == question_id).first()
    if update_question:
        if update_question.owner_id != current_user.user_id:
            return HTTPException(status_code=404, detail="Not authorized")
        update_question.title = request.title
        update_question.content = request.content
        update_question.expected_result = request.expected_result
        # update_question.updated_at = request.updated_at
        db.commit()
        return {"success": True, "message": {
        "title":update_question.title,
        "content":update_question.content,
        "expected_result":update_question.expected_result}}


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(question_id: str, db: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
    delete_question = db.query(model.Question).filter(
        model.Question.question_id == question_id).first()

    if delete_question:
        if delete_question.owner_id == current_user.user_id or current_user.is_admin:
            db.delete(delete_question)
            db.commit()
            return {"success": True, "message": delete_question.question_id}
        else:
            return {"success": False, "message": "Not authorized"}
