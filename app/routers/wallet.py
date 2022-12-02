from fastapi import APIRouter, Depends, HTTPException, status

from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from uuid import uuid4, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from sqlalchemy import Column, String, Integer
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import get_db
from schema import TransactionRequest
from model import Wallet
import schema

router = APIRouter(
    prefix='/user',
    tags=['wallet']
)

app = FastAPI()
Base = declarative_base()



def create_wallet( user_id: int,  db: Session = Depends(get_db)):
	walletobj= db.query(Wallet).filter(Wallet.user_id==user_id).first()
	if not walletobj:
		itemobj = Wallet(user_id=user_id)
		db.add(itemobj)
		db.commit()
		db.refresh(itemobj)
		return itemobj
	else:
		return walletobj

@router.put('/wallet/earn')
def add_to_wallet(request: schema.TransactionRequest, db: Session = Depends(get_db)):
	id = request.wallet_address
	user_account = db.query(Wallet).filter(Wallet.id == id).first()
	if not user_account:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
		detail=f'account with the id {id} not available.')
	amount = request.amount

	user_account.balance += amount
	user_account.deposits_made += 1
	db.add(user_account)
	db.commit()
	db.refresh(user_account)
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
		
	amount = request.amount
	if user_account.balance >= amount:

		user_account.balance -= amount
		user_account.spendings += 1
		db.add(user_account)
		db.commit()
		db.refresh(user_account)
		return {"code": "success", 
		"message": "Deposit was successfully added", 
		"balance": user_account.balance}
	else:
		return {"code": "error", "message": "Wallet Balance Insufficience"}



# {
#   "Success": true,
#   "Message": "user added successfully",
#   "data": {
#     "user_id": 7,
#     "userName": "strong",
#     "email": "strong@example.com",
#     "wallet": {
#       "user_id": 7,
#       "balance": 1000,
#       "deposits_made": 0,
#       "spendings": 0,
#       "id": "e6bd3c1c-8f06-4b3d-b2db-2be00707e972",
#       "created_at": "2022-12-02T01:11:47.129076"
#     }
#   },
#   "Token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3LCJleHAiOjE2Njk5NDQ0MDh9.9_IL2vXmGzLhF_SAwyacS03OOLctNJVZ6vOKvckdgk0"
# }