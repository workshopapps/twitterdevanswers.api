from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from uuid import uuid4, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from sqlalchemy import Column, String, Integer
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import get_db
from schema import TransactionRequest, WalletItem
from model import Wallet
import schema

router = APIRouter(
    prefix='/user',
    tags=['wallet']
)

app = FastAPI()
Base = declarative_base()



@router.post('/create', status_code=status.HTTP_201_CREATED)
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

