from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.exceptions import HTTPException
import schema, model, oauth
from sqlalchemy.orm import Session
from database import get_db
from database import get_db
from routers.answer import get_question
from routers.notification import create_notification


router = APIRouter(
    prefix="/like",
    tags=["Like"]
)


@router.get("/{question_id}")
def list_like(question_id: int, db: Session = Depends(get_db)):
    """ List all likes for a specific question """

    return db.query(model.Like).filter(model.Like.question_id == question_id).all()


@router.post("/")
def create_like(like_base: schema.Like, background_task: BackgroundTasks, db: Session = Depends(get_db),
                current_user: int = Depends(oauth.get_current_user)):
    """ Add Like endpoint for a specific question """

    # get question
    db_question = get_question(db=db, question_id=like_base.question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Invalid Question ID")

    # get like
    check_if_like_exist = db.query(model.Like).filter(
        model.Like.question_id == like_base.question_id, model.Like.user_id == current_user.user_id
    ).first()

    # check_if_like_exist
    if check_if_like_exist is not None:

        if check_if_like_exist.like_type == "up" and check_if_like_exist.like_type == "up":
            pass

        elif check_if_like_exist.like_type != "up" and like_base.like_type == "up":
            question_db = db.query(model.Question).filter(model.Question.question_id == like_base.question_id).first()
            question_db.total_like = question_db.total_like + 1
            question_db.total_unlike = question_db.total_unlike - 1
            db.commit()
            db.refresh(question_db)

        elif check_if_like_exist.like_type == "up" and like_base.like_type != "up":
            question_db = db.query(model.Question).filter(model.Question.question_id == like_base.question_id).first()
            question_db.total_unlike = question_db.total_unlike + 1
            question_db.total_like = question_db.total_like - 1
            db.commit()
            db.refresh(question_db)
        else:
            pass

        return {"detail": "Success"}
    else:

        db_like = model.Like(
            user_id=current_user.user_id,
            like_type=like_base.like_type,
            question_id=like_base.question_id
        )

        # add like
        question_db = db.query(model.Question).filter(model.Question.question_id == like_base.question_id).first()
        if like_base.like_type == "up":
            question_db.total_like = question_db.total_like + 1
        else:
            question_db.total_unlike = question_db.total_unlike + 1

        db.add(db_like)
        db.commit()
        db.refresh(db_like)
        db.refresh(question_db)

        # This automatically creates a notification by calling create_notification as a background function which
        # runs after returning a response
        notification = schema.NotificationCreate(
            owner_id=db_question.owner_id,
            content_id=db_like.like_id,
            type="Like",
            title=f"@{current_user.username} like your question.",
        )
        background_task.add_task(create_notification, notification=notification, db=db)

        return db_like

# @router.post("/", status_code=status.HTTP_201_CREATED)
# def like(like: schema.Like, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
#     question = db.query(model.Question).filter(
#         model.Question.question_id == like.question_id).first()
#     if not question:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Question with id: {like.question_id} does not exist.")
#
#     like_query = db.query(model.Like).filter(
#         model.Like.question_id == like.question_id,
#         model.Like.user_id == current_user.user_id
#     )
#     found_like = like_query.first()
#     if (like.dir == 1):
#         if found_like:
#             raise HTTPException(status_code=status.HTTP_409_CONFLICT,
#                                 detail=f"user {current_user.user_id} has already voted on post {like.question_id}")
#
#         new_like = model.Like(question_id=like.question_id,
#                               user_id=current_user.user_id)
#         db.add(new_like)
#         db.commit()
#
#         return {"message": "successfully added Like to Question"}
#     else:
#         if not found_like:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND, detail="like does not exist")
#
#         like_query.delete(synchronize_session=False)
#         db.commit()
#
#         return {"message": "successfully removed like"}
