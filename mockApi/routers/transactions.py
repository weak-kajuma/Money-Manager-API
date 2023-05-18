from fastapi import APIRouter, HTTPException
import random
import datetime

from mockApi.schemas.transactions import Transaction, TransactionCreate, OneRankingResponse

router = APIRouter()

@router.get("/transactions/{transaction_id}", response_model=Transaction)
async def get_transactions(transaction_id: str):
    return Transaction(transaction_id=transaction_id, user_id="9cf2", dealer_id="d12f", amount=100, type=1, timestamp=datetime.datetime.now())

@router.post("/transactions", response_model=Transaction)
async def create_transactions(create_transaction: TransactionCreate):
    return Transaction(transaction_id="b5eb", **create_transaction.dict(), timestamp=datetime.datetime.now())

@router.get("/rankings", response_model=list[OneRankingResponse])
async def get_rankings():
    return [
        OneRankingResponse(rank=1, user_id="aaaa", nickname="よわいかじゅま", having_money=4000),
        OneRankingResponse(rank=2, user_id="9cf2", nickname="名無しのギャンブラー", having_money=3000)
    ]