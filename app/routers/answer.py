from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.database import get_db
from app import model, schema, oauth

router = APIRouter(
    prefix='/answer',
    tags=['Answer']
)


def get_question(question_id: int, db: Session):
    """ Get single answer  """

    return db.query(model.Question).filter(model.Question.question_id == question_id).first()


def get_answer(answer_id: int, db: Session):
    """ Get single answer  """

    return db.query(model.Answer).filter(model.Answer.answer_id == answer_id).first()


@router.get("/{question_id}")
def list_answer(question_id: int, db: Session = Depends(get_db)):
    """ List answers endpoint for a specific question """

    db_question = get_question(db=db, question_id=question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Invalid Question ID")
    return db.query(model.Answer).filter(model.Answer.question_id == question_id).order_by(
        desc(model.Answer.vote)).all()
    # return db.query(model.Answer).filter(model.Answer.question_id == question_id).all()


@router.post("/")
def create_answer(answer: schema.CreateAnswer, db: Session = Depends(get_db),
                  current_user: int = Depends(oauth.get_current_user)):
    """ Add answer endpoint for a specific question """

    db_question = get_question(db=db, question_id=answer.question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Invalid Question ID")
    db_answer = model.Answer(
        owner_id=current_user.user_id,
        content=answer.content,
        question_id=answer.question_id
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


@router.patch("/{answer_id}")
def update_answer(answer_id: int, answer: schema.UpdateAnswer, db: Session = Depends(get_db),
                  current_user: int = Depends(oauth.get_current_user)):
    """ Update answer endpoint for a specific question """

    db_answer = db.query(model.Answer).filter(model.Answer.answer_id == answer_id).first()
    if db_answer is None or db_answer.owner_id != current_user.user_id:
        raise HTTPException(status_code=404, detail="Not Found")
    db_answer.content = answer.content
    db.commit()
    db.refresh(db_answer)
    return db_answer


@router.delete("/{answer_id}")
def delete_answer(answer_id: int, db: Session = Depends(get_db),
                  current_user: int = Depends(oauth.get_current_user)):
    """ Delete answer endpoint for a specific question """

    db_answer = get_answer(db=db, answer_id=answer_id)
    if db_answer is None or db_answer.owner_id != current_user.user_id:
        raise HTTPException(status_code=404, detail="Not Found")
    del_answer = db.query(model.Answer).filter(model.Answer.answer_id == answer_id).first()
    db.delete(del_answer)
    db.commit()
    return {"detail": "success"}


@router.post("/vote")
def vote_answer(answer: schema.AnswerVote, db: Session = Depends(get_db),
                current_user: int = Depends(oauth.get_current_user)):
    """ Vote endpoint for a specific answer """

    # checks if answer_id exists
    db_answer = get_answer(db=db, answer_id=answer.answer_id)
    if db_answer is None:
        raise HTTPException(status_code=404, detail="Not Found")

    # check if user voted before
    check_user_vote = db.query(model.AnswerVote).filter(model.AnswerVote.answer_id == answer.answer_id).first()

    if check_user_vote.owner_id == current_user.user_id:
        # update vote
        get_answer_detail = get_answer(db=db, answer_id=answer.answer_id)

        # prevent user from voting up again
        if check_user_vote.vote_type == "add" and answer.vote_type == "add":
            raise HTTPException(status_code=400, detail="Already voted!")

        # add vote if previous vote is not add
        elif check_user_vote.vote_type != "add" and answer.vote_type == "add":
            db_vote_answer = db.query(model.Answer).get(model.Answer.answer_id == answer.answer_id).update(
                vote=get_answer_detail.vote + 1
            )
            check_user_vote.vote_type = answer.vote_type
            db.commit()
            db.refresh(db_vote_answer)
            db.refresh(check_user_vote)

        # remove vote if previous vote is add
        elif check_user_vote.vote_type == "add" and answer.vote_type != "add":
            db_vote_answer = db.query(model.Answer).get(model.Answer.answer_id == answer.answer_id).update(
                vote=get_answer_detail.vote - 1
            )
            check_user_vote.vote_type = answer.vote_type
            db.commit()
            db.refresh(db_vote_answer)
            db.refresh(check_user_vote)
        else:
            pass
        return {"detail": "Success"}
    else:
        # add vote
        db_answer_vote = model.AnswerVote(
            owner_id=current_user.user_id,
            answer_id=answer.answer_id,
            vote_type=answer.vote_type
        )

        # update vote point
        get_answer_detail = get_answer(db=db, answer_id=answer.answer_id)
        db_vote_answer = db.query(model.Answer).get(model.Answer.answer_id == answer.answer_id).update(
            vote=get_answer_detail.vote + 1 if answer.vote_type == "add" else get_answer_detail.vote - 1
        )

        db.add(db_answer_vote)
        db.add(db_vote_answer)
        db.commit()
        db.refresh(db_answer_vote)
        db.refresh(db_vote_answer)

    return {"detail": "Success"}
