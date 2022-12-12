from fastapi import APIRouter, Depends, HTTPException, status

from pydantic import BaseModel, Field
from fastapi import HTTPException
from uuid import uuid4, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from sqlalchemy import Column, String, Integer
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.database import get_db

from app.schema import TransactionRequest

from app.model import Wallet, User
from app import schema

router = APIRouter(
    prefix='/user',
    tags=['wallet']
)


@router.get("/wallet/view/{user_id}")
def view_wallet(user_id, db: Session = Depends(get_db)):

    user_account = db.query(Wallet).filter(Wallet.user_id == user_id).first()
    if not user_account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'account with the id {user_id} not available.')

    return user_account


