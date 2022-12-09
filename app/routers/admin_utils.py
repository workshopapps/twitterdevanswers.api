from app import schema, crud
from sqlalchemy import desc
from app.model import *
from typing import List
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, APIRouter, status, Request, Path
from app.oauth import get_current_user
from app import model, schema, oauth
from app.schema import AdminPayments
from app.database import engine, get_db

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

def admin_deduction(question_owner_id: int, amount:int, admin_id: int, db: Session = Depends(get_db)):
	
	"""
		deducts question allocated payment amount from question owner account
		params:
			question_owner_balance
			amount
			admin_id
		Return: admin obj
	"""
	question_owner_account = db.query(Wallet).filter(Wallet.user_id == question_owner_id).first()


	if question_owner_account.balance >= amount:
		
		admin_obj = db.query(model.User).filter(admin_id == model.User.user_id).first()

		if not admin_obj.is_admin:
			
			raise  HTTPException(status_code=401, detail="Authorization needed")
		
		question_owner_account.balance -= amount
		question_owner_account.spendings += 1
		question_owner_account.total_spent += amount
		db.add(question_owner_account)
		db.commit()

		admin_account = db.query(Wallet).filter(Wallet.user_id == admin_id).first()
		admin_account.balance += amount
		admin_account.earnings += 1
		admin_account.total_earned += amount
		db.add(admin_account)
		db.add(question_owner_account)
		db.commit()
		db.refresh(admin_account)
		db.refresh(question_owner_account)

		return {"admin_obj": admin_account, 
		"question_owner": question_owner_account}
	else:
		return {"code": "error", "balance": question_owner_account.balance,
			"message": "Wallet Balance Insufficience"}



@router.post('/transactions')
def admin_transactions(item: AdminPayments,  db: Session = Depends(get_db)):

	question_id=item.question_id
	amount= item.amount
	admin_id = item.admin_id
	commission = item.commission


	try:
		question_obj = get_question(question_id, amount, db)
	except:
			raise HTTPException(status_code=404, detail="question not found")
	question_owner_id = question_obj.owner_id
	
	admin_obj = db.query(model.User).filter(admin_id == model.User.user_id).first()

	if not admin_obj.is_admin:
			raise  HTTPException(status_code=401, detail="Authorization needed")
	
	try:
		res_obj = admin_deduction(question_owner_id, amount, admin_id, db)

	except:
		raise  HTTPException(status_code=401, detail=f"Payment Failed for user {question_owner_id}")
	
	admin_obj = res_obj['admin_obj']
	question_owner = res_obj['question_owner']

	return  question_owner
	
	answer_exists = db.query(model.Answer).filter(model.Answer.question_id == question_id).order_by(
		desc(model.Answer.vote)).first()

	# Check if answer exists
	if not answer_exists:
		raise HTTPException(status_code=404, detail=f"No answer available for question {question_obj.content}")

	if admin_obj.balance >= amount:

		# Admins remits earnings and subtracts commision
		answer_owner_id = answer_exists.owner_id
		earned_value = amount - commission		
		answerer_account = db.query(Wallet).filter(Wallet.user_id == answer_owner_id).first()
		
		admin_obj.balance  -= earned_value
		admin_obj.spendings += 1
		admin_obj.total_spent += earned_value


		answerer_account.balance += earned_value
		answerer_account.earnings += 1
		answerer_account.total_earned += earned_value

		db.add(answerer_account)
		db.add(admin_obj)
		db.commit()
		db.refresh(answerer_account)
		db.refresh(question_owner_account)

		return {"code": "success",
				"message": "extra tokens has been added for maximum voted answer",
				"earned": earned_value,
				"Answer Owner Transaction History": answerer_account,
				"Question Owner History": question_owner_account
				}
