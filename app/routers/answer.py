from fastapi import Depends, HTTPException, APIRouter, BackgroundTasks
from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.database import get_db
from app import model, schema, oauth
from app.routers.notification import create_notification

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


def get_correct_answer(question_id: int, db: Session):
    """ Get correct answer  function """

    # check if question exists
    db_question = get_question(db=db, question_id=question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Invalid Question ID")

    # check correct answer
    check_answer = db.query(model.Answer).filter(
        model.Answer.question_id == question_id,
        model.Answer.is_answered == True
    ).first()

    return check_answer


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
def create_answer(answer: schema.CreateAnswer, background_task: BackgroundTasks, db: Session = Depends(get_db),
                  current_user: int = Depends(oauth.get_current_user)):
    """ Add answer endpoint for a specific question """

    db_question = get_question(db=db, question_id=answer.question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Invalid Question ID")

    check_if_answer_exist = db.query(model.Answer).filter(
        model.Answer.question_id == answer.question_id, model.Answer.owner_id == current_user.user_id
    ).first()

    if check_if_answer_exist is not None:
        raise HTTPException(status_code=400, detail="Already added answer")

    db_answer = model.Answer(
        owner_id=current_user.user_id,
        content=answer.content,
        question_id=answer.question_id
    )

    # update user account balance
    # try:
    #     db_user = db.query(model.User).filter(
    #         model.User.user_id == current_user.user_id).first()
    #     db_user.account_balance = db_user.account_balance + db_question.payment_amount
    # except Exception as e:
    #     db_user = db.query(model.User).filter(
    #         model.User.user_id == current_user.user_id).first()
    #     db_user.account_balance = db_user.account_balance + 0

    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    # db.refresh(db_user)

    # This automatically creates a notification by calling create_notification as a background function which
    # runs after returning a response
    notification = schema.NotificationCreate(
        owner_id=db_question.owner_id,
        content_id=db_answer.answer_id,
        type="Answer",
        title=f"@{current_user.username} provided an answer to your question.",
    )
    background_task.add_task(
        create_notification, notification=notification, db=db)

    return db_answer


@router.patch("/{answer_id}")
def update_answer(answer_id: int, answer: schema.UpdateAnswer, db: Session = Depends(get_db),
                  current_user: int = Depends(oauth.get_current_user)):
    """ Update answer endpoint for a specific question """

    db_answer = db.query(model.Answer).filter(
        model.Answer.answer_id == answer_id).first()
    if db_answer is None:
        raise HTTPException(status_code=404, detail="Invalid answer id")
    elif db_answer.owner_id != current_user.user_id:
        raise HTTPException(
            status_code=400, detail="Only owner can update this answer")
    db_answer.content = answer.content
    db.commit()
    db.refresh(db_answer)
    return db_answer


@router.patch("/correct")
def update_correct_answer(answer: schema.UpdateCorrectAnswer, db: Session = Depends(get_db),
                          current_user: int = Depends(oauth.get_current_user)):
    """ Add correct answer endpoint """

    db_answer = get_answer(db=db, answer_id=answer.answer_id)
    db_question = get_question(db=db, question_id=answer.question_id)

    if db_answer is None:
        raise HTTPException(status_code=404, detail="Invalid answer id")

    if db_question is None:
        raise HTTPException(status_code=404, detail="Invalid Question ID")

    if db_question.owner_id != current_user.user_id:
        raise HTTPException(
            status_code=400, detail="Not Authorized to perform this action")

    check_answer = db.query(model.Answer).filter(
        model.Answer.answer_id == answer.answer_id,
        model.Answer.is_answered == True
    ).first()

    if check_answer is None:
        check_question = db.query(model.Question).filter(model.Question.question_id == answer.question_id).first()
        check_question.answered = True
        check_answer.is_answered = True
        db.commit()
        db.refresh(check_answer)
        db.refresh(check_question)
        return check_answer
    else:
        raise HTTPException(
            status_code=400, detail="Already have correct answer")


@router.delete("/{answer_id}")
def delete_answer(answer_id: int, db: Session = Depends(get_db),
                  current_user: int = Depends(oauth.get_current_user)):
    """ Delete answer endpoint for a specific question """

    db_answer = get_answer(db=db, answer_id=answer_id)
    if db_answer is None:
        raise HTTPException(status_code=404, detail="Invalid answer id")
    elif db_answer.owner_id != current_user.user_id:
        raise HTTPException(
            status_code=400, detail="Only owner can delete this answer")
    del_answer = db.query(model.Answer).filter(
        model.Answer.answer_id == answer_id).first()
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
        raise HTTPException(status_code=404, detail="Answer Not Found")

    # check if user voted before
    check_user_vote = db.query(model.AnswerVote).filter(
        model.AnswerVote.answer_id == answer.answer_id).first()

    if check_user_vote is not None:
        if check_user_vote.owner_id == current_user.user_id:
            # update vote
            get_answer_detail = get_answer(db=db, answer_id=answer.answer_id)

            # prevent user from voting up again
            if check_user_vote.vote_type == "add" and answer.vote_type == "add":
                raise HTTPException(status_code=400, detail="Already voted!")

            # add vote if previous vote is not add
            elif check_user_vote.vote_type != "add" and answer.vote_type == "add":
                db_vote_answer = db.query(model.Answer).filter(
                    model.Answer.answer_id == answer.answer_id).first()
                db_vote_answer.vote = get_answer_detail.vote + 1
                check_user_vote.vote_type = answer.vote_type
                db.commit()
                db.refresh(db_vote_answer)
                db.refresh(check_user_vote)

            # remove vote if previous vote is add
            elif check_user_vote.vote_type == "add" and answer.vote_type != "add":
                db_vote_answer = db.query(model.Answer).filter(
                    model.Answer.answer_id == answer.answer_id).first()
                db_vote_answer.vote = get_answer_detail.vote - 1
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
        db_vote_answer = db.query(model.Answer).filter(
            model.Answer.answer_id == answer.answer_id).first()
        try:
            db_vote_answer.vote = get_answer_detail.vote + 1 if answer.vote_type == "add" \
                else get_answer_detail.vote - 1
        except Exception as e:
            db_vote_answer.vote = 1 if answer.vote_type == "add" \
                else - 1

        db.add(db_answer_vote)
        db.commit()
        db.refresh(db_answer_vote)
        db.refresh(db_vote_answer)

    return {"detail": "Success"}
