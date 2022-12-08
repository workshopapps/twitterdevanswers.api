import schema, crud
from sqlalchemy import desc
from model import *
from typing import List
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, APIRouter, status, Request, Path
from oauth import get_current_user
import model, schema, oauth
from schema import AdminPayments
from database import engine, get_db

router = APIRouter(
    prefix='/admin',
    tags=['Admin']
)



def get_question(question_id: int, amount: int, db: Session = Depends(get_db)):
	"""
		gets question with given question id and amount
		params:
			question_id
			amount
		Return: Question obj
	"""

	question_obj = db.query(model.Question).filter(
        model.Question.question_id == question_id).first()
	
	question_obj.payment_amount = amount
	db.add(question_obj)
	db.commit()
	db.refresh(question_obj)
	
	return question_obj

def admin_deduction(question_owner_balance: int, amount:int, admin_id: int, db: Session = Depends(get_db)):
	
	"""
		deducts question allocated payment amount from question owner account
		params:
			question_owner_balance
			amount
			admin_id
		Return: admin obj
	"""
	if question_owner_balance >= amount:
		
		admin_obj = db.query(model.User).filter(admin_id == model.User.user_id).first()

		if not admin_obj.is_admin:
			
			raise  HTTPException(status_code=401, detail="Authorization needed")
		question_owner_balance -= amount
		admin_obj.account_balance += amount
		db.add(admin_obj)
		db.commit()
		db.refresh(admin_obj)
		return admin_obj
	else:
		return {"code": "error", "balance": question_owner_account.balance,
			"message": "Wallet Balance Insufficience"}



@router.post('/payments')
def admin_transactions(item: AdminPayments,  db: Session = Depends(get_db)):

	question_id=item.question_id
	amount= item.amount
	admin_id = item.admin_id
	commission = item.commission

	admin_obj = db.query(model.User).filter(admin_id == model.User.user_id).first()
	if not admin_obj.is_admin:
			raise  HTTPException(status_code=401, detail="Authorization needed")

	try:
		question_obj = get_question(question_id, amount, db)
	except:
			raise HTTPException(status_code=404, detail="question not found")

	# verfying account owner account balance
	question_owner_id = question_obj.owner_id
	question_owner_account = db.query(Wallet).filter(Wallet.user_id == question_owner_id).first()
	try:
		admin_obj = admin_deduction(question_owner_account.balance, amount, admin_id, db)
	except:
		raise  HTTPException(status_code=401, detail="Authorization needed")

	if admin_obj.account_balance: 
		# checks if answer exists
		answer_exists = db.query(model.Answer).filter(model.Answer.question_id == question_id).order_by(
			desc(model.Answer.vote)).first()
	
		if not answer_exists:
			raise HTTPException(status_code=404, detail=f"No answer available for question {question_obj}")

		# Admins remits earnings
		answer_owner_id = answer_exists.owner_id
		earned_value = amount - commission		
		answerer_account = db.query(Wallet).filter(Wallet.user_id == answer_owner_id).first()
		
		admin_obj.account_balance  -= earned_value
		answerer_account.balance += earned_value
		admin_balance = admin_obj.account_balance

		db.add(answerer_account)
		db.add(admin_obj)
		db.commit()
		db.refresh(answerer_account)

		return {"code": "success",
				"message": "extra tokens has been added for maximum voted answer",
				"earned": earned_value,
				"wallet": answerer_account}

		




