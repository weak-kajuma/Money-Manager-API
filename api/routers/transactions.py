from fastapi import APIRouter, HTTPException
import random
import datetime

from api.schemas.transactions import Transaction, TransactionCreate, OneRankingResponse, TransactionType
from api.db import mysql_connect

router = APIRouter()

@router.get("/transactions/{transaction_id}", response_model=Transaction)
async def get_transactions(transaction_id: str):
    with mysql_connect().cursor() as cur:
        cur.execute("SELECT * FROM transactions WHERE transaction_id = %s", (transaction_id,))
        return Transaction(**cur.fetchone())

@router.post("/transactions", response_model=Transaction)
async def create_transactions(create_transaction: TransactionCreate):
    with mysql_connect().cursor() as cur:
        cur.execute("SELECT having_money FROM users WHERE user_id = %s", (create_transaction.user_id,))
        having_money = cur.fetchone()["having_money"]
        if having_money is None:
            raise HTTPException(status_code=404, detail="The User is Not Fount")
        cur.execute("SELECT dealer_id FROM dealers WHERE dealer_id = %s", (create_transaction.dealer_id,))
        if cur.fetchone() is None:
            raise HTTPException(status_code=404, detail="The Dealer is Not Fount")
    _transaction_id = format(random.randrange(2**16-1), '04x')
    with mysql_connect() as con:
        with con.cursor() as cur:
            cur.execute("INSERT INTO transactions (transaction_id, user_id, dealer_id, amount, type) VALUES (%s, %s, %s, %s, %s)",
                        (_transaction_id, create_transaction.user_id, create_transaction.dealer_id, create_transaction.amount, create_transaction.type.name))
            # ここからユーザーの所持金計算
            now_money = having_money + create_transaction.amount \
                if create_transaction.type == TransactionType.payout or create_transaction.type == TransactionType.other \
                else having_money - create_transaction.amount
            cur.execute("UPDATE users SET having_money = %s WHERE user_id = %s", (now_money, create_transaction.user_id))

            con.commit()
            cur.execute("SELECT * FROM transactions WHERE transaction_id = %s", (_transaction_id,))
            return Transaction(**cur.fetchone())

@router.get("/rankings", response_model=list[OneRankingResponse])
async def get_rankings():
    with mysql_connect().cursor() as cur:
        cur.execute("SELECT user_id, nickname, having_money, @rank := @rank + 1 AS `rank` FROM users, (SELECT @rank := 0) r ORDER BY having_money DESC")
        return [OneRankingResponse(**user) for user in cur.fetchall()]