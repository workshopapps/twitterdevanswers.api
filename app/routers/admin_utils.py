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
from routers.answer import get_correct_answer

router = APIRouter(
    prefix='/admin',
    tags=['Admin']
)


def get_devask_wallet(db: Session = Depends(get_db)):

	devask_account = db.query(Wallet).filter(Wallet.is_devask_wallet == True).first()
	if not devask_account:
		wallet_id = uuid4()
		devask_wallet_obj = Wallet(is_devask_wallet=True, id=wallet_id)
		db.add(devask_wallet_obj)
		db.commit()
		db.refresh(devask_wallet_obj)
		return devask_wallet_obj
	
	return devask_account

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
	
	# sets payment amount
	question_obj.payment_amount = amount
	db.add(question_obj)
	db.commit()
	db.refresh(question_obj)
	
	return question_obj

def admin_deduction(question_owner_id: int, amount:int, db: Session = Depends(get_db),
	devask_account =  Depends(get_devask_wallet)):
	
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
		
		question_owner_account.balance -= amount
		question_owner_account.spendings += 1
		question_owner_account.total_spent += amount
		db.add(question_owner_account)
		db.commit()


		devask_account.balance += amount
		devask_account.earnings += 1
		devask_account.total_earned += amount
		db.add(devask_account)
		db.add(question_owner_account)
		db.commit()
		db.refresh(devask_account)
		db.refresh(question_owner_account)

		return {"devask_account": devask_account, 
		"question_owner": question_owner_account}
	else:
		return {"code": "error", "balance": question_owner_account.balance,
			"message": "Wallet Balance Insufficience"}



@router.post('/transactions')
def admin_transactions(item: AdminPayments,  db: Session = Depends(get_db),
 devask_account= Depends(get_devask_wallet)):

	question_id=item.question_id
	amount= item.amount
	commission = item.commission

	try:
		question_obj = get_question(question_id, amount, db)
	except:
			raise HTTPException(status_code=404, detail="question not found")
	question_owner_id = question_obj.owner_id
	
	res_obj = admin_deduction(question_owner_id=question_owner_id, amount=amount, db=db, devask_account=devask_account)

	
	admin_obj = res_obj['devask_account']
	question_owner = res_obj['question_owner']

	
	# gets correct selected answer
	correct_answer = get_correct_answer(question_id=question_id, db=db)
	
	if not correct_answer:
		raise HTTPException(status_code=404,
		detail=f"No answer available for question {question_obj.content}")


	if admin_obj.balance >= amount:

		# Admins remits earnings and subtracts commision
		answer_owner_id = correct_answer.owner_id
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
		db.refresh(question_owner)

		return {"code": "success",
				"message": "extra tokens has been added for owner of selected correct answer",
				"amount earned": earned_value,
				"Answer Owner Transaction History": answerer_account,
				"amount deducted": amount,
				"Question Owner History": question_owner
				}


