from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List
from app import answer_crud, schema

router = APIRouter(
    prefix='/answer',
    tags=['Answer']
)


@router.get("/answer/{question_id}", response_model=List[schema.ListAnswerBase])
def list_answer(question_id: int, db: Session = Depends(get_db)):
    """ List answers endpoint for a specific question """

    answers = answer_crud.list_answer(db, question_id=question_id)
    return answers


@router.post("/answer", response_model=schema.ListAnswerBase)
def create_answer(answer: schema.CreateAnswer, db: Session = Depends(get_db)):
    """ Add answer endpoint for a specific question """

    return answer_crud.create_answer(db=db, answer=answer)


@router.put("/answer/{answer_id}", response_model=schema.ListAnswerBase)
def update_answer(answer_id: int, answer: schema.UpdateAnswer, db: Session = Depends(get_db)):
    """ Update answer endpoint for a specific question """

    db_answer = answer_crud.get_answer(db=db, answer_id=answer_id)
    if db_answer is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return answer_crud.update_answer(db=db, answer_id=answer_id, answer=answer)


@router.delete("/answer/{answer_id}")
def delete_answer(answer_id: int, db: Session = Depends(get_db)):
    """ Delete answer endpoint for a specific question """

    db_answer = answer_crud.get_answer(db=db, answer_id=answer_id)
    if db_answer is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return answer_crud.delete_answer(db=db, answer_id=answer_id)
