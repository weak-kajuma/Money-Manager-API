from fastapi import APIRouter, HTTPException
import random
import datetime

from mockApi.schemas.users import User, CreateUserResponse
from mockApi.schemas.transactions import Transaction

router = APIRouter()

@router.post("/users", response_model=CreateUserResponse)
async def create_user():
    return CreateUserResponse(user_id="9cf2")
        
@router.get("/users", response_model=list[CreateUserResponse])
async def get_users():
    return [
        CreateUserResponse(user_id="9cf2"),
        CreateUserResponse(user_id="aaaa", nickname="よわいかじゅま", having_money=4000)
    ]

@router.get("/users/{user_id}", response_model=User)
async def get_user_info(user_id: str):
    return User(user_id=user_id, transaction_history=[
        Transaction(transaction_id=format(random.randrange(2**16-1), '04x'), user_id=user_id, dealer_id="d12f", amount=100, type=1, timestamp=datetime.datetime.now()),
        Transaction(transaction_id=format(random.randrange(2**16-1), '04x'), user_id=user_id, dealer_id="d12f", amount=300, type=2, timestamp=datetime.datetime.now()),
    ])

@router.put("/users/{user_id}/nickname", response_model=CreateUserResponse)
async def update_name(user_id: str, nickname: str):
    return CreateUserResponse(user_id=user_id, nickname=nickname)
