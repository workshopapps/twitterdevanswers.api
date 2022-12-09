from fastapi import APIRouter, Depends, HTTPException, status

from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from uuid import uuid4, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from sqlalchemy import Column, String, Integer
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.database import get_db

from app.schema import TransactionRequest

from app.model import Wallet
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


@router.put('/wallet/earn')
def add_to_wallet(request: schema.TransactionRequest, db: Session = Depends(get_db)):
    id = request.user_id
    user_account = db.query(Wallet).filter(Wallet.user_id == id).first()

    if not user_account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'account with the id {id} not available.')
    
    user_obj = db.query(User).filter(User.user_id == user_account.user_id).first()
    amount = request.amount
    user_account.balance += amount
    user_account.deposits_made += 1
    user_obj.account_balance = user_account.balance

    db.add(user_account)
    db.add(user_obj)
    db.commit()
    db.refresh(user_account)
    db.refresh(user_obj)
    return {"code": "success",
            "message": "Deposit was successfully added",
            "balance": user_account.balance}


@router.put('/wallet/spend')
def remove_from_wallet(request: schema.TransactionRequest, db: Session = Depends(get_db)):

    id = request.user_id
    user_account = db.query(Wallet).filter(Wallet.user_id == id).first()

    if not user_account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'account with the id {id} not available.')

    user_obj = db.query(User).filter(User.user_id == user_account.user_id).first()
    amount = request.amount
    if user_account.balance >= amount:
        user_account.balance -= amount
        user_account.spendings += 1
        user_obj.account_balance = user_account.balance
        db.add(user_account)
        db.add(user_obj)
        db.commit()
        db.refresh(user_account)
        db.refresh(user_obj)

        return {"code": "success",
                "message": "Payment successful",
                "balance": user_account.balance}
    else:
        return {"code": "error", "message": "Wallet Balance Insufficience"}

