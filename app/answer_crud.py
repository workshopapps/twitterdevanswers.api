from sqlalchemy.orm import Session
from . import model, schema


def get_answer(db: Session, answer_id: int):
    """ Get single answer  """

    return db.query(model.Answer).filter(model.Answer.id == answer_id).first()


def list_answer(db: Session, question_id: int):
    """ List answers for list answer endpoint """

    return db.query(model.Answer).filter(model.Question.id == question_id).all()


def create_answer(db: Session, answer: schema.CreateAnswer):
    """ Create answer for create answer endpoint """

    db_answer = model.Answer(
        owner_id=answer.owner_id,
        content=answer.content,
        question_id=answer.question_id
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


def update_answer(db: Session, answer_id: int, answer: schema.UpdateAnswer):
    """ Update answer for update answer endpoint """

    db_answer = db.query(model.Answer).get(model.Answer.id == answer_id).update(
        content=answer.content
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


def delete_answer(db: Session, answer_id: int):
    """ Delete answer for delete answer endpoint """

    db_answer = db.query(model.Answer).filter(model.Answer.id == answer_id).first()
    db.delete(db_answer)
    db.commit()
    db.refresh(db_answer)
    return {"detail": "success"}
